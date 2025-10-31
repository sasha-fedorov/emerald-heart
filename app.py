import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)

CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING')
client = MongoClient(CONNECTION_STRING)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    cmd = data.get('command', '').strip().lower()

    if cmd == 'hello':
        response = "Hello world!"
    elif cmd == 'ping':
        if client.db_name.command('ping'):
            response = "Database connected!"
        else:
            response = "Database not connected :("
    else:
        response = f"Unknown command: {cmd}"

    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
