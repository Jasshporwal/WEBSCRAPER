from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from extractor import extract_information
from config import Settings

async def scrape_website(url: str, settings: Settings):
    try:
        # Load HTML content
        loader = AsyncHtmlLoader([url])
        docs = await loader.load()

        # Transform HTML to text
        bs_transformer = BeautifulSoupTransformer()
        docs_transformed = bs_transformer.transform_documents(docs)

        # Extract content from specific tags
        extracted_content = []
        for doc in docs_transformed:
            soup = bs_transformer.soup_maker(doc.page_content)
            for tag in ['p', 'li', 'div', 'a', 'span']:
                elements = soup.find_all(tag)
                extracted_content.extend([element.get_text(strip=True) for element in elements])

        # Join extracted content
        text = ' '.join(extracted_content)

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        splits = text_splitter.split_text(text)

        # Extract information using LLM
        extracted_info = []
        for split in splits:
            result = await extract_information(split, settings)
            extracted_info.extend(result)

        return extracted_info
    except Exception as e:
        raise Exception(f"Error scraping website: {str(e)}")