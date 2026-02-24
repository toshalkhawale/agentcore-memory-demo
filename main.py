"""
Main CLI Demo for Agentcore Memory System
Knight of the Seven Kingdoms
"""

import os
from dotenv import load_dotenv
from core import MemoryManager, KnightAgent

# Load environment variables
load_dotenv()


def print_banner():
    """Print demo banner"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║     AGENTCORE MEMORY RETRIEVAL DEMO                       ║
║     Knight of the Seven Kingdoms                          ║
║     ACD Ahmedabad 2026                                    ║
╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_memory_stats(agent: KnightAgent):
    """Print current memory statistics"""
    stats = agent.get_memory_stats()
    print("\n" + "="*60)
    print("MEMORY STATISTICS")
    print("="*60)
    print(f"Short-term Memory: {stats['stm_messages']} messages ({stats['stm_tokens']}/{stats['stm_capacity']} tokens)")
    print(f"Long-term Memory: {stats['ltm_memories']} stored memories")
    print("="*60 + "\n")


def main():
    """Main demo function"""
    print_banner()
    
    # Initialize memory manager
    print("Initializing memory systems...")
    stm_max_tokens = int(os.getenv("STM_MAX_TOKENS", 2000))
    collection_name = os.getenv("LTM_COLLECTION_NAME", "knight_memories")
    
    memory_manager = MemoryManager(
        stm_max_tokens=stm_max_tokens,
        collection_name=collection_name
    )
    
    # Initialize agent
    agent = KnightAgent(memory_manager)
    print("✓ Memory systems initialized")
    print("✓ Knight persona loaded\n")
    
    # Display greeting
    print(agent.get_greeting())
    print("\n" + "-"*60)
    print("Commands: 'stats' - show memory stats | 'quit' - exit demo")
    print("-"*60 + "\n")
    
    # Main conversation loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nSer Duncan: Farewell, friend. May honor guide your path.")
                break
            
            if user_input.lower() == 'stats':
                print_memory_stats(agent)
                continue
            
            # Process message
            response = agent.process_message(user_input)
            print(f"\nSer Duncan: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nSer Duncan: Farewell, friend. May honor guide your path.")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()
