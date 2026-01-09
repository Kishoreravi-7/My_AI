import os
from flask import Flask, render_template, request, jsonify
from lisa.ai_engine import LisaAI

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "lisa-secret-key")

lisa_sessions = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    if session_id not in lisa_sessions:
        lisa_sessions[session_id] = LisaAI()
    
    lisa = lisa_sessions[session_id]
    response = lisa.process_command(user_message)
    
    return jsonify({
        'response': response,
        'session_id': session_id
    })

@app.route('/api/clear', methods=['POST'])
def clear_context():
    data = request.get_json()
    session_id = data.get('session_id', 'default')
    
    if session_id in lisa_sessions:
        lisa_sessions[session_id].clear_context()
    
    return jsonify({'message': 'Conversation cleared'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)