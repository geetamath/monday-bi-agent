from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from groq import Groq
from monday_client import MondayClient
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize clients
monday_client = MondayClient()
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Simple HTML UI
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Monday.com BI Agent</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 50px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        .input-group {
            margin: 20px 0;
        }
        input[type="text"] {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 8px;
            box-sizing: border-box;
            transition: border 0.3s;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 10px;
            font-weight: bold;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        button:active {
            transform: translateY(0);
        }
        #response {
            margin-top: 20px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
            white-space: pre-wrap;
            display: none;
            line-height: 1.6;
            border-left: 4px solid #667eea;
        }
        .loading {
            text-align: center;
            color: #667eea;
            display: none;
            margin-top: 20px;
        }
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .example {
            font-size: 13px;
            color: #888;
            margin-top: 8px;
            font-style: italic;
        }
        .examples-section {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .examples-section h3 {
            margin-top: 0;
            color: #333;
            font-size: 14px;
        }
        .examples-section ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        .examples-section li {
            color: #666;
            font-size: 13px;
            margin: 5px 0;
            cursor: pointer;
        }
        .examples-section li:hover {
            color: #667eea;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Monday.com BI Agent</h1>
        <p class="subtitle">AI-powered business intelligence for your Work Orders & Deals</p>
        
        <div class="examples-section">
            <h3>💡 Try asking:</h3>
            <ul>
                <li onclick="fillQuery(this)">How's our pipeline looking for energy sector this quarter?</li>
                <li onclick="fillQuery(this)">What's our total revenue from closed deals?</li>
                <li onclick="fillQuery(this)">Show me work orders by status</li>
                <li onclick="fillQuery(this)">Which sectors are performing best?</li>
                <li onclick="fillQuery(this)">Summarize key metrics for leadership update</li>
            </ul>
        </div>
        
        <div class="input-group">
            <input type="text" id="query" placeholder="Ask a business question..." />
            <div class="example">Natural language queries work best!</div>
        </div>
        
        <button onclick="askQuestion()">🚀 Analyze</button>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Analyzing your data with AI...</p>
        </div>
        <div id="response"></div>
    </div>

    <script>
        function fillQuery(element) {
            document.getElementById('query').value = element.textContent;
        }
        
        async function askQuestion() {
            const query = document.getElementById('query').value;
            const responseDiv = document.getElementById('response');
            const loadingDiv = document.getElementById('loading');
            
            if (!query) {
                alert('Please enter a question');
                return;
            }
            
            responseDiv.style.display = 'none';
            loadingDiv.style.display = 'block';
            
            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: query })
                });
                
                const data = await response.json();
                
                loadingDiv.style.display = 'none';
                responseDiv.style.display = 'block';
                
                if (data.error) {
                    responseDiv.textContent = '❌ Error: ' + data.error;
                } else {
                    responseDiv.textContent = data.response;
                }
            } catch (error) {
                loadingDiv.style.display = 'none';
                responseDiv.style.display = 'block';
                responseDiv.textContent = '❌ Error: ' + error.message;
            }
        }
        
        document.getElementById('query').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                askQuestion();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get-boards', methods=['GET'])
def get_boards():
    """Helper endpoint to see all boards"""
    try:
        boards = monday_client.get_all_boards()
        return jsonify(boards)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.json
        user_query = data.get('query', '')
        
        if not user_query:
            return jsonify({"error": "No query provided"}), 400
        
        # Fetch data from Monday.com
        monday_data = monday_client.get_all_boards_data()
        
        if "error" in monday_data:
            return jsonify({"error": monday_data["error"]}), 500
        
        # Prepare context for Groq
        context = f"""You are a business intelligence analyst examining Monday.com data.

You have access to two boards:
1. Work Orders - Project execution data
2. Deals - Sales pipeline data

The data contains real-world messiness: missing values, inconsistent formats, incomplete records.

Here's the data:
{json.dumps(monday_data, indent=2)}

User Question: {user_query}

Provide a clear, insightful business intelligence answer. Handle data quality issues gracefully and mention any caveats. Focus on actionable insights that would help executives make decisions.

If the question asks for leadership updates or summaries, provide:
- Key metrics and trends
- Notable insights or concerns
- Actionable recommendations
"""
        
        # Call Groq API
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a business intelligence expert who provides clear, data-driven insights from Monday.com boards."
                },
                {
                    "role": "user",
                    "content": context
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1500
        )
        
        response_text = chat_completion.choices[0].message.content
        
        return jsonify({"response": response_text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Show available boards on startup
    print("\n" + "="*50)
    print("MONDAY.COM BI AGENT STARTING")
    print("="*50)
    try:
        boards = monday_client.get_all_boards()
        print("\nAvailable boards:")
        if 'data' in boards and 'boards' in boards['data']:
            for board in boards['data']['boards']:
                print(f"  - {board['name']}: {board['id']}")
        print("\nAdd these IDs to your .env file!")
    except Exception as e:
        print(f"Could not fetch boards: {e}")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)