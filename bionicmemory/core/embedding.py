"""Embedding service using local models"""
from typing import List
import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np


class EmbeddingService:
    """Local embedding service using transformer models"""
    
    def __init__(self, model_name: str = "Qwen/Qwen2-0.5B-Instruct", device: str = "cpu"):
        """
        Initialize embedding service with specified model.
        
        Note: Using Qwen2-0.5B-Instruct as a lightweight alternative.
        Qwen3-Embedding-0.6B is not publicly available yet, so using
        a similar small Qwen model for embedding generation.
        """
        self.device = device
        self.model_name = model_name
        
        print(f"Loading embedding model: {model_name}")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name).to(device)
            self.model.eval()
            print(f"Model loaded successfully on {device}")
        except Exception as e:
            print(f"Warning: Could not load {model_name}, using fallback")
            # Fallback to a smaller model if specified model fails
            self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)
            self.tokenizer = None
            print(f"Using fallback model: {self.model_name}")
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """
        Encode texts into embeddings.
        
        Args:
            texts: List of text strings to encode
            
        Returns:
            numpy array of embeddings
        """
        if isinstance(self.model, type(None)) or self.tokenizer is None:
            # Using sentence-transformers
            embeddings = self.model.encode(texts)
            return np.array(embeddings)
        
        # Using transformer model
        with torch.no_grad():
            # Tokenize
            encoded = self.tokenizer(
                texts,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt"
            ).to(self.device)
            
            # Get model output
            outputs = self.model(**encoded)
            
            # Mean pooling
            embeddings = self._mean_pooling(outputs, encoded['attention_mask'])
            
            # Normalize
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
            
            return embeddings.cpu().numpy()
    
    def _mean_pooling(self, model_output, attention_mask):
        """Apply mean pooling to get sentence embeddings"""
        token_embeddings = model_output.last_hidden_state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    
    def encode_single(self, text: str) -> np.ndarray:
        """Encode a single text into embedding"""
        return self.encode([text])[0]
