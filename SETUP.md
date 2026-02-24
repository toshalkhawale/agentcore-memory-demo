# Setup Guide - Agentcore Memory Demo

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git
- 4GB RAM minimum (for embedding models)

## Installation Steps

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd agentcore-memory-demo
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- ChromaDB (vector database)
- Sentence Transformers (embeddings)
- LangChain (memory utilities)
- Other dependencies

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings (optional)
# Default values work fine for demo
```

### 5. Verify Installation

```bash
python -c "import chromadb; import sentence_transformers; print('✓ All dependencies installed')"
```

## Running the Demo

### Option 1: CLI Interface

```bash
python main.py
```

Features:
- Interactive command-line chat
- Type 'stats' to see memory statistics
- Type 'quit' to exit

### Option 2: Web Interface

```bash
python app.py
```

Then open browser to: http://localhost:5000

Features:
- Visual chat interface
- Real-time memory statistics
- Reset button for STM
- Responsive design

## Troubleshooting

### Issue: ChromaDB Error

```bash
# Clear existing database
rm -rf chroma_db/
# Restart application
```

### Issue: Embedding Model Download

First run downloads ~80MB model. Ensure internet connection.

```bash
# Pre-download model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### Issue: Port Already in Use

```bash
# Change port in .env
FLASK_PORT=5001
```

### Issue: Memory Errors

Reduce STM token limit in .env:
```bash
STM_MAX_TOKENS=1000
```

## Project Structure

```
agentcore-memory-demo/
├── core/
│   ├── __init__.py
│   ├── agent.py              # Main agent logic
│   ├── memory_manager.py     # Memory operations
│   └── knight_persona.py     # Character definition
├── templates/
│   └── index.html            # Web interface
├── chroma_db/                # Vector database (auto-created)
├── main.py                   # CLI entry point
├── app.py                    # Web entry point
├── requirements.txt          # Dependencies
├── .env.example              # Environment template
├── README.md                 # Project overview
├── DEMO-GUIDE.md            # Presentation guide
└── SETUP.md                 # This file
```

## Configuration Options

### .env Variables

```bash
# OpenAI (optional - for enhanced features)
OPENAI_API_KEY=sk-...

# Memory settings
STM_MAX_TOKENS=2000           # Short-term memory capacity
LTM_COLLECTION_NAME=knight_memories  # ChromaDB collection
EMBEDDING_MODEL=all-MiniLM-L6-v2     # Sentence transformer model

# Server settings
FLASK_PORT=5000
FLASK_DEBUG=True
```

## Testing the Setup

Run this test script:

```python
# test_setup.py
from core import MemoryManager, KnightAgent

print("Testing memory manager...")
memory = MemoryManager()
print("✓ Memory manager initialized")

print("Testing agent...")
agent = KnightAgent(memory)
print("✓ Agent initialized")

print("Testing conversation...")
response = agent.process_message("Who are you?")
print(f"✓ Response: {response[:50]}...")

print("\n✓ All tests passed!")
```

```bash
python test_setup.py
```

## Next Steps

1. Review DEMO-GUIDE.md for presentation scenarios
2. Explore the code in core/ directory
3. Customize knight_persona.py for different characters
4. Extend memory_manager.py with new features

## Support

For issues or questions:
- Check TROUBLESHOOTING section above
- Review code comments in core/ modules
- Contact: [Your contact info]

## License

MIT License - Free for educational and commercial use
