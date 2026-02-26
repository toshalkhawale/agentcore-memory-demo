"""
Memory Manager for Agentcore Demo
Handles both short-term and long-term memory operations
"""

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import json
from datetime import datetime
import tiktoken
import pickle
import os


class MemoryManager:
    def __init__(self, stm_max_tokens: int = 200, collection_name: str = "knight_memories"):
        """Initialize memory management system"""
        self.stm_max_tokens = stm_max_tokens
        self.short_term_memory = []
        
        # Initialize FAISS for long-term memory
        self.collection_name = collection_name
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding_dim = 384  # Dimension for all-MiniLM-L6-v2
        
        # Initialize FAISS index
        self.ltm_index = faiss.IndexFlatL2(self.embedding_dim)
        self.ltm_metadata = []  # Store metadata separately
        
        # Load existing memories if available
        self._load_ltm()
        
        # Token counter
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def _load_ltm(self):
        """Load long-term memory from disk"""
        index_path = f"./{self.collection_name}_index.faiss"
        metadata_path = f"./{self.collection_name}_metadata.pkl"
        
        if os.path.exists(index_path) and os.path.exists(metadata_path):
            self.ltm_index = faiss.read_index(index_path)
            with open(metadata_path, 'rb') as f:
                self.ltm_metadata = pickle.load(f)
    
    def _save_ltm(self):
        """Save long-term memory to disk"""
        index_path = f"./{self.collection_name}_index.faiss"
        metadata_path = f"./{self.collection_name}_metadata.pkl"
        
        faiss.write_index(self.ltm_index, index_path)
        with open(metadata_path, 'wb') as f:
            pickle.dump(self.ltm_metadata, f)
    
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
        # Generate embedding
        embedding = self.embedding_model.encode([content])[0]
        
        # Add to FAISS index
        self.ltm_index.add(np.array([embedding], dtype=np.float32))
        
        # Store metadata
        full_metadata = {
            "content": content,
            "category": category,
            "importance": importance,
            "timestamp": datetime.now().isoformat(),
            **(metadata or {})
        }
        self.ltm_metadata.append(full_metadata)
        
        # Save to disk
        self._save_ltm()
    
    def retrieve_from_ltm(self, query: str, n_results: int = 3, category: Optional[str] = None) -> List[Dict]:
        """Retrieve relevant memories from long-term storage"""
        if self.ltm_index.ntotal == 0:
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0]
        
        # Search in FAISS
        distances, indices = self.ltm_index.search(
            np.array([query_embedding], dtype=np.float32), 
            min(n_results, self.ltm_index.ntotal)
        )
        
        # Retrieve metadata
        memories = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.ltm_metadata):
                metadata = self.ltm_metadata[idx]
                if category is None or metadata.get("category") == category:
                    memories.append({
                        "content": metadata["content"],
                        "metadata": metadata,
                        "distance": float(distances[0][i])
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
        ltm_count = self.ltm_index.ntotal
        
        return {
            "stm_messages": len(self.short_term_memory),
            "stm_tokens": stm_tokens,
            "stm_capacity": self.stm_max_tokens,
            "ltm_memories": ltm_count
        }
