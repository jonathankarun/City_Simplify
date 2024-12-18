from qdrant_client import QdrantClient, models
import openai

from qdrant_client.http.models import CollectionDescription

class QdrantClientWrapper:
    def __init__(self):
        self.client = QdrantClient(
            url="https://931bba9e-744e-4123-8d98-9d68d0b64a55.us-west-2-0.aws.cloud.qdrant.io:6333",
            api_key="xhdRxCUTBZ-RC286QU_R_nkfVziAhOTIQsyzqNEEZElKRtGJTVuZpA"
        )
        self._initialize_collection()

    def _initialize_collection(self):
        collection_name = "citychat_documents"
        try:
            #Checks to see if the collection exists
            collections = self.client.get_collections()
            if any(coll.name == collection_name for coll in collections.collections):
                print(f"Collection '{collection_name}' already exists.")
            else:
                self.client.create_collection(
                    collection_name=collection_name,
                    vector_size=1536,
                    distance="Cosine"
                )
                print(f"Collection '{collection_name}' created successfully.")
        except Exception as e:
            print(f"Error initializing collection: {e}") #Error catching 

    def upload_text(self, text: str):
        chunks = text.split(". ")  # Split text into sentences
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
