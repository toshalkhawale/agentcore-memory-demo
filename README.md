# Agentcore Memory Retrieval Demo
## Knight of the Seven Kingdoms Persona

**Prepared for: ACD Ahmedabad 2026**

This demo showcases advanced memory retrieval strategies for AI agents, featuring:
- **Short-term Memory**: Conversation context and recent interactions
- **Long-term Memory**: Persistent knowledge storage and retrieval
- **Persona**: Knight of the Seven Kingdoms character with rich backstory

## Architecture

```
┌─────────────────────────────────────────┐
│         Agent Interface                 │
├─────────────────────────────────────────┤
│  Short-term Memory (STM)                │
│  - Conversation buffer                  │
│  - Recent context (sliding window)      │
│  - Working memory                       │
├─────────────────────────────────────────┤
│  Long-term Memory (LTM)                 │
│  - Vector database (embeddings)         │
│  - Semantic search                      │
│  - Knowledge graphs                     │
├─────────────────────────────────────────┤
│  Memory Retrieval Strategy              │
│  - Recency-based retrieval              │
│  - Relevance-based retrieval            │
│  - Hybrid approach                      │
└─────────────────────────────────────────┘
```

## Features

1. **Dual Memory System**: Implements both STM and LTM
2. **Semantic Search**: Vector-based similarity search for relevant memories
3. **Context Management**: Intelligent context window management
4. **Persona Consistency**: Maintains character traits across conversations
5. **Memory Consolidation**: Moves important STM to LTM

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the demo
python main.py

# Run with web interface
python app.py
```

## Tech Stack

- Python 3.9+
- ChromaDB (Vector database)
- Sentence Transformers (Embeddings)
- Flask (Web interface)
- LangChain (Memory management)

## Demo Scenarios

1. **Conversation Continuity**: Agent remembers recent dialogue
2. **Knowledge Recall**: Retrieves relevant lore from long-term memory
3. **Character Consistency**: Maintains persona across sessions
4. **Memory Prioritization**: Important events stored permanently

## License

MIT License - Created for ACD Ahmedabad 2026
