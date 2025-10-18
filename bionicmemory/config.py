"""Configuration management for BionicMemory"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # OpenAI API Configuration
    openai_api_key: str = ""
    openai_api_base: str = "https://api.openai.com/v1"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Memory Configuration
    memory_decay_rate: float = 0.1
    memory_threshold: float = 0.01
    short_term_memory_size: int = 100
    long_term_memory_size: int = 1000
    
    # Embedding Model
    embedding_model: str = "Qwen/Qwen2-0.5B-Instruct"
    embedding_device: str = "cpu"
    
    # ChromaDB Configuration
    chroma_persist_directory: str = "./chroma_db"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
