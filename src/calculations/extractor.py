from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
from src.calculations.config import Settings


class ExtractedInfo(BaseModel):
    title: str = Field(description="The title of the article")
    summary: str = Field(description="A brief summary of the article")
    key_points: List[str] = Field(description="A list of key points from the article")


async def extract_information(text: str, settings: Settings) -> ExtractedInfo:
    prompt = ChatPromptTemplate.from_template(
        "Extract the following information from the given text:\n"
        "1. The title of the article\n"
        "2. A brief summary of the article\n"
        "3. A list of key points from the article\n\n"
        "Text: {text}\n\n"
        "Provide the output in the following format:\n"
        "Title: [title]\n"
        "Summary: [summary]\n"
        "Key Points:\n"
        "- [point 1]\n"
        "- [point 2]\n"
        "...\n"
    )

    model = ChatOpenAI(
        temperature=0, model="gpt-3.5-turbo", openai_api_key=settings.openai_api_key
    )
    parser = PydanticOutputParser(pydantic_object=ExtractedInfo)

    chain = prompt | model | parser

    try:
        result = await chain.ainvoke({"text": text})
        return result
    except Exception as e:
        print(f"Error in extract_information: {str(e)}")
        return ExtractedInfo(
            title="Error in extraction",
            summary="An error occurred while extracting information.",
            key_points=["Unable to extract key points due to an error."],
        )
