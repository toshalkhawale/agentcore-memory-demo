# Agentcore Memory Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│  ┌──────────────────────┐      ┌──────────────────────┐        │
│  │   CLI Interface      │      │   Web Interface      │        │
│  │   (main.py)          │      │   (app.py + HTML)    │        │
│  │                      │      │                      │        │
│  │  • Interactive chat  │      │  • Visual UI         │        │
│  │  • Stats command     │      │  • Real-time stats   │        │
│  │  • Simple I/O        │      │  • Reset button      │        │
│  └──────────┬───────────┘      └──────────┬───────────┘        │
└─────────────┼──────────────────────────────┼────────────────────┘
              │                              │
              └──────────────┬───────────────┘
                             │
┌─────────────────────────────▼───────────────────────────────────┐
│                      AGENT CORE                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              KnightAgent (agent.py)                      │  │
│  │                                                          │  │
│  │  1. Receive user message                                │  │
│  │  2. Add to STM                                          │  │
│  │  3. Query LTM for relevant memories                     │  │
│  │  4. Build context (STM + LTM)                           │  │
│  │  5. Generate response                                   │  │
│  │  6. Return response + stats                             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                   │
│              ┌──────────────┴──────────────┐                   │
│              │                             │                   │
│  ┌───────────▼──────────┐    ┌────────────▼──────────┐        │
│  │  Persona Config      │    │  Memory Manager       │        │
│  │  (knight_persona.py) │    │  (memory_manager.py)  │        │
│  │                      │    │                       │        │
│  │  • Character data    │    │  • STM operations     │        │
│  │  • Core memories     │    │  • LTM operations     │        │
│  │  • Speaking style    │    │  • Retrieval logic    │        │
│  │  • System prompt     │    │  • Statistics         │        │
│  └──────────────────────┘    └────────────┬──────────┘        │
└──────────────────────────────────────────────┼──────────────────┘
                                              │
┌─────────────────────────────────────────────▼──────────────────┐
│                      MEMORY LAYER                              │
│                                                                │
│  ┌──────────────────────┐      ┌──────────────────────┐      │
│  │  Short-Term Memory   │      │  Long-Term Memory    │      │
│  │  (STM)               │      │  (LTM)               │      │
│  │                      │      │                      │      │
│  │  Implementation:     │      │  Implementation:     │      │
│  │  • Python list       │      │  • ChromaDB          │      │
│  │  • Token-limited     │      │  • Vector database   │      │
│  │  • FIFO buffer       │      │  • Persistent        │      │
│  │                      │      │                      │      │
│  │  Capacity:           │      │  Capacity:           │      │
│  │  • 2000 tokens       │      │  • Unlimited         │      │
│  │  • ~10-20 messages   │      │  • Millions of docs  │      │
│  │                      │      │                      │      │
│  │  Access:             │      │  Access:             │      │
│  │  • O(1) read         │      │  • O(log n) search   │      │
│  │  • Instant           │      │  • ~50ms             │      │
│  └──────────────────────┘      └──────────┬───────────┘      │
│                                            │                  │
│                                ┌───────────▼───────────┐      │
│                                │  Sentence Transformers│      │
│                                │  (Embeddings)         │      │
│                                │                       │      │
│                                │  • all-MiniLM-L6-v2   │      │
│                                │  • 384 dimensions     │      │
│                                │  • Semantic search    │      │
│                                └───────────────────────┘      │
└────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Message Processing Flow

```
User Input
    │
    ▼
┌───────────────────┐
│ 1. Add to STM     │
│    • Store message│
│    • Manage size  │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ 2. Query LTM      │
│    • Embed query  │
│    • Search DB    │
│    • Get top-K    │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ 3. Build Context  │
│    • System prompt│
│    • LTM memories │
│    • STM messages │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ 4. Generate       │
│    Response       │
│    • Process      │
│    • Format       │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ 5. Store Response │
│    • Add to STM   │
│    • Update stats │
└────────┬──────────┘
         │
         ▼
    User Output
```

## Memory Retrieval Strategy

### Short-Term Memory (Recency-Based)

```
Recent Messages Buffer
┌─────────────────────────────────┐
│ [0] System: You are Ser Duncan  │  ← Oldest
│ [1] User: Who are you?          │
│ [2] Agent: I am Ser Duncan...   │
│ [3] User: Tell me more          │
│ [4] Agent: I come from...       │  ← Newest
└─────────────────────────────────┘
         │
         ▼
When capacity reached:
Remove [0], shift all up
```

### Long-Term Memory (Relevance-Based)

```
User Query: "Tell me about honor"
         │
         ▼
┌─────────────────────────────────┐
│ Embed Query                     │
│ [0.12, -0.45, 0.78, ...]        │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ Vector Database Search          │
│ • Cosine similarity             │
│ • Top-K results                 │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ Retrieved Memories              │
│ 1. Trial of Seven (0.89)        │
│ 2. Knightly values (0.85)       │
│ 3. Defending helpless (0.82)    │
└─────────────────────────────────┘
```

### Hybrid Approach

```
User Message
     │
     ├─────────────┬─────────────┐
     │             │             │
     ▼             ▼             ▼
  Add to      Query LTM    Get Persona
   STM       (semantic)      Config
     │             │             │
     └──────┬──────┴─────────────┘
            │
            ▼
    Combine All Context
            │
            ▼
    Generate Response
```

## Component Interactions

### Initialization Flow

```
1. Load Environment Variables
         │
         ▼
2. Initialize Memory Manager
   ├─ Create STM buffer
   └─ Connect to ChromaDB
         │
         ▼
3. Initialize Agent
   ├─ Load persona config
   ├─ Generate system prompt
   └─ Load core memories to LTM
         │
         ▼
4. Start Interface (CLI/Web)
```

### Memory Consolidation (Future)

```
STM Message
     │
     ▼
Check Importance
     │
     ├─ High (≥7) ──────┐
     │                  │
     └─ Low (<7)        │
        │               │
        ▼               ▼
    Discard      Store in LTM
                       │
                       ▼
                 Persist to DB
```

## Technology Stack Layers

```
┌─────────────────────────────────────┐
│         Application Layer           │
│  • Flask (Web)                      │
│  • CLI (Terminal)                   │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│         Business Logic              │
│  • Agent (agent.py)                 │
│  • Memory Manager                   │
│  • Persona Config                   │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│         Data Layer                  │
│  • ChromaDB (Vector DB)             │
│  • Python Lists (STM)               │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│         Infrastructure              │
│  • Sentence Transformers            │
│  • tiktoken (Token counting)        │
│  • Python 3.9+                      │
└─────────────────────────────────────┘
```

## Scalability Architecture

### Horizontal Scaling

```
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Agent 1  │  │ Agent 2  │  │ Agent 3  │
│ Instance │  │ Instance │  │ Instance │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     └─────────────┼─────────────┘
                   │
         ┌─────────▼─────────┐
         │  Shared ChromaDB  │
         │  (Centralized)    │
         └───────────────────┘
```

### Vertical Scaling

```
Small Deployment:
• 2GB RAM
• 1 CPU core
• 1000 memories

Medium Deployment:
• 8GB RAM
• 4 CPU cores
• 100K memories

Large Deployment:
• 32GB RAM
• 16 CPU cores
• 1M+ memories
```

## Performance Characteristics

```
Operation          | Time Complexity | Actual Time
-------------------|-----------------|-------------
STM Add            | O(1)            | <1ms
STM Read           | O(n)            | <1ms
STM Remove         | O(n)            | <1ms
LTM Add            | O(log n)        | ~10ms
LTM Search         | O(log n)        | ~50ms
Embedding Gen      | O(m)            | ~100ms
Full Pipeline      | O(log n + m)    | ~200ms

n = number of memories
m = text length
```

## Security Considerations

```
┌─────────────────────────────────────┐
│         Input Validation            │
│  • Sanitize user input              │
│  • Rate limiting                    │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│         Data Privacy                │
│  • No PII in logs                   │
│  • Memory encryption (optional)     │
│  • User data isolation              │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│         Access Control              │
│  • API authentication               │
│  • Memory access permissions        │
└─────────────────────────────────────┘
```

---

**Architecture designed for ACD Ahmedabad 2026 demonstration**
