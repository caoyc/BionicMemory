"""ChromaDB vector storage integration"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import uuid


class VectorStore:
    """Vector storage using ChromaDB"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize ChromaDB client"""
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        self.collections: Dict[str, Any] = {}
    
    def get_or_create_collection(self, user_id: str):
        """Get or create a collection for a user"""
        collection_name = f"user_{user_id}"
        
        if collection_name not in self.collections:
            self.collections[collection_name] = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"user_id": user_id}
            )
        
        return self.collections[collection_name]
    
    def add_memory(
        self,
        user_id: str,
        memory_id: str,
        embedding: List[float],
        content: str,
        metadata: Dict[str, Any]
    ):
        """Add a memory to the vector store"""
        collection = self.get_or_create_collection(user_id)
        
        collection.add(
            ids=[memory_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[metadata]
        )
    
    def query_memories(
        self,
        user_id: str,
        query_embedding: List[float],
        n_results: int = 10,
        where: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Query similar memories from vector store"""
        collection = self.get_or_create_collection(user_id)
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where
        )
        
        return results
    
    def update_memory(
        self,
        user_id: str,
        memory_id: str,
        embedding: Optional[List[float]] = None,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Update a memory in the vector store"""
        collection = self.get_or_create_collection(user_id)
        
        update_dict = {"ids": [memory_id]}
        if embedding is not None:
            update_dict["embeddings"] = [embedding]
        if content is not None:
            update_dict["documents"] = [content]
        if metadata is not None:
            update_dict["metadatas"] = [metadata]
        
        collection.update(**update_dict)
    
    def delete_memory(self, user_id: str, memory_id: str):
        """Delete a memory from vector store"""
        collection = self.get_or_create_collection(user_id)
        collection.delete(ids=[memory_id])
    
    def get_memory(self, user_id: str, memory_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific memory by ID"""
        collection = self.get_or_create_collection(user_id)
        
        try:
            result = collection.get(ids=[memory_id])
            if result["ids"]:
                return {
                    "id": result["ids"][0],
                    "embedding": result["embeddings"][0] if result.get("embeddings") else None,
                    "document": result["documents"][0] if result.get("documents") else None,
                    "metadata": result["metadatas"][0] if result.get("metadatas") else None
                }
        except Exception:
            pass
        
        return None
    
    def count_memories(self, user_id: str) -> int:
        """Count memories for a user"""
        collection = self.get_or_create_collection(user_id)
        return collection.count()
