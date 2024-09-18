from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.text_splitter import CharacterTextSplitter
from extractor import extract_information
from config import Settings
from bs4 import BeautifulSoup
import aiohttp
from extractor import extract_information, ExtractedInfo

async def scrape_website(url: str, settings: Settings):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                html_content = await response.text()

        print(f"HTML content: {html_content[:500]}...")  # Print first 500 characters of HTML

        # Parse HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract content from specific tags
        extracted_content = []
        for tag in ['p', 'li', 'div', 'a', 'span', 'article', 'section', 'main', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            elements = soup.find_all(tag)
            for element in elements:
                text = element.get_text(strip=True)
                if text:  # Only add non-empty strings
                    extracted_content.append(text)

        print(f"Total extracted items: {len(extracted_content)}")

        # Join extracted content
        text = ' '.join(extracted_content)
        print(f"Combined text length: {len(text)}")

        # Split text into chunks
        text_splitter = CharacterTextSplitter(chunk_size=4000, chunk_overlap=200)
        splits = text_splitter.split_text(text)
        print(f"Number of splits: {len(splits)}")
        
        # Extract information using LLM
        extracted_info = []
        for i, split in enumerate(splits):
            print(f"Processing split {i+1}")
            try:
                result = await extract_information(split, settings)
                if isinstance(result, ExtractedInfo):
                    extracted_info.append(result)
                else:
                    print(f"Unexpected result type from extract_information: {type(result)}")
            except Exception as e:
                if "invalid_api_key" in str(e):
                    raise ValueError("Invalid OpenAI API key. Please check your configuration.") from e
                else:
                    print(f"Error processing split {i+1}: {str(e)}")
                    extracted_info.append(ExtractedInfo(
                        title=f"Error in extraction (split {i+1})",
                        summary=f"An error occurred while extracting information from split {i+1}.",
                        key_points=[f"Unable to extract key points from split {i+1} due to an error."]
                    ))

        return extracted_info

    except ValueError as ve:
        print(f"API Key Error: {str(ve)}")
        raise
    except Exception as e:
        print(f"Error in scrape_website: {str(e)}")
        raise