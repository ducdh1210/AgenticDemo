from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.pydantic_v1 import BaseModel, Field


class QAPair(BaseModel):
    """Question and answer pair generated from context."""

    question: str = Field(description="The generated question based on the context")
    answer: str = Field(description="The answer to the generated question")


def create_structured_qa_chain():
    # Create the language model
    llm = ChatOpenAI(temperature=0.7)

    # Create the prompt template
    prompt = ChatPromptTemplate.from_template(
        "Based on the provided context, please generate a clear and concise question along with its corresponding answer:\n\n"
        "Context: {context}\n\n"
        "Your response should be formatted as a question followed by the answer."
    )

    # Create the chain with structured output
    chain = (
        {"context": RunnablePassthrough()} | prompt | llm.with_structured_output(QAPair)
    )

    return chain


# Example usage
if __name__ == "__main__":
    context = "The Python programming language was created by Guido van Rossum and first released in 1991. It is known for its simplicity and readability, making it a popular choice for beginners and experienced programmers alike."

    qa_chain = create_structured_qa_chain()
    result = qa_chain.invoke(context)

    print(f"Question: {result.question}")
    print(f"Answer: {result.answer}")
    print("\nFull output:")
    print(result.model_dump_json(indent=2))

# TODO: refactoring in this generate evaluation by chunks

# from backend.schema.embedding import LangchainPGCollection, LangchainPGEmbedding
# from backend.schema.evaluation import Evaluation
# from backend.config import CONNECTION_STRING
# from sqlmodel import create_engine, Session, select
# from backend.database import SessionLocal

# import pandas as pd


# def load_embeddings_to_dataframe():
#     engine = create_engine(CONNECTION_STRING)
#     with Session(engine) as session:
#         embeddings = session.exec(select(LangchainPGEmbedding)).all()
#         embeddings_list = []
#         for embedding in embeddings:
#             embeddings_list.append(
#                 {
#                     "id": embedding.id,
#                     "collection_id": embedding.collection_id,
#                     "embedding": embedding.embedding,
#                     "document": embedding.document,
#                     "cmetadata": embedding.cmetadata,
#                 }
#             )
#         df = pd.DataFrame(embeddings_list)
#         # Extracting the keys from 'cmetadata' into separate columns
#         df_expanded = pd.concat(
#             [df.drop(columns=["cmetadata"]), df["cmetadata"].apply(pd.Series)], axis=1
#         )

#         return df_expanded


# if __name__ == "__main__":
#     df = load_embeddings_to_dataframe()
#     print(df)
