import threading
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from starlette.middleware.cors import CORSMiddleware

from app.services.search import search_web
from app.services.llm_client import setup_rag_system, query_documents
from myproject.spiders.example_spider import MySpider

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

results = []
def run_crawler(manual_urls):
    print("inside run_crawler")
    global results
    results.clear()
    process = CrawlerProcess(get_project_settings())
    process.crawl(MySpider, results=results, start_urls=manual_urls)
    process.start()

@app.post("/ask")
async def ask_question(request: QueryRequest):
    query = request.query
    try:
        web_results = search_web(query)
        manual_urls = []

        if not web_results:
            raise HTTPException(status_code=404, detail="No search results found.")


        for item in web_results:
            print("item=> ",item)
            manual_urls.append(item['link'])

        thread = threading.Thread(target=run_crawler, args=(manual_urls,))
        thread.start()
        thread.join()

        print("enriched_data=> ",results)
        if not results[0]:
            return {
                "query": query,
                "top_results": [item['link'] for item in web_results[:3]]
            }

        if not results or not results[0]:
            raise HTTPException(status_code=500, detail="Failed to enrich search results.")

        content = results
        query_engine = setup_rag_system(content)
        response_data = query_documents(query_engine, query)

        return {
            "query": query,
            "answer": response_data.response,
            "top_results": [item['link'] for item in web_results[:3]]  # Optional: return top 3 results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def main():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    main()