# AI Research Agent

An intelligent full-stack application that autonomously researches web information to answer complex user queries. The system performs web searches, scrapes relevant content, and uses AI to synthesize comprehensive answers with source citations.

## 🚀 Features

- **Interactive Web Interface**: Clean React.js frontend with search functionality
- **Autonomous Web Research**: Automated Google search and content extraction
- **Multi-source Analysis**: Scrapes and analyzes top search results
- **AI-Powered Synthesis**: Uses Llama 3.2:1b model for intelligent answer generation
- **Source Citations**: Provides credible references with URLs and titles
- **Error Handling**: Robust error management for network and processing issues

## 🏗️ Architecture

### Frontend (React.js)
- **Components**: Modular React components for UI elements
- User-friendly search interface
- Real-time query processing
- Error handling and user feedback
- Response display with source links

### Backend (Python)
The backend is structured with a clean separation of concerns:

#### API Layer (`app/api/`)
- **main.py**: Main application entry point and API endpoints
- Handles HTTP requests and responses
- Coordinates between services

#### Service Layer (`app/services/`)
- **search.py**: SerpAPI integration for web search functionality
- **llm_client.py**: Llama 3.2:1b model interface and LlamaIndex operations
- Business logic and core processing

#### Scrapy Project (`myProject/`)
- **spiders/example_spider.py**: Web scraping spider implementation
- **middlewares.py**: Custom downloader middlewares
- **settings.py**: Scrapy configuration and settings

The backend processing follows three main milestones:

#### Milestone 1: Web Search
- **Technology**: SerpAPI integration
- **Function**: Performs Google searches and retrieves top result URLs
- **Output**: Ranked list of relevant web pages

#### Milestone 2: Content Extraction
- **Technology**: Scrapy + Splash
- **Function**: Scrapes content from top 3 search results
- **Processing**: Runs on separate threads for optimal performance
- **Output**: Clean, structured text data from web sources

#### Milestone 3: AI Analysis & Synthesis
- **Technology**: Llama 3.2:1b + LlamaIndex
- **Function**: 
  - Chunks scraped content using LlamaIndex
  - Creates vector index of resources
  - Queries the index with user's question
  - Synthesizes comprehensive answer
- **Output**: Structured response with source citations

## 🛠️ Technology Stack

### Frontend
- **React.js** - User interface framework
- **JavaScript/JSX** - Frontend logic and components

### Backend
- **Python** - Core backend language
- **SerpAPI** - Google search integration
- **Scrapy** - Web scraping framework
- **Splash** - JavaScript rendering service
- **Llama 3.2:1b** - Large language model
- **LlamaIndex** - Document indexing and retrieval
- **Multiprocessing** - Used to run Scrapy in isolated processes to avoid Twisted reactor conflicts



## 📋 Prerequisites

- Node.js
- Python
- SerpAPI key
- Splash server running
- Ollama or compatible LLM runtime

## 💡 Usage

1. **Start the Application**
   - Launch the backend server
   - Start the React frontend
   - Ensure Splash server is running

2. **Query the System**
   - Enter your question in the search bar
   - Click the send button
   - Wait for the AI to research and respond

3. **View Results**
   - Read the synthesized answer
   - Check provided source links
   - Review any error messages if issues occur

## 🔄 Processing Flow

```
User Query → Frontend → Backend API
    ↓
SerpAPI Search → Top URLs Retrieved
    ↓
Scrapy + Splash → Content Extraction (Threaded)
    ↓
LlamaIndex Chunking → Vector Index Creation
    ↓
Llama 3.2:1b Processing → Answer Synthesis
    ↓
Response with Citations → Frontend Display
```

## 🛡️ Error Handling

- **Network Errors**: Graceful handling of connection issues
- **Scraping Failures**: Fallback mechanisms for inaccessible content
- **LLM Processing**: Timeout and error recovery for model inference
- **User Feedback**: Clear error messages displayed in frontend

## 🎯 Example Use Cases

- **Product Comparisons**: *"Compare the latest electric vehicle models and their safety features"*
- **Market Research**: *"What are the current trends in renewable energy investment?"*
- **Technical Analysis**: *"Explain the latest developments in quantum computing"*
- **News Synthesis**: *"Summarize recent developments in AI regulation"*

## 📁 Project Structure

```
ai-research-agent/
│
├── frontend/
│   ├── components/
│   ├── package.json
│   └── package-lock.json
│
└── backend/
    ├── app/
    │   ├── api/
    │   │   ├── __init__.py
    │   │   └── main.py
    │   ├── services/
    │   │   ├── __init__.py
    │   │   ├── llm_client.py
    │   │   └── search.py
    │   └── __init__.py
    ├── myProject/
    │   ├── spiders/
    │   │   ├── __init__.py
    │   │   └── example_spider.py
    │   ├── __init__.py
    │   ├── items.py
    │   ├── middlewares.py
    │   ├── pipelines.py
    │   └── settings.py
    ├── .gitignore
    └── scrapy.cfg
```
