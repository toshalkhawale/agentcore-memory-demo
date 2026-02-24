# Agentcore Memory Demo - Presentation Guide
## ACD Ahmedabad 2026

## Overview
This demo showcases a dual-memory architecture for AI agents using the "Knight of the Seven Kingdoms" persona.

## Key Concepts

### 1. Short-Term Memory (STM)
- **Purpose**: Maintains recent conversation context
- **Implementation**: Sliding window buffer with token limits
- **Capacity**: 2000 tokens (configurable)
- **Behavior**: Automatically removes oldest messages when capacity reached

### 2. Long-Term Memory (LTM)
- **Purpose**: Persistent knowledge storage
- **Implementation**: Vector database (ChromaDB) with semantic search
- **Storage**: Embeddings using Sentence Transformers
- **Retrieval**: Similarity-based search for relevant memories

### 3. Memory Retrieval Strategy

#### Recency-Based (STM)
```
Recent messages → Immediate context
Advantages: Fast, maintains conversation flow
Limitations: Limited capacity, loses old context
```

#### Relevance-Based (LTM)
```
User query → Embedding → Similarity search → Top-K memories
Advantages: Retrieves semantically relevant information
Limitations: May miss exact matches, requires good embeddings
```

#### Hybrid Approach (Our Implementation)
```
1. User sends message
2. Add to STM
3. Query LTM for relevant memories
4. Combine STM + LTM for context
5. Generate response
6. Store important interactions in LTM
```

## Demo Scenarios

### Scenario 1: Conversation Continuity
**Goal**: Show STM maintaining recent context

```
User: "Who are you?"
Agent: [Introduces self as Ser Duncan]

User: "What did you just tell me?"
Agent: [References previous introduction from STM]
```

### Scenario 2: Knowledge Recall
**Goal**: Show LTM retrieving relevant memories

```
User: "Tell me about honor"
Agent: [Retrieves memories about Trial of Seven, knightly values]

User: "What about your squire?"
Agent: [Retrieves memories about Egg/Prince Aegon]
```

### Scenario 3: Memory Statistics
**Goal**: Show memory management in action

```
1. Start conversation - observe STM growing
2. Continue until STM reaches capacity
3. Watch oldest messages being removed
4. Check LTM count - see persistent storage
```

### Scenario 4: Context Switching
**Goal**: Demonstrate hybrid retrieval

```
User: "Tell me about a battle you fought"
Agent: [Retrieves LTM about Trial of Seven + recent STM context]

User: "Why did you fight?"
Agent: [Uses STM to understand "you" refers to previous battle]
```

## Technical Architecture

```
┌─────────────────────────────────────────┐
│         User Interface (CLI/Web)        │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│         Knight Agent                    │
│  - Process messages                     │
│  - Build context                        │
│  - Generate responses                   │
└────────┬───────────────────┬────────────┘
         │                   │
┌────────▼────────┐  ┌──────▼─────────────┐
│  Memory Manager │  │  Persona Config    │
│  - STM buffer   │  │  - Character data  │
│  - LTM storage  │  │  - Core memories   │
│  - Retrieval    │  │  - Speaking style  │
└────────┬────────┘  └────────────────────┘
         │
┌────────▼────────────────────────────────┐
│         Storage Layer                   │
│  - ChromaDB (Vector DB)                 │
│  - Sentence Transformers (Embeddings)   │
└─────────────────────────────────────────┘
```

## Running the Demo

### CLI Version
```bash
python main.py
```
- Interactive command-line interface
- Type 'stats' to see memory statistics
- Type 'quit' to exit

### Web Version
```bash
python app.py
```
- Open browser to http://localhost:5000
- Visual interface with real-time stats
- Reset button to clear STM

## Key Talking Points

1. **Why Dual Memory?**
   - STM: Fast, maintains conversation flow
   - LTM: Persistent, semantic retrieval
   - Together: Best of both worlds

2. **Real-World Applications**
   - Customer service bots (remember customer history)
   - Personal assistants (recall user preferences)
   - Educational tutors (track learning progress)
   - Game NPCs (remember player interactions)

3. **Scalability Considerations**
   - STM: O(1) access, limited by tokens
   - LTM: O(log n) search, scales with vector DB
   - Trade-off: Speed vs. capacity

4. **Future Enhancements**
   - Memory consolidation (STM → LTM)
   - Importance scoring
   - Memory decay/forgetting
   - Multi-modal memories (images, audio)
   - Knowledge graphs

## Q&A Preparation

**Q: Why not just use a large context window?**
A: Cost, latency, and relevance. LTM allows selective retrieval of only relevant information.

**Q: How do you decide what goes into LTM?**
A: Importance scoring based on user feedback, repetition, or explicit marking.

**Q: Can the agent forget?**
A: Yes, we can implement memory decay or explicit deletion for privacy/relevance.

**Q: How does this compare to RAG?**
A: Similar concept - LTM is essentially RAG over conversation history and persona knowledge.

## Demo Tips

1. Start with greeting to show persona
2. Ask about character background (triggers LTM)
3. Have a multi-turn conversation (shows STM)
4. Check stats periodically
5. Reset STM and show memory persistence
6. Ask similar questions to show consistent retrieval

## Contact & Resources

- GitHub: [Your Repo URL]
- Demo: ACD Ahmedabad 2026
- Tech Stack: Python, ChromaDB, Flask, Sentence Transformers
