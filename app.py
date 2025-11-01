import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)

CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING')
client = MongoClient(CONNECTION_STRING)
db = client["emerald-heart"]
sessions = db["sessions"]
users = db["users"]


@app.route('/')
def index():
    """ Returns page to show """
    return render_template('index.html')


@app.route('/action', methods=['POST'])
def action():
    """
    Event handler from user

    Returns result from action as:
        response:    next text to display
        next_action: next action to do
        error:       error message when occured
    """

    data = request.get_json()

    action = data.get('action', '').strip().lower()
    input = data.get('input', '').strip().lower()

    result = {
        "response": "",
        "next_action": action,
        "error": ""
    }

    try:
        match action:
            case "init":
                result["response"] = "Login or create an account: \n 1. Login \n 2. Create an account"
                result["next_action"] = "login_or_registration"

            case "login_or_registration":
                try:
                    selection = int(input)
                    match selection:
                        case 1:
                            result["response"] = "Enter username:"
                            result["next_action"] = "registration_password"
                        case 2:
                            result["response"] = "Enter username:"
                            result["next_action"] = "login_password"
                        case _: raise Exception
                except Exception:
                    result["error"] = f"Invalid input: {input}. Please try again"

            case _:
                result["error"] = "Unexpected error occurs, please try again"
                result["next_action"] = "init"

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f"Unexpected error: {e}, please try again",
                        'next_action': 'init'})


# result["response"] = ""
# result["next_action"] = ""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
