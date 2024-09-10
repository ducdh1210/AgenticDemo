import os
from enum import Enum
from typing import List, Literal

import pandas as pd
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import (
    AmazonTextractPDFLoader,
    PyMuPDFLoader,
    PyPDFium2Loader,
    PyPDFLoader,
)
from langchain_core.utils.json_schema import dereference_refs
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from openai import RateLimitError
from pydantic import BaseModel, Field

#######################
#  PDF processing tool #
########################


def _make_extraction_prompt_template() -> ChatPromptTemplate:
    """Make a system message from instructions and examples."""
    system_message = (
        "You are a top-tier algorithm for extracting information from text. "
        "Only extract information that is relevant to the provided text. "
        "If no information is relevant, use the schema and output "
        "an empty list where appropriate."
    )
    prompt_components = [("system", system_message)]
    prompt_components.append(
        (
            "human",
            "I need to extract information from "
            "the following text: ```\n{text}\n```",
        ),
    )

    return ChatPromptTemplate.from_messages(prompt_components)


def _update_json_schema(
    schema: dict,
    *,
    multi: bool = True,
) -> dict:
    """Add missing fields to JSON schema and add support for multiple records."""
    if multi:
        # Wrap the schema in an object called "Root" with a property called: "data"
        # which will be a json array of the original schema.
        schema_ = {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": dereference_refs(schema),
                },
            },
            "required": ["data"],
        }
    else:
        raise NotImplementedError("Only multi is supported for now.")

    schema_["title"] = "extractor"
    schema_["description"] = "Extract information matching the given schema."

    return schema_


def load_pdf(
    path: str,
    top_k: int,
    loader_type: str = "PyPDF",
) -> List[str]:
    """
    Load a PDF file using the specified loader type and split it into pages.

    Args:
        path (str): The path to the PDF file.
        loader_type (str): The type of PDF loader to use.
        top_k (int): The maximum number of pages to return.
    Returns:
        List[str]: A list of strings representing the content of each page.
    """
    loader_mapper = {
        "PyPDF": PyPDFLoader,
        "PyPDFium2": PyPDFium2Loader,
        "PyMuPDF": PyMuPDFLoader,
        "AmazonTextractPDF": AmazonTextractPDFLoader,
    }

    if loader_type not in loader_mapper:
        raise ValueError("Invalid loader type")

    loader = loader_mapper.get(loader_type)(path)

    try:
        if loader_type == "AmazonTextractPDF":
            pages = loader.load()
        else:
            pages = loader.load_and_split()
    except Exception as e:
        raise ValueError(f"Failed to load PDF: {e}")

    print(f"Apply {loader_type} on {path} --  Number of pages: {len(pages)}")
    if top_k:
        pages = pages[:top_k]
    return pages


def load_pdf_files(data_dir: str, k=None) -> list[str]:
    files = os.listdir(data_dir)
    if k:
        files = files[:k]
    loaded_docs = []
    for file in files:
        if file.endswith(".pdf"):
            pdf_path = os.path.join(data_dir, file)
            loaded_doc: str = load_pdf(pdf_path, top_k=1)[
                0
            ]  # loaded_doc must be a string, so just take the first result
            loaded_docs.append(loaded_doc)
    return loaded_docs


def list_to_dataframe(data_list):
    # Flatten the nested structure
    flattened_data = []
    for item in data_list:
        for data in item["data"]:
            for utility in data["utilities"]:
                flattened_data.append(utility)

    # Convert the flattened data to a DataFrame
    df = pd.DataFrame(flattened_data)
    return df


def update_extraction_results(
    extraction_results: dict,
    sources: list[str],
    output_format: Literal["df", "json"] = "json",
) -> pd.DataFrame:
    # add file path source back to the extraction results
    for i, extraction_result in enumerate(extraction_results):
        source = sources[i]
        for result in extraction_result["data"]:
            for utility in result["utilities"]:
                utility["source"] = source
    extraction_results_df = list_to_dataframe(extraction_results)

    if output_format == "df":
        return extraction_results_df
    elif output_format == "json":
        return extraction_results_df.to_dict(orient="records")
    else:
        raise ValueError(f"Invalid output format: {output_format}")


class UtilityTypeEnum(Enum):
    ELECTRICITY = "Electricity"
    GAS = "Gas"
    WATER = "Water"
    SEWER = "Sewer"
    OTHER = "Other"


class UtilityBillDetail(BaseModel):
    utility_type: UtilityTypeEnum = Field(..., description="The fixed type of utility")
    utility_type_detail: str = Field(
        ...,
        description="The one-word description of the utility type, can be similar to the utility_type",
    )
    account: str = Field(
        ..., description="The account number associated with the utility bill"
    )
    charge_amount: float = Field(
        ..., description="The total amount specified in the utility bill"
    )
    consumption_amount_unit: str = Field(
        ..., description="The unit of measurement for the energy used, if applicable"
    )
    consumption_amount: float = Field(
        ...,
        description="The amount of energy used as specified in the utility bill, if applicable",
    )
    charge_amount_unit: str = Field(
        ..., description="The unit of currency for the bill amount"
    )
    service_location: str = Field(
        ..., description="The location where the utility service is provided"
    )
    billing_period: str = Field(
        ..., description="The period for which the bill is issued"
    )
    utility_provider: str = Field(
        ..., description="The name of the utility provider issuing the bill"
    )


class UtilityBillSchema(BaseModel):
    utilities: List[UtilityBillDetail] = Field(
        ..., description="A list of utility bill instances"
    )


@tool
def pdf_utility_bill_extraction(data_dir: str) -> pd.DataFrame:
    """
    Run utility bill extraction on the PDF file.
    """
    # Create a prompt template
    prompt_template = _make_extraction_prompt_template()

    # Create a structured output model
    schema = _update_json_schema(UtilityBillSchema.model_json_schema())
    extraction_model = (
        ChatOpenAI(
            model_name=os.getenv("OPENAI_CHAT_MODEL"),
            temperature=os.getenv("OPENAI_CHAT_MODEL_TEMPERATURE"),
        )
        .with_structured_output(schema=schema, method="function_calling")
        .with_config({"run_name": "extraction"})
        .with_retry(
            retry_if_exception_type=(RateLimitError,),  # Retry only on RateLimitError
            wait_exponential_jitter=True,  # Add jitter to the exponential backoff
            stop_after_attempt=2,
        )
    )

    # Make the runnable and run on the loaded PDF file
    runnable = prompt_template | extraction_model

    # Load the PDF files
    loaded_docs = load_pdf_files(os.getenv("DATA_DIR"))
    # loaded_docs = load_pdf_files("/Users/ducdo/Repo/Demo/data/live")

    # Prepare the batch input
    batch_input = [{"text": doc.page_content} for doc in loaded_docs]

    # Run the extraction
    extraction_results = runnable.batch(batch_input)

    # Generate the dataframe
    sources = [doc.metadata["source"].split("/")[-1] for doc in loaded_docs]
    extraction_results = update_extraction_results(
        extraction_results=extraction_results, sources=sources, output_format="json"
    )

    # Display the results
    return extraction_results
