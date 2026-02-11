from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from anthropic import Anthropic
from monday_client import MondayClient
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize clients
monday_client = MondayClient()
anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Simple HTML UI
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Monday.com BI Agent</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .input-group {
            margin: 20px 0;
        }
        input[type="text"] {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            background: #0073ea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
        }
        button:hover {
            background: #0060c0;
        }
        #response {
            margin-top: 20px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 5px;
            white-space: pre-wrap;
            display: none;
        }
        .loading {
            text-align: center;
            color: #666;
            display: none;
        }
        .example {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Monday.com BI Agent</h1>
        <p style="text-align: center; color: #666;">Ask business intelligence questions about your work orders and deals</p>
        
        <div class="input-group">
            <input type="text" id="query" placeholder="Ask a business question..." />
            <div class="example">Example: "What's our pipeline for energy sector this quarter?"</div>
        </div>
        
        <button onclick="askQuestion()">Ask Question</button>
        
        <div class="loading" id="loading">Analyzing data...</div>
        <div id="response"></div>
    </div>

    <script>
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
                responseDiv.textContent = data.response;
            } catch (error) {
                loadingDiv.style.display = 'none';
                responseDiv.style.display = 'block';
                responseDiv.textContent = 'Error: ' + error.message;
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

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.json
        user_query = data.get('query', '')
        
        if not user_query:
            return jsonify({"error": "No query provided"}), 400
        
        # Fetch data from Monday.com
        monday_data = monday_client.get_all_boards_data()
        
        # Prepare context for Claude
        context = f"""
You are a business intelligence agent analyzing data from Monday.com boards.

You have access to two boards:
1. Work Orders - Project execution data
2. Deals - Sales pipeline data

The data is messy and real-world. Handle missing values, inconsistent formats gracefully.

Here's the data:
{json.dumps(monday_data, indent=2)}

User Question: {user_query}

Provide a clear, insightful answer. If data is missing or unclear, mention it. Focus on actionable insights.
"""
        
        # Call Claude
        message = anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": context}
            ]
        )
        
        response_text = message.content[0].text
        
        return jsonify({"response": response_text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

## **File 4: `requirements.txt`**
```
flask==3.0.0
anthropic==0.18.1
requests==2.31.0
flask-cors==4.0.0
python-dotenv==1.0.0