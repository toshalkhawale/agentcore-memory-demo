# Agentcore Memory Retrieval Demo
## Presentation Slides - ACD Ahmedabad 2026

---

## Slide 1: Title
**Agentcore Memory Retrieval Strategies**
**Short-Term & Long-Term Memory for AI Agents**

Presented at: ACD Ahmedabad 2026
Demo: Knight of the Seven Kingdoms Persona

---

## Slide 2: The Memory Challenge

**Problem**: AI agents need to remember context

- Conversations span multiple turns
- Users reference past interactions
- Agents need consistent personality
- Context windows have limits

**Solution**: Dual memory architecture

---

## Slide 3: Human Memory Analogy

**Short-Term Memory (Working Memory)**
- What you're thinking about right now
- Limited capacity (~7 items)
- Quickly accessible
- Temporary

**Long-Term Memory (Knowledge Base)**
- Everything you've learned
- Unlimited capacity
- Requires retrieval
- Persistent

---

## Slide 4: Architecture Overview

```
┌─────────────────────────────────────────┐
│         User Interface                  │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│         Agent Core                      │
│  • Process input                        │
│  • Retrieve memories                    │
│  • Generate response                    │
└────────┬───────────────────┬────────────┘
         │                   │
┌────────▼────────┐  ┌──────▼─────────────┐
│  Short-Term     │  │  Long-Term         │
│  Memory (STM)   │  │  Memory (LTM)      │
│  • Buffer       │  │  • Vector DB       │
│  • Recent msgs  │  │  • Embeddings      │
│  • Fast access  │  │  • Semantic search │
└─────────────────┘  └────────────────────┘
```

---

## Slide 5: Short-Term Memory (STM)

**Implementation**: Sliding window buffer

**Characteristics**:
- Stores recent conversation turns
- Token-limited (e.g., 2000 tokens)
- FIFO removal when full
- O(1) access time

**Use Cases**:
- Maintaining conversation flow
- Pronoun resolution ("it", "that")
- Immediate context

---

## Slide 6: Long-Term Memory (LTM)

**Implementation**: Vector database (ChromaDB)

**Characteristics**:
- Stores embeddings of memories
- Semantic similarity search
- Persistent across sessions
- O(log n) retrieval

**Use Cases**:
- Character backstory
- User preferences
- Historical interactions
- Domain knowledge

---

## Slide 7: Memory Retrieval Strategy

**Step 1**: User sends message
**Step 2**: Add to STM
**Step 3**: Query LTM for relevant memories
**Step 4**: Combine STM + LTM → Context
**Step 5**: Generate response
**Step 6**: Store important info in LTM

**Key Insight**: Hybrid approach gets best of both worlds

---

## Slide 8: Demo Persona

**Ser Duncan the Tall**
- Knight of the Seven Kingdoms
- From humble origins (Flea Bottom)
- Values: Honor, loyalty, justice
- Companion: Egg (his squire)

**Why this persona?**
- Rich backstory (LTM)
- Consistent character traits
- Clear speaking style
- Memorable interactions

---

## Slide 9: Live Demo - Scenario 1

**Conversation Continuity**

```
User: "Who are you?"
Agent: "I am Ser Duncan the Tall..."

User: "What did you just tell me?"
Agent: [References previous response from STM]
```

**Demonstrates**: STM maintaining recent context

---

## Slide 10: Live Demo - Scenario 2

**Knowledge Recall**

```
User: "Tell me about honor"
Agent: [Retrieves memories about Trial of Seven]

User: "Who is your squire?"
Agent: [Retrieves memories about Egg/Prince Aegon]
```

**Demonstrates**: LTM semantic search

---

## Slide 11: Live Demo - Scenario 3

**Memory Management**

- Start with empty STM
- Send multiple messages
- Watch STM fill up
- Observe oldest messages removed
- LTM remains persistent

**Demonstrates**: Capacity management

---

## Slide 12: Technical Stack

**Backend**:
- Python 3.9+
- ChromaDB (vector database)
- Sentence Transformers (embeddings)
- LangChain (memory utilities)

**Frontend**:
- Flask (web framework)
- Vanilla JavaScript
- Responsive CSS

**Why these choices?**
- Open source
- Easy to deploy
- Production-ready
- Well-documented

---

## Slide 13: Key Metrics

**Memory Statistics**:
- STM messages count
- STM token usage
- LTM memory count
- Retrieval latency

**Performance**:
- STM access: <1ms
- LTM retrieval: ~50ms
- Embedding generation: ~100ms

---

## Slide 14: Real-World Applications

**Customer Service**:
- Remember customer history
- Personalized responses
- Issue tracking

**Personal Assistants**:
- User preferences
- Routine patterns
- Long-term goals

**Education**:
- Student progress
- Learning style
- Knowledge gaps

**Gaming**:
- NPC memory
- Player relationships
- World state

---

## Slide 15: Challenges & Solutions

**Challenge 1**: What to store in LTM?
**Solution**: Importance scoring, user feedback

**Challenge 2**: Retrieval relevance
**Solution**: Better embeddings, hybrid search

**Challenge 3**: Memory conflicts
**Solution**: Timestamps, versioning

**Challenge 4**: Privacy concerns
**Solution**: Encryption, user control, deletion

---

## Slide 16: Future Enhancements

**Memory Consolidation**:
- Automatic STM → LTM transfer
- Importance-based filtering

**Advanced Retrieval**:
- Knowledge graphs
- Multi-hop reasoning
- Temporal awareness

**Multi-Modal**:
- Image memories
- Audio context
- Video understanding

---

## Slide 17: Comparison with Alternatives

**Large Context Windows**:
- ✓ Simple
- ✗ Expensive
- ✗ Slow
- ✗ No selectivity

**RAG (Retrieval Augmented Generation)**:
- ✓ Selective retrieval
- ✓ Scalable
- ✗ No conversation memory
- ✗ Single-shot

**Our Approach (Dual Memory)**:
- ✓ Conversation + knowledge
- ✓ Fast + scalable
- ✓ Cost-effective
- ✓ Flexible

---

## Slide 18: Code Walkthrough

**Core Components**:

1. `memory_manager.py` - Memory operations
2. `knight_persona.py` - Character definition
3. `agent.py` - Main agent logic
4. `main.py` / `app.py` - Interfaces

**Key Functions**:
- `add_to_stm()` - Store recent message
- `retrieve_from_ltm()` - Semantic search
- `process_message()` - Main loop

---

## Slide 19: Deployment Considerations

**Scalability**:
- Horizontal: Multiple agent instances
- Vertical: Larger vector DB

**Monitoring**:
- Memory usage metrics
- Retrieval latency
- User satisfaction

**Costs**:
- Embedding API calls
- Vector DB storage
- Compute resources

---

## Slide 20: Q&A

**Common Questions**:

Q: Why not just use GPT-4 with 128k context?
A: Cost, latency, and selective retrieval

Q: How do you handle memory conflicts?
A: Timestamps and importance scoring

Q: Can users delete their memories?
A: Yes, privacy controls included

Q: How does this scale?
A: Vector DBs scale to millions of memories

---

## Slide 21: Try It Yourself

**GitHub Repository**:
[Your Repo URL]

**Quick Start**:
```bash
git clone <repo>
cd agentcore-memory-demo
pip install -r requirements.txt
python main.py
```

**Web Interface**:
```bash
python app.py
# Open http://localhost:5000
```

---

## Slide 22: Thank You

**Agentcore Memory Demo**
ACD Ahmedabad 2026

**Contact**:
- GitHub: [Your GitHub]
- Email: [Your Email]
- LinkedIn: [Your LinkedIn]

**Resources**:
- Demo code: [Repo URL]
- Documentation: README.md
- Presentation: PRESENTATION.md

---

## Appendix: Additional Resources

**Papers**:
- "Memory Networks" (Weston et al.)
- "Neural Turing Machines" (Graves et al.)
- "Retrieval-Augmented Generation" (Lewis et al.)

**Tools**:
- ChromaDB: https://www.trychroma.com/
- LangChain: https://langchain.com/
- Sentence Transformers: https://www.sbert.net/

**Related Work**:
- MemGPT
- AutoGPT memory systems
- LangChain memory modules
