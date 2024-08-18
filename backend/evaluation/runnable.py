from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough


# def create_qa_chain():
#     llm = ChatOpenAI(temperature=0.7)

#     template = """
#     Your task is to review the context text and generate a pair of question and answer in  JSON format and must contain following keys: question, answer.

#     Context: {context}

#     For example:
#     Context: "Joe Biden is the 46th president of United States"
#     Response: {{"question": "How many American presidents so far?", "answer": "There are 46 American presidents up to now."}}    ...

#     Questions and Answers:
#     """

#     prompt = ChatPromptTemplate.from_template(template)

#     chain = {"context": RunnablePassthrough()} | prompt | llm | StrOutputParser()

#     return chain


# # Example usage
# if __name__ == "__main__":
#     context = "The Python programming language was created by Guido van Rossum and first released in 1991. It is known for its simplicity and readability, making it a popular choice for beginners and experienced programmers alike."

#     qa_chain = create_qa_chain()
#     result = qa_chain.invoke(context)

#     print(result)

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.pydantic_v1 import BaseModel, Field
from langchain.schema.runnable import RunnablePassthrough


class QAPair(BaseModel):
    question: str = Field(description="The generated question")
    answer: str = Field(description="The answer to the generated question")


def create_qa_chain():
    llm = ChatOpenAI(temperature=0.7)

    output_parser = PydanticOutputParser(pydantic_object=QAPair)

    template = """
    Given the following context, generate a single question and its corresponding answer:

    Context: {context}

    {format_instructions}

    Question and Answer:
    """

    prompt = ChatPromptTemplate.from_template(template)

    chain = (
        {
            "context": RunnablePassthrough(),
            "format_instructions": output_parser.get_format_instructions(),
        }
        | prompt
        | llm
        | output_parser
    )

    return chain


# Example usage
if __name__ == "__main__":
    context = "The Python programming language was created by Guido van Rossum and first released in 1991. It is known for its simplicity and readability, making it a popular choice for beginners and experienced programmers alike."

    qa_chain = create_qa_chain()
    result = qa_chain.invoke(context)

    print(f"Question: {result.question}")
    print(f"Answer: {result.answer}")
