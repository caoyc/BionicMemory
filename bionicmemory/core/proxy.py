"""OpenAI API proxy service"""
import httpx
from typing import Dict, Any, List
from ..config import settings
from ..models.api_models import ChatCompletionRequest, ChatCompletionResponse


class OpenAIProxy:
    """Proxy for OpenAI API calls with memory injection"""
    
    def __init__(self):
        self.api_key = settings.openai_api_key
        self.api_base = settings.openai_api_base
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def chat_completion(
        self,
        request: ChatCompletionRequest,
        context_memories: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Forward chat completion request to OpenAI with injected memory context.
        
        Args:
            request: Chat completion request
            context_memories: Relevant memories to inject into context
            
        Returns:
            OpenAI API response
        """
        # Inject memories into context if provided
        messages = request.messages.copy()
        
        if context_memories:
            # Create a context message from memories
            memory_context = self._format_memory_context(context_memories)
            
            # Insert context before the last user message
            if len(messages) > 0:
                # Find the last user message
                last_user_idx = -1
                for i in range(len(messages) - 1, -1, -1):
                    if messages[i].role == "user":
                        last_user_idx = i
                        break
                
                if last_user_idx >= 0:
                    # Insert context before last user message
                    context_message = {
                        "role": "system",
                        "content": memory_context
                    }
                    messages.insert(last_user_idx, context_message)
        
        # Prepare request for OpenAI
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": request.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": request.temperature,
            "top_p": request.top_p,
            "n": request.n,
            "stream": request.stream,
            "max_tokens": request.max_tokens,
            "presence_penalty": request.presence_penalty,
            "frequency_penalty": request.frequency_penalty
        }
        
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}
        
        # Make request to OpenAI
        response = await self.client.post(
            f"{self.api_base}/chat/completions",
            headers=headers,
            json=payload
        )
        
        response.raise_for_status()
        return response.json()
    
    def _format_memory_context(self, memories: List[Dict[str, Any]]) -> str:
        """Format memories into context string"""
        if not memories:
            return ""
        
        context_parts = ["# Relevant Context from Memory:\n"]
        
        for i, memory in enumerate(memories, 1):
            temp_indicator = "🔥" if memory["temperature"] > 0.7 else "🌡️" if memory["temperature"] > 0.3 else "❄️"
            context_parts.append(
                f"{i}. {temp_indicator} {memory['content']}"
            )
        
        context_parts.append("\nPlease consider this context when responding.\n")
        
        return "\n".join(context_parts)
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
