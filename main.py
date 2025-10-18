"""Main entry point for BionicMemory server"""
import uvicorn
from bionicmemory.config import settings


def main():
    """Run the BionicMemory server"""
    uvicorn.run(
        "bionicmemory.api.app:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
