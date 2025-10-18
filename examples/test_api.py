"""Example usage of BionicMemory API"""
import httpx
import asyncio
import json


async def test_memory_system():
    """Test the BionicMemory system"""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        print("🧠 BionicMemory API Test\n")
        
        # 1. Health check
        print("1. Checking health...")
        response = await client.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
        
        # 2. Add memories
        print("2. Adding memories...")
        memories_to_add = [
            {
                "user_id": "test_user",
                "content": "Python is a high-level programming language known for its simplicity.",
                "metadata": {"topic": "programming", "language": "python"}
            },
            {
                "user_id": "test_user",
                "content": "Machine learning is a subset of AI that learns from data.",
                "metadata": {"topic": "AI", "field": "machine_learning"}
            },
            {
                "user_id": "test_user",
                "content": "The Ebbinghaus forgetting curve describes how memory decays over time.",
                "metadata": {"topic": "psychology", "concept": "memory"}
            }
        ]
        
        for mem in memories_to_add:
            response = await client.post(f"{base_url}/v1/memories", json=mem)
            result = response.json()
            print(f"   Added: {result['status']} - {result['memory_id'][:8]}...")
        
        print()
        
        # 3. Query memories
        print("3. Querying memories...")
        query_request = {
            "user_id": "test_user",
            "query": "Tell me about programming languages",
            "n_results": 5
        }
        
        response = await client.post(f"{base_url}/v1/memories/query", json=query_request)
        memories = response.json()
        
        print(f"   Found {len(memories)} relevant memories:")
        for mem in memories:
            temp_icon = "🔥" if mem["temperature"] > 0.7 else "🌡️" if mem["temperature"] > 0.3 else "❄️"
            print(f"   {temp_icon} [{mem['temperature']:.2f}] {mem['content'][:60]}...")
        
        print()
        
        # 4. Get stats
        print("4. Getting memory stats...")
        response = await client.get(f"{base_url}/v1/memories/stats/test_user")
        stats = response.json()
        print(f"   Total memories: {stats['total_memories']}")
        print(f"   Hot memories: {stats['hot_memories']}")
        print(f"   Avg temperature: {stats['avg_temperature']:.2f}")
        
        print("\n✅ Test completed!")


async def test_chat_completion():
    """Test chat completion with memory"""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        print("\n💬 Testing Chat Completion with Memory\n")
        
        request = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": "What do you know about programming?"}
            ],
            "user": "test_user"
        }
        
        print("Sending chat request...")
        try:
            response = await client.post(f"{base_url}/v1/chat/completions", json=request)
            if response.status_code == 200:
                result = response.json()
                print(f"Response: {result['choices'][0]['message']['content'][:200]}...")
            else:
                print(f"Error: {response.status_code}")
                print(f"Note: This requires valid OPENAI_API_KEY in .env")
        except Exception as e:
            print(f"Note: Chat completion test requires OpenAI API key")
            print(f"Error: {e}")


if __name__ == "__main__":
    print("Make sure the BionicMemory server is running on http://localhost:8000")
    print("Run: python main.py\n")
    
    asyncio.run(test_memory_system())
    # Uncomment to test chat completion (requires OpenAI API key)
    # asyncio.run(test_chat_completion())
