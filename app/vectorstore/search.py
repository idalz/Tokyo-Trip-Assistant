"""
Vector store search for Tokyo Trip Assistant.
Handles semantic search queries against the Pinecone knowledge base.
"""

from typing import List, Dict, Any, Optional
from pinecone import Pinecone
from openai import OpenAI

from app.core.config import settings
from app.core.logger import logger


class VectorStoreSearcher:
    """Handles semantic search queries against Pinecone vector store."""

    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.index_name = settings.PINECONE_INDEX_NAME
        self.namespace = settings.PINECONE_NAMESPACE
        self.index = self.pc.Index(self.index_name)

    def create_query_embedding(self, query: str) -> List[float]:
        """Create embedding for search query using OpenAI."""
        try:
            response = self.openai_client.embeddings.create(
                model=settings.OPENAI_EMBEDDING_MODEL,
                input=[query]
            )
            embedding = response.data[0].embedding
            logger.debug(f"Created embedding for query: '{query[:50]}...'")
            return embedding
        except Exception as e:
            logger.error(f"Error creating query embedding: {e}")
            return []

    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None,
        include_scores: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search against the knowledge base.

        Args:
            query: Natural language search query
            top_k: Number of results to return
            filter_dict: Optional metadata filters (e.g., {"category": "temple"})
            include_scores: Whether to include similarity scores

        Returns:
            List of search results with metadata and optional scores
        """
        try:
            # Create embedding for the query
            query_embedding = self.create_query_embedding(query)
            if not query_embedding:
                logger.error("Failed to create query embedding")
                return []

            # Perform vector search
            search_results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                namespace=self.namespace,
                filter=filter_dict,
                include_metadata=True,
                include_values=False  # Don't return the actual vectors
            )

            # Format results
            results = []
            for match in search_results.matches:
                result = {
                    "id": match.id,
                    "metadata": match.metadata,
                    "title": match.metadata.get("title", ""),
                    "content": match.metadata.get("content", ""),
                    "category": match.metadata.get("category", ""),
                    "area": match.metadata.get("area", ""),
                }

                if include_scores:
                    result["score"] = round(match.score, 4)

                results.append(result)

            logger.info(f"Found {len(results)} results for query: '{query[:50]}...'")
            return results

        except Exception as e:
            logger.error(f"Error performing search: {e}")
            return []

    def search_by_category(
        self,
        query: str,
        category: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Search within a specific category (temple, shrine, viewpoint, etc.)."""
        filter_dict = {"category": category}
        return self.search(query, top_k=top_k, filter_dict=filter_dict)

    def search_by_area(
        self,
        query: str,
        area: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Search within a specific area/neighborhood."""
        filter_dict = {"area": area}
        return self.search(query, top_k=top_k, filter_dict=filter_dict)

    def get_similar_items(
        self,
        item_id: str,
        top_k: int = 5,
        exclude_self: bool = True
    ) -> List[Dict[str, Any]]:
        """Find items similar to a given item."""
        try:
            # Get the vector for the given item
            fetch_result = self.index.fetch(ids=[item_id], namespace=self.namespace)

            if not fetch_result.vectors or item_id not in fetch_result.vectors:
                logger.warning(f"Item {item_id} not found in vector store")
                return []

            item_vector = fetch_result.vectors[item_id].values

            # Search for similar items
            adjust_k = top_k + 1 if exclude_self else top_k
            search_results = self.index.query(
                vector=item_vector,
                top_k=adjust_k,
                namespace=self.namespace,
                include_metadata=True,
                include_values=False
            )

            # Format results and optionally exclude the original item
            results = []
            for match in search_results.matches:
                if exclude_self and match.id == item_id:
                    continue

                result = {
                    "id": match.id,
                    "metadata": match.metadata,
                    "title": match.metadata.get("title", ""),
                    "content": match.metadata.get("content", ""),
                    "category": match.metadata.get("category", ""),
                    "area": match.metadata.get("area", ""),
                    "score": round(match.score, 4)
                }
                results.append(result)

            # Trim to requested number if we excluded self
            if exclude_self:
                results = results[:top_k]

            logger.info(f"Found {len(results)} similar items for {item_id}")
            return results

        except Exception as e:
            logger.error(f"Error finding similar items: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store."""
        try:
            stats = self.index.describe_index_stats()
            namespace_stats = stats.namespaces.get(self.namespace, {})

            return {
                "total_vectors": stats.total_vector_count,
                "namespace": self.namespace,
                "namespace_vectors": namespace_stats.get("vector_count", 0),
                "dimension": stats.dimension,
                "index_fullness": stats.index_fullness
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {}


def main():
    """Test the vector store searcher."""
    searcher = VectorStoreSearcher()

    # Test basic search
    print("=== Testing Basic Search ===")
    results = searcher.search("temples with beautiful gardens", top_k=3)
    for result in results:
        print(f"- {result['title']} (Score: {result['score']})")
        print(f"  {result['content'][:100]}...")
        print()

    # Test category search
    print("=== Testing Category Search ===")
    results = searcher.search_by_category("best views", "viewpoint", top_k=3)
    for result in results:
        print(f"- {result['title']} (Score: {result['score']})")
        print()

    # Test stats
    print("=== Vector Store Stats ===")
    stats = searcher.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()