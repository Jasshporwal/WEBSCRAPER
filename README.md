# Webscraper Project

This project is a web scraping application that extracts information from websites using FastAPI, LangChain, and OpenAI's language models.


## Features

- Scrapes web pages and extracts structured information
- Uses OpenAI's language models for information extraction
- Implements rate limiting to prevent abuse
- Provides a FastAPI endpoint for easy integration

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/Jasshporwal/WEBSCRAPER.git
   cd WEBSCRAPER
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

1. Start the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

2. Send a POST request to the `/scrape` endpoint with a JSON body containing the URL to scrape:
   ```
   curl -X POST "http://localhost:8000/scrape?url=https://example.com" -H "Content-Type: application/json"
   ```

## API Endpoints

- `POST /scrape`: Scrapes the provided URL and returns extracted information.
  - Query Parameter: `url` (required) - The URL to scrape

## Configuration

The project uses Pydantic's `BaseSettings` for configuration management. You can modify the `Settings` class in `src/calculations/config.py` to add or change configuration options.

## Error Handling

The application includes error handling for invalid API keys, rate limiting, and general exceptions. Check the server logs for detailed error messages.

## Rate Limiting

The application implements rate limiting using the `slowapi` library to prevent abuse of the API.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
