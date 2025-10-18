"""Integrated memory system combining all components"""
import uuid
import time
from typing import List, Dict, Any, Optional
import numpy as np

from ..core.memory import MemoryManager, MemoryItem
from ..core.embedding import EmbeddingService
from ..core.storage import VectorStore
from ..core.clustering import ClusteringSuppressor
from ..config import settings


class BionicMemorySystem:
    """
    Integrated memory management system with:
    - Newton cooling-based forgetting
    - Vector similarity search
    - Clustering suppression
    - User isolation
    """
    
    def __init__(self):
        """Initialize the memory system"""
        self.memory_manager = MemoryManager(
            decay_rate=settings.memory_decay_rate,
            threshold=settings.memory_threshold,
            short_term_size=settings.short_term_memory_size,
            long_term_size=settings.long_term_memory_size
        )
        
        self.embedding_service = EmbeddingService(
            model_name=settings.embedding_model,
            device=settings.embedding_device
        )
        
        self.vector_store = VectorStore(
            persist_directory=settings.chroma_persist_directory
        )
        
        self.clustering_suppressor = ClusteringSuppressor(
            similarity_threshold=0.85
        )
    
    def add_memory(
        self,
        user_id: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Add a new memory with clustering suppression.
        
        Returns:
            Dictionary with memory_id and status (added/merged/suppressed)
        """
        if metadata is None:
            metadata = {}
        
        # Generate embedding
        embedding = self.embedding_service.encode_single(content)
        
        # Check for similar memories (clustering suppression)
        user_memories = self.memory_manager.get_user_memories(user_id)
        
        if user_memories:
            existing_embeddings = [
                np.array(self.vector_store.get_memory(user_id, mem_id)["embedding"])
                for mem_id in [str(i) for i, _ in enumerate(user_memories)]
                if self.vector_store.get_memory(user_id, str(i))
            ]
            existing_ids = [str(i) for i in range(len(user_memories))]
            
            # Check if should suppress
            should_suppress, similar_id, similarity = self.clustering_suppressor.should_suppress(
                embedding,
                existing_embeddings,
                existing_ids
            )
            
            if should_suppress and similar_id:
                # Merge with existing memory by boosting its temperature
                boost = self.clustering_suppressor.merge_strategy(similarity)
                self.memory_manager.access_memory(similar_id, boost=boost)
                
                # Update metadata to indicate reinforcement
                existing_memory = self.vector_store.get_memory(user_id, similar_id)
                if existing_memory:
                    updated_metadata = existing_memory.get("metadata", {})
                    updated_metadata["reinforced_at"] = time.time()
                    updated_metadata["reinforcement_count"] = updated_metadata.get("reinforcement_count", 0) + 1
                    self.vector_store.update_memory(user_id, similar_id, metadata=updated_metadata)
                
                return {
                    "memory_id": similar_id,
                    "status": "merged",
                    "similarity": float(similarity)
                }
        
        # Add new memory
        memory_id = str(uuid.uuid4())
        
        # Add to memory manager
        memory = self.memory_manager.add_memory(
            memory_id=memory_id,
            content=content,
            embedding=embedding.tolist(),
            metadata=metadata,
            user_id=user_id
        )
        
        # Add to vector store
        self.vector_store.add_memory(
            user_id=user_id,
            memory_id=memory_id,
            embedding=embedding.tolist(),
            content=content,
            metadata={
                **metadata,
                "temperature": memory.temperature,
                "created_at": memory.created_at
            }
        )
        
        return {
            "memory_id": memory_id,
            "status": "added"
        }
    
    def query_memories(
        self,
        user_id: str,
        query: str,
        n_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Query relevant memories for a user.
        
        Returns memories sorted by relevance and temperature.
        """
        # Update all temperatures before querying
        self.memory_manager.update_temperatures()
        
        # Generate query embedding
        query_embedding = self.embedding_service.encode_single(query)
        
        # Query vector store
        results = self.vector_store.query_memories(
            user_id=user_id,
            query_embedding=query_embedding.tolist(),
            n_results=n_results * 2  # Get more results to filter by temperature
        )
        
        # Combine with temperature information
        memories = []
        for i, mem_id in enumerate(results.get("ids", [[]])[0]):
            memory = self.memory_manager.memories.get(mem_id)
            
            # Skip cold memories
            if memory and not memory.is_cold(self.memory_manager.threshold):
                # Access the memory (boosts temperature)
                memory.access(boost=0.1)
                
                memories.append({
                    "id": mem_id,
                    "content": results["documents"][0][i],
                    "temperature": memory.temperature,
                    "metadata": results["metadatas"][0][i],
                    "distance": results.get("distances", [[]])[0][i] if results.get("distances") else None,
                    "created_at": memory.created_at,
                    "last_accessed": memory.last_accessed,
                    "access_count": memory.access_count
                })
        
        # Sort by temperature (hottest first)
        memories.sort(key=lambda m: m["temperature"], reverse=True)
        
        return memories[:n_results]
    
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get statistics for a user's memories"""
        self.memory_manager.update_temperatures()
        
        user_memories = self.memory_manager.get_user_memories(user_id)
        
        if not user_memories:
            return {
                "total_memories": 0,
                "hot_memories": 0,
                "cold_memories": 0,
                "avg_temperature": 0.0
            }
        
        temperatures = [m.temperature for m in user_memories]
        cold_count = sum(1 for m in user_memories if m.is_cold(self.memory_manager.threshold))
        
        return {
            "total_memories": len(user_memories),
            "hot_memories": len(user_memories) - cold_count,
            "cold_memories": cold_count,
            "avg_temperature": sum(temperatures) / len(temperatures)
        }
    
    def cleanup_memories(self, user_id: Optional[str] = None):
        """Clean up cold memories"""
        cleaned = self.memory_manager.cleanup_cold_memories()
        
        # Also remove from vector store
        # Note: In production, you'd want to batch this operation
        for memory_id in list(self.memory_manager.memories.keys()):
            memory = self.memory_manager.memories.get(memory_id)
            if memory and memory.is_cold(self.memory_manager.threshold):
                if user_id is None or memory.user_id == user_id:
                    self.vector_store.delete_memory(memory.user_id, memory_id)
        
        return cleaned
