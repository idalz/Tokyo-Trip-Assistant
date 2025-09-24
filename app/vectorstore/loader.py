"""
Vector store loader for Tokyo Trip Assistant.
Loads travel data and creates embeddings in Pinecone.
"""

import json
from typing import List, Dict, Any
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI

from app.core.config import settings
from app.core.logger import logger

class VectorStoreLoader:
    """Handles loading data to Pinecone vector store."""

    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.index_name = settings.PINECONE_INDEX_NAME
        self.dimension = 1536  # text-embedding-3-small

    def create_index_if_not_exists(self):
        """Create Pinecone index if it doesn't exist."""
        if self.index_name not in self.pc.list_indexes().names():
            logger.info(f"Creating Pinecone index: {self.index_name}")
            self.pc.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud=settings.PINECONE_CLOUD,
                    region=settings.PINECONE_REGION
                )
            )
        else:
            logger.info(f"Pinecone index {self.index_name} already exists")

    def load_travel_data(self, data_path: str = "app/data/tokyo_guide.json") -> List[Dict[str, Any]]:
        """Load travel data from JSON file."""
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Loaded {len(data)} items from {data_path}")
            return data
        except FileNotFoundError:
            logger.error(f"Data file not found: {data_path}")
            return []

    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings using OpenAI."""
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=texts
            )
            embeddings = [item.embedding for item in response.data]
            logger.info(f"Created {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            logger.error(f"Error creating embeddings: {e}")
            return []

    def upload_to_pinecone(self, data: List[Dict[str, Any]]):
        """Upload data with embeddings to Pinecone."""
        self.create_index_if_not_exists()
        index = self.pc.Index(self.index_name)

        # Prepare texts for embedding
        texts = []
        for item in data:
            # Create searchable text from item data
            text = f"{item.get('title', '')} {item.get('content', '')} {item.get('category', '')} {item.get('area', '')}"
            texts.append(text)

        # Create embeddings
        embeddings = self.create_embeddings(texts)

        if not embeddings:
            logger.error("No embeddings created, skipping upload")
            return

        # Prepare vectors for upload
        vectors = []
        for i, (item, embedding) in enumerate(zip(data, embeddings)):
            # Ensure ASCII-only vector ID by encoding non-ASCII characters
            original_id = item.get('id', f"item_{i}")
            ascii_id = original_id.encode('ascii', 'ignore').decode('ascii')
            if not ascii_id:  # If all characters were non-ASCII, use fallback
                ascii_id = f"item_{i}"

            vector = {
                "id": ascii_id,
                "values": embedding,
                "metadata": {
                    "title": item.get('title', ''),
                    "content": item.get('content', ''),
                    "category": item.get('category', ''),
                    "area": item.get('area', ''),
                    "original_id": item.get('id', '')  # Keep original ID in metadata
                }
            }
            vectors.append(vector)

        # Upload in batches with namespace
        batch_size = 100
        namespace = settings.PINECONE_NAMESPACE
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            index.upsert(vectors=batch, namespace=namespace)
            logger.info(f"Uploaded batch {i//batch_size + 1}/{(len(vectors) + batch_size - 1)//batch_size} to namespace '{namespace}'")

        logger.info(f"Successfully uploaded {len(vectors)} vectors to Pinecone")

def main():
    """Main function to load data to vector store."""
    logger.info("Starting vector store loader...")
    logger.info(f"PINECONE_API_KEY present: {bool(settings.PINECONE_API_KEY)}")
    logger.info(f"OPENAI_API_KEY present: {bool(settings.OPENAI_API_KEY)}")
    loader = VectorStoreLoader()
    data = loader.load_travel_data()
    if data:
        logger.info(f"Loaded {len(data)} items, uploading to Pinecone...")
        loader.upload_to_pinecone(data)
        logger.info("Upload complete!")
    else:
        logger.error("No data to upload")

if __name__ == "__main__":
    main()