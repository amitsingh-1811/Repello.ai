from llama_index.core import (
    VectorStoreIndex,
    Settings,
    Document
)
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

llm = Ollama(
    model="llama3.2:1b",
    base_url="http://localhost:11434",
    request_timeout=120.0
)

embed_model = OllamaEmbedding(
    model_name="llama3.2:1b",
    base_url="http://localhost:11434",
)

Settings.llm = llm
Settings.embed_model = embed_model


def create_sample_documents(enriched_data):
    parser = SimpleNodeParser.from_defaults(chunk_size=512, chunk_overlap=50)
    nodes = parser.get_nodes_from_documents([Document(text=enriched_data[0])])
    return nodes


def setup_rag_system(enriched_data):
    nodes = create_sample_documents(enriched_data)

    print(f"Loaded {len(nodes)} documents",nodes)

    print("Creating vector index...")
    index = VectorStoreIndex(nodes)

    query_engine = index.as_query_engine(
        similarity_top_k=3,
        response_mode="compact"
    )

    return query_engine


def query_documents(query_engine, question):
    print(f"\n🔍 Question: {question}")
    print("Processing...")

    response = query_engine.query(question)
    print("response=> ",response)

    return response
