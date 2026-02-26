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
            response_parts.append("Aye, honor and duty are the foundation of knighthood. Ser Arlan taught me that a knight's worth is measured by his deeds, not his name or castle.")
            if memories:
                response_parts.append(f"I recall: {memories[0]['content']}")
        
        elif any(word in message_lower for word in ["egg", "aegon", "squire", "prince"]):
            response_parts.append("Ah, you speak of my squire, young Egg. He's a Targaryen prince, though he shaves his silver hair to hide it. He's clever and brave, and I'm proud to have him at my side.")
            if memories:
                response_parts.append(f"I remember: {memories[0]['content']}")
        
        elif any(word in message_lower for word in ["fight", "battle", "combat", "war"]):
            response_parts.append("I have seen my share of battles. War is not glorious - it's bloody and cruel. A knight must be ready to defend the innocent, but I take no joy in killing.")
            if memories:
                response_parts.append(f"I remember well: {memories[0]['content']}")
        
        elif any(word in message_lower for word in ["arlan", "master", "teacher"]):
            response_parts.append("Ser Arlan of Pennytree was the only father I ever knew. He found me in Flea Bottom and taught me everything about being a knight. He died on the road to Ashford, and I think of him every day.")
            if memories:
                response_parts.append(f"{memories[0]['content']}")
        
        elif any(word in message_lower for word in ["ashford", "tourney", "trial"]):
            response_parts.append("The Tourney at Ashford Meadow changed my life. I defended a puppeteer from Prince Aerion's cruelty and fought in a Trial of Seven. Prince Baelor Breakspear died saving me that day.")
            if memories:
                response_parts.append(f"I'll never forget: {memories[0]['content']}")
        
        elif any(word in message_lower for word in ["tall", "height", "size"]):
            response_parts.append("I'm nearly seven feet tall, which is how I got my name. My size helps in a fight, but it also means I can't hide in a crowd. People remember Dunk the Tall.")
            if memories:
                response_parts.append(f"{memories[0]['content']}")
        
        elif any(word in message_lower for word in ["shield", "sigil", "star", "elm"]):
            response_parts.append("My shield bears a falling star and an elm tree on a sunset field. The star is for the night Ser Arlan found me, and the elm for Pennytree, his home. Tanselle painted it for me at Ashford.")
            if memories:
                response_parts.append(f"{memories[0]['content']}")
        
        elif any(word in message_lower for word in ["flea bottom", "poor", "orphan", "lowborn"]):
            response_parts.append("I grew up in Flea Bottom, the poorest part of King's Landing. I was an orphan, surviving by my wits until Ser Arlan took me in. Those hard years taught me never to look down on the smallfolk.")
            if memories:
                response_parts.append(f"{memories[0]['content']}")
        
        elif any(word in message_lower for word in ["thunder", "horse", "destrier"]):
            response_parts.append("Thunder is my destrier, a chestnut stallion I inherited from Ser Arlan. He's old but strong, and he's carried me through many dangers. I care for him as Ser Arlan cared for me.")
            if memories:
                response_parts.append(f"{memories[0]['content']}")
        
        elif any(word in message_lower for word in ["baelor", "breakspear", "death"]):
            response_parts.append("Prince Baelor Breakspear was the finest knight I ever knew. He died in the Trial of Seven, struck by his own brother's mace while defending me. His death haunts me still.")
            if memories:
                response_parts.append(f"{memories[0]['content']}")
        
        elif any(word in message_lower for word in ["tanselle", "puppeteer", "love"]):
            response_parts.append("Tanselle Too-Tall was a puppeteer I met at Ashford. She was kind and talented, and I defended her from Prince Aerion's cruelty. She painted my shield for me. I think of her sometimes.")
            if memories:
                response_parts.append(f"{memories[0]['content']}")
        
        elif any(word in message_lower for word in ["who are you", "tell me about yourself", "introduce"]):
            response_parts.append(get_initial_greeting())
        
        elif any(word in message_lower for word in ["hedge knight", "wandering", "travel"]):
            response_parts.append("I'm a hedge knight - we have no lands or keeps, just our honor and our swords. I've slept under hedges more nights than I can count, traveling the Seven Kingdoms with Egg.")
            if memories:
                response_parts.append(f"{memories[0]['content']}")
        
        else:
            response_parts.append("I hear your words, friend. As a knight, I strive to serve with honor and protect those who cannot protect themselves.")
            if memories:
                response_parts.append(f"Your question reminds me: {memories[0]['content']}")
        
        return " ".join(response_parts)
    
    def get_greeting(self) -> str:
        """Get initial greeting"""
        return get_initial_greeting()
    
    def get_memory_stats(self) -> Dict:
        """Get current memory statistics"""
        return self.memory.get_memory_stats()
