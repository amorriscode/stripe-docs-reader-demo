import os
from pinecone import Pinecone, ServerlessSpec
from llama_index import VectorStoreIndex, download_loader, StorageContext
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

# Set up the StripeDocsReader
print("Loading data...")

StripeDocsReader = download_loader("StripeDocsReader")
loader = StripeDocsReader()

# Iterate through all of the Stripe docs using the StripeDocsReader
documents = loader.load_data()

print("Data loaded!")

print("Creating index from documents...")

# Initialize Pinecone index
# https://docs.llamaindex.ai/en/stable/examples/vector_stores/PineconeIndexDemo.html
pc = Pinecone(api_key=PINECONE_API_KEY)
if "stripe-docs" not in pc.list_indexes().names():
    pc.create_index(
        name="stripe-docs",
        dimension=1536,
        metric='euclidean',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-west-2'
        )
    )
pinecone_index = pc.Index("stripe-docs")

# Create the vector store and index
# https://docs.llamaindex.ai/en/stable/understanding/indexing/indexing.html
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, show_progress=True, storage_context=storage_context)

print("Index created!")
