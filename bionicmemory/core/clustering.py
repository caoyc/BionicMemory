"""Clustering suppression for memory deduplication"""
import numpy as np
from typing import List, Dict, Any
from sklearn.metrics.pairwise import cosine_similarity


class ClusteringSuppressor:
    """
    Implements clustering suppression to avoid redundant memories.
    
    When new memories are similar to existing ones, they are either:
    1. Merged with existing memory (boosting its temperature)
    2. Suppressed to avoid duplication
    """
    
    def __init__(self, similarity_threshold: float = 0.85):
        """
        Initialize clustering suppressor.
        
        Args:
            similarity_threshold: Cosine similarity threshold above which
                                memories are considered duplicates
        """
        self.similarity_threshold = similarity_threshold
    
    def find_similar_memories(
        self,
        query_embedding: np.ndarray,
        memory_embeddings: List[np.ndarray],
        memory_ids: List[str]
    ) -> List[tuple]:
        """
        Find memories similar to the query.
        
        Returns:
            List of (memory_id, similarity_score) tuples for similar memories
        """
        if not memory_embeddings:
            return []
        
        # Reshape query embedding
        query_emb = query_embedding.reshape(1, -1)
        
        # Stack memory embeddings
        memory_matrix = np.vstack(memory_embeddings)
        
        # Calculate cosine similarities
        similarities = cosine_similarity(query_emb, memory_matrix)[0]
        
        # Filter by threshold
        similar_indices = np.where(similarities >= self.similarity_threshold)[0]
        
        return [(memory_ids[i], similarities[i]) for i in similar_indices]
    
    def should_suppress(
        self,
        new_embedding: np.ndarray,
        existing_embeddings: List[np.ndarray],
        existing_ids: List[str]
    ) -> tuple:
        """
        Determine if a new memory should be suppressed.
        
        Returns:
            (should_suppress: bool, similar_memory_id: str or None, similarity: float)
        """
        similar_memories = self.find_similar_memories(
            new_embedding,
            existing_embeddings,
            existing_ids
        )
        
        if similar_memories:
            # Find most similar memory
            most_similar = max(similar_memories, key=lambda x: x[1])
            return True, most_similar[0], most_similar[1]
        
        return False, None, 0.0
    
    def merge_strategy(
        self,
        similarity: float,
        boost_base: float = 0.3
    ) -> float:
        """
        Calculate temperature boost based on similarity.
        
        Higher similarity = stronger boost (reinforcing existing memory)
        """
        # Boost proportional to similarity
        return boost_base * similarity
