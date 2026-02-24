"""
Test Scenarios for Agentcore Memory Demo
Demonstrates different memory retrieval patterns
"""

from core import MemoryManager, KnightAgent


def scenario_1_conversation_continuity():
    """Test STM maintaining conversation context"""
    print("\n" + "="*60)
    print("SCENARIO 1: Conversation Continuity (STM)")
    print("="*60)
    
    memory = MemoryManager(stm_max_tokens=2000)
    agent = KnightAgent(memory)
    
    messages = [
        "Who are you?",
        "What did you just tell me?",
        "Do you remember your name?"
    ]
    
    for msg in messages:
        print(f"\nUser: {msg}")
        response = agent.process_message(msg)
        print(f"Ser Duncan: {response}")
        
        stats = agent.get_memory_stats()
        print(f"[STM: {stats['stm_messages']} messages, {stats['stm_tokens']} tokens]")


def scenario_2_knowledge_recall():
    """Test LTM retrieving relevant memories"""
    print("\n" + "="*60)
    print("SCENARIO 2: Knowledge Recall (LTM)")
    print("="*60)
    
    memory = MemoryManager(stm_max_tokens=2000)
    agent = KnightAgent(memory)
    
    queries = [
        "Tell me about honor and duty",
        "What do you know about trials?",
        "Who is your squire?"
    ]
    
    for query in queries:
        print(f"\nUser: {query}")
        response = agent.process_message(query)
        print(f"Ser Duncan: {response}")
        
        # Show retrieved memories
        memories = memory.retrieve_from_ltm(query, n_results=2)
        print(f"\n[Retrieved {len(memories)} relevant memories from LTM]")
        for i, mem in enumerate(memories, 1):
            print(f"  {i}. {mem['content'][:80]}...")


def scenario_3_memory_capacity():
    """Test STM capacity management"""
    print("\n" + "="*60)
    print("SCENARIO 3: Memory Capacity Management")
    print("="*60)
    
    memory = MemoryManager(stm_max_tokens=500)  # Small capacity for demo
    agent = KnightAgent(memory)
    
    # Send multiple messages to exceed capacity
    for i in range(10):
        msg = f"This is message number {i+1}. Tell me something about knighthood."
        print(f"\nUser: {msg}")
        response = agent.process_message(msg)
        
        stats = agent.get_memory_stats()
        print(f"[STM: {stats['stm_messages']} messages, {stats['stm_tokens']}/{stats['stm_capacity']} tokens]")
        
        if stats['stm_tokens'] >= stats['stm_capacity'] * 0.9:
            print("⚠️  STM near capacity - oldest messages being removed")


def scenario_4_hybrid_retrieval():
    """Test combined STM + LTM retrieval"""
    print("\n" + "="*60)
    print("SCENARIO 4: Hybrid Retrieval (STM + LTM)")
    print("="*60)
    
    memory = MemoryManager(stm_max_tokens=2000)
    agent = KnightAgent(memory)
    
    # Build conversation context
    conversation = [
        ("Tell me about a battle you fought", "Discussing battles"),
        ("Why did you fight in that battle?", "Referencing previous context"),
        ("What values guided your decision?", "Combining recent context with core values")
    ]
    
    for msg, note in conversation:
        print(f"\nUser: {msg}")
        print(f"[{note}]")
        
        response = agent.process_message(msg)
        print(f"Ser Duncan: {response}")
        
        # Show context sources
        stm_context = memory.get_stm_context()
        ltm_memories = memory.retrieve_from_ltm(msg, n_results=2)
        
        print(f"\nContext sources:")
        print(f"  - STM: {len(stm_context)} recent messages")
        print(f"  - LTM: {len(ltm_memories)} relevant memories")


def scenario_5_memory_persistence():
    """Test LTM persistence across sessions"""
    print("\n" + "="*60)
    print("SCENARIO 5: Memory Persistence")
    print("="*60)
    
    # Session 1
    print("\n--- Session 1 ---")
    memory1 = MemoryManager(collection_name="test_persistence")
    agent1 = KnightAgent(memory1)
    
    msg = "Tell me about your shield"
    print(f"User: {msg}")
    response = agent1.process_message(msg)
    print(f"Ser Duncan: {response}")
    
    stats1 = agent1.get_memory_stats()
    print(f"LTM memories: {stats1['ltm_memories']}")
    
    # Session 2 (new instance, same collection)
    print("\n--- Session 2 (New Instance) ---")
    memory2 = MemoryManager(collection_name="test_persistence")
    agent2 = KnightAgent(memory2)
    
    stats2 = agent2.get_memory_stats()
    print(f"LTM memories: {stats2['ltm_memories']}")
    print(f"✓ Memories persisted across sessions!")
    
    # Query from new session
    msg2 = "What symbols are on your shield?"
    print(f"\nUser: {msg2}")
    response2 = agent2.process_message(msg2)
    print(f"Ser Duncan: {response2}")


def run_all_scenarios():
    """Run all test scenarios"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║     AGENTCORE MEMORY DEMO - TEST SCENARIOS                ║
║     Knight of the Seven Kingdoms                          ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    scenarios = [
        scenario_1_conversation_continuity,
        scenario_2_knowledge_recall,
        scenario_3_memory_capacity,
        scenario_4_hybrid_retrieval,
        scenario_5_memory_persistence
    ]
    
    for scenario in scenarios:
        try:
            scenario()
            input("\nPress Enter to continue to next scenario...")
        except KeyboardInterrupt:
            print("\n\nDemo interrupted by user.")
            break
        except Exception as e:
            print(f"\nError in scenario: {e}")
            continue
    
    print("\n" + "="*60)
    print("All scenarios completed!")
    print("="*60)


if __name__ == "__main__":
    run_all_scenarios()
