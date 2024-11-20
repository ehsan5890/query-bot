import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

# Database connection settings
db_host = os.getenv("DATABASE_HOST", "localhost")
db_port = os.getenv("DATABASE_PORT", "6333")

# Initialize the Qdrant client
qdrant_client = QdrantClient(host=db_host, port=int(db_port))
openai.api_key = os.getenv("OPENAI_API_KEY")
