# Agentcore Memory Demo - Presentation Guide
## ACD Ahmedabad 2026

## Overview
This demo showcases a dual-memory architecture for AI agents using the "Knight of the Seven Kingdoms" persona.

## Key Concepts

### 1. Short-Term Memory (STM)
- **Purpose**: Maintains recent conversation context
- **Implementation**: Sliding window buffer with token limits
- **Capacity**: 200 tokens (configurable via STM_MAX_TOKENS)
- **Behavior**: Automatically removes oldest messages when capacity reached
- **Use Case**: Keeps track of the immediate conversation flow, pronouns, and recent topics

**Example Flow:**
```
Message 1: "Who are you?" (15 tokens) → STM: 15/200
Message 2: "I am Ser Duncan..." (45 tokens) → STM: 60/200
Message 3: "Tell me about Egg" (20 tokens) → STM: 80/200
Message 4: "He is my squire..." (35 tokens) → STM: 115/200
Message 5: "What about honor?" (18 tokens) → STM: 133/200
Message 6: "Honor is everything..." (40 tokens) → STM: 173/200
Message 7: "Tell me more" (15 tokens) → STM: 188/200
Message 8: "A knight must..." (25 tokens) → STM: 213/200
→ Oldest message removed → STM: 198/200
```

### 2. Long-Term Memory (LTM)
- **Purpose**: Persistent knowledge storage and semantic retrieval
- **Implementation**: Vector database (FAISS) with semantic search
- **Storage**: Embeddings using Sentence Transformers (all-MiniLM-L6-v2)
- **Retrieval**: Similarity-based search for relevant memories
- **Persistence**: Saved to disk, survives application restarts
- **Initial Load**: 20 core memories about Ser Duncan's life and adventures

**Memory Categories:**
- `origin`: Backstory and how he became a knight
- `defining_moment`: Key events that shaped his character
- `relationships`: Important people in his life
- `values`: His beliefs and principles
- `identity`: Who he is and how he sees himself
- `possessions`: His belongings and their significance
- `personality`: His traits and characteristics

**Example LTM Entries:**
```
Memory 1: "I was knighted by Ser Arlan of Pennytree on his deathbed..."
  Category: origin
  Importance: 10
  Embedding: [0.234, -0.123, 0.456, ...]

Memory 2: "At the Tourney at Ashford Meadow, I defended Tanselle..."
  Category: defining_moment
  Importance: 10
  Embedding: [0.123, 0.234, -0.345, ...]
```

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

### Scenario 1: STM in Action - Conversation Continuity
**Goal**: Demonstrate how STM maintains recent context and handles overflow

**Step-by-Step:**
```
1. User: "Who are you?"
   → Agent: "I am Ser Duncan the Tall, a hedge knight..."
   → STM: 1 message (user) + 1 message (agent) ≈ 60 tokens
   → Stats: STM: 60/200 tokens, LTM: 20 memories

2. User: "What did you just tell me?"
   → Agent: References the introduction from STM
   → STM: 4 messages ≈ 120 tokens
   → Shows: Agent remembers recent conversation

3. User: "Tell me more about being a hedge knight"
   → Agent: Responds with details
   → STM: 6 messages ≈ 180 tokens
   → Shows: Approaching capacity

4. User: "Where do you travel?"
   → Agent: Responds about traveling the Seven Kingdoms
   → STM: 8 messages ≈ 220 tokens
   → Oldest messages start being removed
   → Shows: Automatic memory management (overflow!)

5. User: "What was the first thing I asked you?"
   → Agent: May not remember (removed from STM)
   → Shows: STM limitations - only ~3-4 exchanges fit in 200 tokens
   → Demonstrates why LTM is essential
```

**Key Observation**: With only 200 tokens, overflow happens quickly (after 3-4 exchanges). Type `stats` after each message to watch the dramatic overflow behavior!

### Scenario 2: LTM in Action - Knowledge Recall
**Goal**: Show LTM retrieving relevant memories based on semantic similarity

**Step-by-Step:**
```
1. User: "Tell me about honor and duty"
   → LTM Search: Finds memories about Trial of Seven, knightly values
   → Agent: "Aye, honor and duty are the foundation of knighthood..."
   → Shows: Semantic retrieval of relevant memories
   → Retrieved: "I believe a true knight must defend the helpless..."

2. User: "Who is your squire?"
   → LTM Search: Finds memories about Egg/Prince Aegon
   → Agent: "Ah, you speak of my squire, young Egg..."
   → Retrieved: "I met Prince Aegon Targaryen, who I knew as Egg..."

3. User: "Tell me about a battle"
   → LTM Search: Finds memories about Trial of Seven, Ashford
   → Agent: Describes the Trial of Seven
   → Retrieved: "I fought in a Trial of Seven at Ashford Meadow..."

4. User: "What happened to Prince Baelor?"
   → LTM Search: Finds specific memory about Baelor's death
   → Agent: "Prince Baelor Breakspear died saving my life..."
   → Shows: Precise memory retrieval
```

**Key Observation**: Same question asked in different sessions retrieves same memories (persistence)

### Scenario 3: Hybrid Memory - STM + LTM Working Together
**Goal**: Demonstrate how both memory systems complement each other

**Step-by-Step:**
```
1. User: "Tell me about your shield"
   → LTM: Retrieves memory about shield design
   → Agent: "My shield bears a falling star and elm tree..."
   → STM: Stores this exchange

2. User: "Who painted it?"
   → STM: Knows "it" refers to shield from previous message
   → LTM: Retrieves memory about Tanselle
   → Agent: "Tanselle Too-Tall painted it for me at Ashford..."
   → Shows: STM provides context, LTM provides knowledge

3. User: "Why did you defend her?"
   → STM: Knows "her" refers to Tanselle
   → LTM: Retrieves memory about defending Tanselle from Aerion
   → Agent: "Prince Aerion Brightflame was cruel to her..."
   → Shows: Perfect integration of both memory systems

4. User: "What was that prince's name again?"
   → STM: Recalls "Prince Aerion" from recent conversation
   → Agent: "Prince Aerion Brightflame"
   → Shows: STM handles immediate recall
```

**Key Observation**: STM handles pronouns and references, LTM provides detailed knowledge

### Scenario 4: Memory Overflow and Persistence
**Goal**: Show STM overflow behavior and LTM persistence

**Step-by-Step:**
```
1. Start fresh session
   → Check stats: STM: 0 messages, LTM: 20 memories

2. Have a conversation (just 4-5 exchanges needed!)
   → Watch STM grow: 60 → 120 → 180 → 220 tokens
   → Observe: Oldest messages being removed at 200+ tokens
   → With 200 tokens, overflow happens VERY quickly

3. Ask about something from early in conversation
   → Agent may not remember (removed from STM after just 3-4 turns)
   → Shows: Severe STM limitations with small buffer

4. Exit and restart the application
   → STM: Reset to 0
   → LTM: Still has 20 memories

5. Ask same questions about Ser Duncan's past
   → Agent still remembers everything from LTM
   → Shows: LTM persistence across sessions
```

**Key Observation**: With 200 tokens, you can only keep ~3-4 conversation turns in memory. This dramatically shows why LTM is critical!

### Scenario 5: Semantic Search Demonstration
**Goal**: Show how LTM finds relevant memories even with different wording

**Step-by-Step:**
```
1. User: "What's your background?"
   → LTM finds: origin memories about Flea Bottom, Ser Arlan
   
2. User: "Where did you come from?"
   → LTM finds: Same origin memories (semantic similarity)
   
3. User: "Tell me about your childhood"
   → LTM finds: Same memories again
   → Shows: Different questions, same semantic meaning

4. User: "Who taught you to fight?"
   → LTM finds: Memories about Ser Arlan training him

5. User: "Who was your mentor?"
   → LTM finds: Same Ser Arlan memories
   → Shows: Semantic understanding, not keyword matching
```

**Key Observation**: LTM understands meaning, not just exact words

## Technical Architecture

```
┌─────────────────────────────────────────┐
│         User Interface (CLI/Web)        │
│  - Input: User messages                 │
│  - Output: Agent responses + stats      │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│         Knight Agent                    │
│  1. Receive user message                │
│  2. Add to STM                          │
│  3. Query LTM for relevant memories     │
│  4. Build context (STM + LTM)           │
│  5. Generate response                   │
│  6. Add response to STM                 │
└────────┬───────────────────┬────────────┘
         │                   │
┌────────▼────────┐  ┌──────▼─────────────┐
│  Memory Manager │  │  Persona Config    │
│                 │  │                    │
│  STM (200 tok)  │  │  - Character data  │
│  ┌───────────┐  │  │  - 20 core mems    │
│  │ Msg 1     │  │  │  - Speaking style  │
│  │ Msg 2     │  │  │  - Backstory       │
│  │ Msg 3     │  │  └────────────────────┘
│  │ (3-4 max) │  │
│  │ Msg N     │  │
│  └───────────┘  │
│                 │
│  LTM (FAISS)    │
│  ┌───────────┐  │
│  │ Memory 1  │  │  ← Embeddings
│  │ Memory 2  │  │  ← Semantic search
│  │ ...       │  │  ← Persistent storage
│  │ Memory 20 │  │
│  └───────────┘  │
└────────┬────────┘
         │
┌────────▼────────────────────────────────┐
│         Storage Layer                   │
│  - FAISS Index (Vector DB)              │
│  - Metadata (Pickle files)              │
│  - Sentence Transformers (Embeddings)   │
│    Model: all-MiniLM-L6-v2              │
│    Dimension: 384                       │
└─────────────────────────────────────────┘

Memory Flow:
═══════════

User Message → STM → LTM Query → Context Building → Response
     ↓           ↓        ↓              ↓              ↓
  Tokenize   Add to   Embed &      Combine STM    Generate
             buffer   Search       + LTM results   & Store
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

### Preparation
1. Ensure `.env` file is configured (copy from `.env.example`)
2. Set `STM_MAX_TOKENS=200` for dramatic overflow demonstration
3. Have the application running before presentation
4. Open two terminals: one for app, one for monitoring
5. **Important**: With 200 tokens, overflow happens after just 3-4 exchanges - perfect for demos!

### Presentation Flow

**Phase 1: Introduction (2 minutes)**
1. Start with greeting: "Who are you?"
2. Show persona response with character details
3. Explain the Knight of Seven Kingdoms theme

**Phase 2: STM Demonstration (3 minutes)**
1. Have a natural conversation (3-4 exchanges only!)
2. Type `stats` after each message
3. Point out STM token count increasing rapidly
4. Continue until STM overflows (>200 tokens - happens fast!)
5. Show oldest messages being removed after just 3-4 turns
6. Ask about first question - agent won't remember (dramatic!)
7. Emphasize: "With only 200 tokens, we can barely keep 3-4 exchanges!"

**Phase 3: LTM Demonstration (3 minutes)**
1. Ask about character background: "Tell me about Ser Arlan"
2. Show how LTM retrieves relevant memories
3. Ask similar question differently: "Who was your mentor?"
4. Show same memories retrieved (semantic search)
5. Type `stats` to show LTM count (25 memories)

**Phase 4: Hybrid Memory (3 minutes)**
1. Ask: "Tell me about your shield"
2. Follow up: "Who painted it?" (pronoun from STM)
3. Follow up: "Why did you defend her?" (context from STM + LTM)
4. Show how both systems work together

**Phase 5: Persistence (2 minutes)**
1. Exit the application
2. Restart it
3. Show STM reset to 0
4. Ask same questions - LTM still remembers
5. Demonstrate persistence across sessions

### Key Points to Emphasize

**STM Benefits:**
- ✅ Fast access (O(1))
- ✅ Maintains conversation flow
- ✅ Handles pronouns and references
- ❌ Very limited capacity (200 tokens = ~3-4 exchanges)
- ❌ Loses old context quickly

**LTM Benefits:**
- ✅ Unlimited capacity (scales with disk)
- ✅ Semantic search (understands meaning)
- ✅ Persistent across sessions
- ✅ Organized by categories
- ❌ Slower than STM (embedding + search)

**Hybrid Approach:**
- ✅ Best of both worlds
- ✅ STM for immediate context
- ✅ LTM for knowledge retrieval
- ✅ Realistic conversation experience

### Common Questions & Answers

**Q: Why only 200 tokens for STM?**
A: This is intentionally small for demonstration purposes! It makes overflow behavior very visible - you can see memory management in action after just 3-4 exchanges. In production, you'd use 2000-4000 tokens depending on use case. The small size dramatically shows why LTM is essential.

**Q: How many conversation turns fit in 200 tokens?**
A: Approximately 3-4 exchanges (user message + agent response). Each exchange averages 50-70 tokens, so 200 tokens fills up very quickly!

**Q: How does semantic search work?**
A: User query → Embedding (384-dim vector) → Cosine similarity with stored embeddings → Top-K results

**Q: What if STM and LTM conflict?**
A: STM takes precedence for immediate context. LTM provides background knowledge.

**Q: Can you add new memories to LTM?**
A: Yes! Important conversations can be promoted from STM to LTM with importance scoring.

**Q: How much does this cost?**
A: Embeddings are local (free). Only cost is storage (minimal) and compute (negligible for small scale).

### Troubleshooting

**Issue**: Agent responses are generic
- **Fix**: Check that LTM loaded properly (should have 20 memories)
- **Command**: Type `stats` to verify

**Issue**: STM not overflowing
- **Fix**: With 200 tokens, this shouldn't happen! Just 3-4 exchanges should trigger overflow
- **Check**: Verify STM_MAX_TOKENS=200 in .env file

**Issue**: Same memories retrieved every time
- **Fix**: This is correct! Shows consistency and reliability

### Advanced Demonstrations

**Memory Categories:**
```bash
# Show different memory types
"Tell me about your origin"     → origin memories
"What defines you?"             → defining_moment memories  
"Who do you know?"              → relationships memories
"What do you believe?"          → values memories
```

**Token Counting:**
```bash
# Show token efficiency
Short message: "Hi" → ~5 tokens
Medium message: "Tell me about honor" → ~20 tokens
Long response: Full paragraph → ~100-150 tokens
```

**Semantic Similarity:**
```bash
# Same meaning, different words
"Who taught you?" 
"Who was your teacher?"
"Who trained you?"
→ All retrieve Ser Arlan memories
```

## Contact & Resources

- GitHub: [Your Repo URL]
- Demo: ACD Ahmedabad 2026
- Tech Stack: Python, ChromaDB, Flask, Sentence Transformers
