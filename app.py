import os
import re
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET_KEY")

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


def is_user_exists(username: str) -> bool:
    user = users.find_one({"_id": username})
    return user is not None


def is_username_valid(username: str) -> bool:
    pattern = re.compile(r"^[A-Za-z][A-Za-z0-9._-]{2,19}$")
    return pattern.match(username)


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

    action = data.get('action', '')
    input = data.get('input', '')

    response = ""
    next_action = action
    error = ""

    try:
        match action:
            case "init":
                response = "Login or create an account: \n " \
                           "1. Login \n " \
                           "2. Create an account"
                next_action = "login_or_registration"

            case "login_or_registration":
                try:
                    match input.strip():
                        case "1":
                            response = "Enter username:"
                            next_action = "login_username"
                        case "2":
                            response = "Enter username:"
                            next_action = "registration_username"
                        case _: raise ValueError
                except ValueError:
                    error = "Invalid input. Please enter 1 or 2"

            case "registration_username":
                pattern = re.compile(r"^[A-Za-z][A-Za-z0-9._-]{2,19}$")
                if (pattern.match(input)):
                    if (is_user_exists(input)):
                        error = "This username is unavailable. Try another."
                    else:
                        response = "Enter password:"
                        next_action = "registration_password"
                        session["username"] = input
                else:
                    error = "Invalid username. Rules:\n"\
                            "- Must start with a letter.\n"\
                            "- Can contain letters, numbers, '.', '-', '_'.\n"\
                            "- Length must be between 3 and 20 characters."

            case "registration_password":
                if (len(input) != len(data.get('input', ''))):
                    error = "Password can not contain white spaces."
                elif (len(input) < 2 | len(input) > 19):
                    error = "Password must contain 3 and 20 characters."
                else:
                    try:
                        name = session.get("username")
                        if (name is None):
                            raise KeyError()

                        user = User(name, input)
                        user.create_user()
                        # next action main menu
                    except KeyError:
                        error = "Something went wrong. Try again."
                        next_action = "login_or_registration"

            case _:
                error = "Unexpected error occurs, please try again"
                next_action = "init"
                response = "Login or create an account: \n " \
                           "1. Login \n " \
                           "2. Create an account"

        result = {
            "response": response,
            "next_action": next_action,
            "error": error
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f"Unexpected error: {e}. Please try again",
                        'next_action': 'init'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
