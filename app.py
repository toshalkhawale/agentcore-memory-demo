"""
Flask Web Interface for Agentcore Memory Demo
"""

import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from core import MemoryManager, KnightAgent

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize memory and agent
memory_manager = MemoryManager(
    stm_max_tokens=int(os.getenv("STM_MAX_TOKENS", 200)),
    collection_name=os.getenv("LTM_COLLECTION_NAME", "knight_memories")
)
agent = KnightAgent(memory_manager)


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Process message
        response = agent.process_message(user_message)
        
        # Get memory stats
        stats = agent.get_memory_stats()
        
        return jsonify({
            'response': response,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/greeting', methods=['GET'])
def greeting():
    """Get initial greeting"""
    return jsonify({
        'greeting': agent.get_greeting(),
        'stats': agent.get_memory_stats()
    })


@app.route('/api/stats', methods=['GET'])
def stats():
    """Get memory statistics"""
    return jsonify(agent.get_memory_stats())


@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset short-term memory"""
    agent.memory.clear_stm()
    return jsonify({
        'message': 'Short-term memory cleared',
        'stats': agent.get_memory_stats()
    })


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║     AGENTCORE MEMORY DEMO - WEB INTERFACE                 ║
║     Knight of the Seven Kingdoms                          ║
║     ACD Ahmedabad 2026                                    ║
╚═══════════════════════════════════════════════════════════╝

Server running at: http://localhost:{port}
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
