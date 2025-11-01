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


class User:
    """
    A class to represent a user.

    Attributes:
    ----------
    name : str
        The name of the user.
    password : str
        The user's password.
    """

    def __init__(self, name: str, password: str):
        """
        Initializes a new User instance.

        Parameters:
        ----------
        name : str
            The name of the user.
        password : str
            The user's password.
        session_id : str
            The user current session ID.
        """
        self._id = name
        self.password = password

    def create_user(self):
        """ Create a user entry """
        user = users.find_one({"_id": self._id})
        if (user):
            raise KeyError()
        else:
            users.insert_one({"_id": self._id, "password": self.password})

        return self


def create_user(name: str, password: str):
    """
    Create a user entry

    Parameters:
    ----------
    name : str
        The name of the user.
    password : str
        The user's password.

    Returns:
    ----------
    Created entry.
    """
    user = users.find_one({"_id": name})
    if (user):
        raise KeyError("User with this name is alredy exists")
    else:
        user = users.insert_one({"_id": name, "password": password})

    return user


def is_user_exists(username):
    user = users.find_one({"_id": username})
    if (user):
        return True
    return False


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
