"""
Memory Manager for Agentcore Demo
Handles both short-term and long-term memory operations
"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import json
from datetime import datetime
import tiktoken


class MemoryManager:
    def __init__(self, stm_max_tokens: int = 2000, collection_name: str = "knight_memories"):
        """Initialize memory management system"""
        self.stm_max_tokens = stm_max_tokens
        self.short_term_memory = []
        
        # Initialize ChromaDB for long-term memory
        self.chroma_client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./chroma_db"
        ))
        
        # Create or get collection
        self.ltm_collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Knight of Seven Kingdoms memories"}
        )
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Token counter
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoding.encode(text))
    
    def add_to_stm(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add message to short-term memory"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.short_term_memory.append(message)
        self._manage_stm_size()
    
    def _manage_stm_size(self):
        """Manage STM size by removing old messages"""
        total_tokens = sum(self.count_tokens(msg["content"]) for msg in self.short_term_memory)
        
        while total_tokens > self.stm_max_tokens and len(self.short_term_memory) > 1:
            removed = self.short_term_memory.pop(0)
            total_tokens -= self.count_tokens(removed["content"])
    
    def get_stm_context(self) -> List[Dict]:
        """Get current short-term memory context"""
        return self.short_term_memory.copy()
    
    def add_to_ltm(self, content: str, category: str, importance: int = 5, metadata: Optional[Dict] = None):
        """Add memory to long-term storage"""
        memory_id = f"{category}_{datetime.now().timestamp()}"
        
        full_metadata = {
            "category": category,
            "importance": importance,
            "timestamp": datetime.now().isoformat(),
            **(metadata or {})
        }
        
        self.ltm_collection.add(
            documents=[content],
            metadatas=[full_metadata],
            ids=[memory_id]
        )
    
    def retrieve_from_ltm(self, query: str, n_results: int = 3, category: Optional[str] = None) -> List[Dict]:
        """Retrieve relevant memories from long-term storage"""
        where_filter = {"category": category} if category else None
        
        results = self.ltm_collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter
        )
        
        memories = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                memories.append({
                    "content": doc,
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i]
                })
        
        return memories
    
    def consolidate_memory(self, stm_message: Dict):
        """Move important STM to LTM"""
        importance = stm_message.get("metadata", {}).get("importance", 5)
        
        if importance >= 7:
            self.add_to_ltm(
                content=stm_message["content"],
                category="conversation",
                importance=importance,
                metadata=stm_message.get("metadata", {})
            )
    
    def clear_stm(self):
        """Clear short-term memory"""
        self.short_term_memory = []
    
    def get_memory_stats(self) -> Dict:
        """Get memory statistics"""
        stm_tokens = sum(self.count_tokens(msg["content"]) for msg in self.short_term_memory)
        ltm_count = self.ltm_collection.count()
        
        return {
            "stm_messages": len(self.short_term_memory),
            "stm_tokens": stm_tokens,
            "stm_capacity": self.stm_max_tokens,
            "ltm_memories": ltm_count
        }
