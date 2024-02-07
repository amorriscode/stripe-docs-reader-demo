import os
from pinecone import Pinecone
from llama_index import VectorStoreIndex, StorageContext
from llama_index.vector_stores import PineconeVectorStore
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY environment not set")

if not PINECONE_API_KEY:
    raise Exception("PINECONE_API_KEY environment not set")

# Set the Open API key
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Initialize Pinecone index
pc = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pc.Index("stripe-docs")

# Create the vector store and index
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(vector_store, show_progress=True, storage_context=storage_context)

# Create the query engine
query_engine = index.as_query_engine(response_mode="refine")

print("How can I help you today?")
q = input()

# Querying has the following steps:
# 1. Retrieve documents from the index
# 2. Post-process the documents
# 3. Send the prompt + documents to an LLM
# https://docs.llamaindex.ai/en/stable/understanding/querying/querying.html
res = query_engine.query(f"""
You are a world class expert at Stripe integrations.

Your job is to provide detailed answers to help Stripe users integrate their products with Stripe.

I will provide you with relevant Stripe documentation. You will provide detailed answers to the questions asked.
                         
NEVER tell users to read the documentation or contact Stripe support. Always provide the answer directly.
                         
Use citations when possible.
                         
Use real code examples when applicable.

You have been asked the following question: {q}""")

print(f"""\n{res}""")
