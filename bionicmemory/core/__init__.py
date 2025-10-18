"""Core module initialization"""
# Lazy imports to avoid loading heavy dependencies unless needed
__all__ = ["MemoryItem", "MemoryManager", "EmbeddingService", "VectorStore", "ClusteringSuppressor"]

def __getattr__(name):
    if name == "MemoryItem":
        from .memory import MemoryItem
        return MemoryItem
    elif name == "MemoryManager":
        from .memory import MemoryManager
        return MemoryManager
    elif name == "EmbeddingService":
        from .embedding import EmbeddingService
        return EmbeddingService
    elif name == "VectorStore":
        from .storage import VectorStore
        return VectorStore
    elif name == "ClusteringSuppressor":
        from .clustering import ClusteringSuppressor
        return ClusteringSuppressor
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
