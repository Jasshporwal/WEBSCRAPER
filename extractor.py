from langchain_community.llms import OpenAI
from langchain.chains import create_extraction_chain
from langchain.callbacks.base import BaseCallbackHandler
from typing import List, Dict, Any

# Define the schema for extraction
schema = {
    "properties": {
        "title": {"type": "string"},
        "content": {"type": "string"},
        "author": {"type": "string"},
        "date": {"type": "string"},
    },
    "required": ["title", "content"],
}

class ExtractCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.result = None

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        self.result = outputs.get("output")


async def extract_information(text: str, settings) -> List[Dict[str, Any]]:
    try:
        llm = OpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key=settings.openai_api_key)
        extract_chain = create_extraction_chain(schema, llm)
        
        callback = ExtractCallbackHandler()
        result = extract_chain({"input": text}, callbacks=[callback])
        
        if callback.result is None:
            raise Exception("Failed to extract information")
        
        return callback.result
    except Exception as e:
        raise Exception(f"Error extracting information: {str(e)}")