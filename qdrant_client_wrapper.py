# app/qdrant_client_wrapper.py
import os
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import CollectionDescription
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

class QdrantClientWrapper:
    def __init__(self):
        self.collection_name = "citychat_documents"
        self.client = QdrantClient(
            url=os.getenv("QDRANT-URL-ADDRESS"),
            api_key=os.getenv("QDRANT-API-KEY")
        )
        self._initialize_collection()

    def _initialize_collection(self):
        try:
            collections = self.client.get_collections()
            if any(coll.name == self.collection_name for coll in collections.collections):
                print(f"Collection '{self.collection_name}' already exists.")
            else:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vector_size=1536,
                    distance="Cosine"
                )
                print(f"Collection '{self.collection_name}' created successfully.")
        except Exception as e:
            print(f"Error initializing collection: {e}")

    def upload_text(self, text: str):
        chunks = text.split(". ")
        points = []
        for i, chunk in enumerate(chunks):
            vector = self._vectorize_text(chunk)
            points.append(models.PointStruct(
                id=i,
                payload={"text": chunk},
                vector=vector
            ))
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def query(self, query_text: str) -> str:
        query_vector = self._vectorize_text(query_text)
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=5
        )
        return "\n".join(hit.payload["text"] for hit in results)

    def _vectorize_text(self, text: str) -> list:
        try:
            response = openai.Embedding.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response['data'][0]['embedding']
        except Exception as e:
            raise ValueError(f"Failed to vectorize text: {e}")

