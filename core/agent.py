"""
Agentcore - Main Agent with Memory Integration
"""

from typing import List, Dict, Optional
from .memory_manager import MemoryManager
from .knight_persona import KNIGHT_PERSONA, get_system_prompt, get_initial_greeting


class KnightAgent:
    def __init__(self, memory_manager: MemoryManager):
        """Initialize the Knight Agent"""
        self.memory = memory_manager
        self.persona = KNIGHT_PERSONA
        self.system_prompt = get_system_prompt()
        
        # Initialize LTM with core memories
        self._initialize_core_memories()
    
    def _initialize_core_memories(self):
        """Load core persona memories into LTM"""
        for memory in self.persona["core_memories"]:
            self.memory.add_to_ltm(
                content=memory["content"],
                category=memory["category"],
                importance=memory["importance"]
            )
    
    def process_message(self, user_message: str) -> str:
        """Process user message and generate response"""
        # Add user message to STM
        self.memory.add_to_stm("user", user_message)
        
        # Retrieve relevant LTM
        relevant_memories = self.memory.retrieve_from_ltm(user_message, n_results=3)
        
        # Build context
        context = self._build_context(relevant_memories)
        
        # Generate response (simplified - in production use LLM)
        response = self._generate_response(user_message, context, relevant_memories)
        
        # Add response to STM
        self.memory.add_to_stm("assistant", response)
        
        return response
    
    def _build_context(self, relevant_memories: List[Dict]) -> str:
        """Build context from STM and relevant LTM"""
        context_parts = []
        
        # Add system prompt
        context_parts.append(f"SYSTEM: {self.system_prompt}\n")
        
        # Add relevant long-term memories
        if relevant_memories:
            context_parts.append("RELEVANT MEMORIES:")
            for mem in relevant_memories:
                context_parts.append(f"- {mem['content']} (importance: {mem['metadata'].get('importance', 'N/A')})")
            context_parts.append("")
        
        # Add recent conversation
        context_parts.append("RECENT CONVERSATION:")
        for msg in self.memory.get_stm_context()[-5:]:
            context_parts.append(f"{msg['role'].upper()}: {msg['content']}")
        
        return "\n".join(context_parts)
    
    def _generate_response(self, user_message: str, context: str, memories: List[Dict]) -> str:
        """Generate response based on context and memories"""
        # This is a simplified response generator
        # In production, this would call an LLM with the context
        
        response_parts = []
        
        # Analyze user message for keywords
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ["honor", "duty", "knight", "chivalry"]):
            response_parts.append("Aye, honor and duty are the foundation of knighthood.")
            if memories:
                response_parts.append(f"I recall {memories[0]['content']}")
        
        elif any(word in message_lower for word in ["egg", "aegon", "squire"]):
            response_parts.append("Ah, you speak of my squire, young Egg. A fine lad, though he has secrets of his own.")
        
        elif any(word in message_lower for word in ["fight", "battle", "combat"]):
            response_parts.append("I have seen my share of battles. A knight must be ready to defend the innocent.")
            if memories:
                response_parts.append(f"I remember well: {memories[0]['content']}")
        
        elif any(word in message_lower for word in ["who are you", "tell me about yourself"]):
            response_parts.append(get_initial_greeting())
        
        else:
            response_parts.append("I hear your words, friend. As a knight, I strive to serve with honor.")
            if memories:
                response_parts.append(f"Your question reminds me: {memories[0]['content']}")
        
        return " ".join(response_parts)
    
    def get_greeting(self) -> str:
        """Get initial greeting"""
        return get_initial_greeting()
    
    def get_memory_stats(self) -> Dict:
        """Get current memory statistics"""
        return self.memory.get_memory_stats()
