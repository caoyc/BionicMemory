"""Core memory management with Newton cooling formula"""
import time
import math
from typing import Dict, Any, Optional
from datetime import datetime


class MemoryItem:
    """Represents a single memory item with temperature-based decay"""
    
    def __init__(
        self,
        content: str,
        embedding: list,
        metadata: Dict[str, Any],
        user_id: str,
        initial_temperature: float = 1.0
    ):
        self.content = content
        self.embedding = embedding
        self.metadata = metadata
        self.user_id = user_id
        self.temperature = initial_temperature
        self.created_at = time.time()
        self.last_accessed = time.time()
        self.access_count = 0
    
    def calculate_temperature(self, decay_rate: float = 0.1) -> float:
        """
        Calculate current temperature using Newton cooling formula.
        
        Newton's Law of Cooling: T(t) = T_ambient + (T_initial - T_ambient) * e^(-k*t)
        Where:
        - T(t) is temperature at time t
        - T_ambient is ambient temperature (0 in our case, representing complete forgetting)
        - T_initial is initial temperature (1.0)
        - k is decay rate
        - t is time elapsed since last access
        
        This simulates the Ebbinghaus forgetting curve where memories decay exponentially
        over time unless reinforced through access.
        """
        time_elapsed = time.time() - self.last_accessed
        # Newton cooling formula: T(t) = T_ambient + (T_0 - T_ambient) * e^(-k*t)
        ambient_temp = 0.0
        self.temperature = ambient_temp + (self.temperature - ambient_temp) * math.exp(-decay_rate * time_elapsed)
        return self.temperature
    
    def access(self, boost: float = 0.3):
        """
        Access the memory item and boost its temperature.
        
        Implements "use it or lose it" strategy by increasing temperature
        when memory is accessed, reinforcing the memory.
        """
        self.last_accessed = time.time()
        self.access_count += 1
        # Boost temperature but cap at 1.0
        self.temperature = min(1.0, self.temperature + boost)
    
    def is_cold(self, threshold: float = 0.01) -> bool:
        """Check if memory has cooled below threshold (should be forgotten)"""
        return self.temperature < threshold
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert memory item to dictionary"""
        return {
            "content": self.content,
            "embedding": self.embedding,
            "metadata": self.metadata,
            "user_id": self.user_id,
            "temperature": self.temperature,
            "created_at": self.created_at,
            "last_accessed": self.last_accessed,
            "access_count": self.access_count
        }


class MemoryManager:
    """Manages memory items with temperature-based decay"""
    
    def __init__(
        self,
        decay_rate: float = 0.1,
        threshold: float = 0.01,
        short_term_size: int = 100,
        long_term_size: int = 1000
    ):
        self.decay_rate = decay_rate
        self.threshold = threshold
        self.short_term_size = short_term_size
        self.long_term_size = long_term_size
        self.memories: Dict[str, MemoryItem] = {}
    
    def add_memory(
        self,
        memory_id: str,
        content: str,
        embedding: list,
        metadata: Dict[str, Any],
        user_id: str
    ) -> MemoryItem:
        """Add a new memory item"""
        memory = MemoryItem(
            content=content,
            embedding=embedding,
            metadata=metadata,
            user_id=user_id
        )
        self.memories[memory_id] = memory
        return memory
    
    def access_memory(self, memory_id: str, boost: float = 0.3) -> Optional[MemoryItem]:
        """Access and boost a memory item"""
        if memory_id in self.memories:
            memory = self.memories[memory_id]
            memory.access(boost)
            return memory
        return None
    
    def update_temperatures(self):
        """Update all memory temperatures based on time decay"""
        for memory in self.memories.values():
            memory.calculate_temperature(self.decay_rate)
    
    def cleanup_cold_memories(self):
        """Remove memories that have cooled below threshold"""
        cold_memories = [
            memory_id for memory_id, memory in self.memories.items()
            if memory.is_cold(self.threshold)
        ]
        for memory_id in cold_memories:
            del self.memories[memory_id]
        return len(cold_memories)
    
    def get_user_memories(self, user_id: str) -> list:
        """Get all memories for a specific user"""
        return [
            memory for memory in self.memories.values()
            if memory.user_id == user_id
        ]
    
    def get_hot_memories(self, user_id: str, limit: int = 10) -> list:
        """Get hottest (most recent/accessed) memories for a user"""
        user_memories = self.get_user_memories(user_id)
        # Sort by temperature (descending)
        user_memories.sort(key=lambda m: m.temperature, reverse=True)
        return user_memories[:limit]
