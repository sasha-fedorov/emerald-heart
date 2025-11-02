import os
import re
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session
from pymongo import MongoClient
from bson.objectid import ObjectId

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

    def add_user(self):
        """ Add this user entry in the database """
        user = users.find_one({"_id": self._id})
        if (user):
            raise KeyError()  # When user with this name already exists
        else:
            users.insert_one({"_id": self._id, "password": self.password})

    def validate_password(self, password: str) -> bool:
        """
        Validates the provided password against the user's stored password.

        Parameters
        ----------
        password : str
            The password string provided by the user.

        Returns
        -------
        bool
            True if the provided password matches, False otherwise.
        """
        return self.password == password

    @classmethod
    def get_user(self, username):
        """
        Get a User entry by username from the database.

        Parameters:
        ----------
        self : The class itself (User).
        username : str
            The name of the user.

        Returns:
        Finded User class entry or None
        """

        data = users.find_one({"_id": username})
        if (data):
            name = data.get('_id')
            password = data.get('password')
            return self(name=name, password=password)
        return data


def is_username_valid(username: str) -> bool:
    pattern = re.compile(r"^[A-Za-z][A-Za-z0-9._-]{2,19}$")
    return pattern.match(username)


def is_password_valid(password: str) -> tuple[bool, str]:
    if ' ' in password:
        return (False, "Password can not contain white spaces.")
    elif (len(password) < 3 or len(password) > 20):
        return (False, "Password must contain 3 and 20 characters.")
    return (True, "")


def get_session_user():
    session_id = session.get("session_id")
    if (session_id):
        stored_session = sessions.find_one({"_id": ObjectId(session_id)})
        if (stored_session):
            username = stored_session["username"]
            user = User.get_user(username)
            if (user):
                return user
            else:
                terminate_session(session_id)
        else:
            session.pop("session_id")


def terminate_session(session_id):
    sessions.delete_one({"_id": ObjectId(session_id)})
    session.pop("session_id")


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

    session_user = get_session_user()

    try:
        match action:
            case "init":
                if (session_user):
                    next_action = "main_selection"
                    response = response = "Main menu. \n" \
                                          "0. Log out"
                else:
                    response = "Login or create an account: \n " \
                            "1. Login \n " \
                            "2. Create an account"
                    next_action = "login_or_registration"

            case "login_or_registration":
                try:
                    match input.strip():
                        case "1":
                            response = "Login into account. \nEnter username:"
                            next_action = "login_username"
                        case "2":
                            response = "Create an account. \nEnter username:"
                            next_action = "registration_username"
                        case _: raise ValueError
                except ValueError:
                    error = "Invalid input. Please enter 1 or 2"

            case "registration_username":
                if (is_username_valid(input)):
                    if (User.get_user(input)):
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
                is_valid, error = is_password_valid(input)
                if is_valid:
                    try:
                        name = session.get("username")
                        if (name is None):
                            raise KeyError()

                        user = User(name, input)
                        user.add_user()

                        response = "Account succesfuly created!\n" \
                                   "Login into account.\n" \
                                   "Enter username:"
                        next_action = "login_username"
                    except KeyError:
                        error = "Something went wrong. Try again."
                        response = "Login or create an account: \n " \
                                   "1. Login \n " \
                                   "2. Create an account"
                        next_action = "init"

            case "login_username":
                if (input.strip() == "1"):
                    response = "Create an account. \nEnter username:"
                    next_action = "registration_username"
                elif (is_username_valid(input)):
                    if (User.get_user(input)):
                        response = "Enter password:"
                        next_action = "login_password"
                        session["username"] = input
                    else:
                        error = "This username not exists.\n" \
                                "Try again or type '1' to create an account."
                else:
                    error = "Invalid username. Rules:\n"\
                            "- Must start with a letter.\n"\
                            "- Can contain letters, numbers, '.', '-', '_'.\n"\
                            "- Length must be between 3 and 20 characters. \n"\
                            "Try another one or type '1' to create an account."

            case "login_password":
                if (input.strip() == "1"):
                    response = "Create an account. \nEnter username:"
                    next_action = "registration_username"
                else:
                    try:
                        name = session.get("username")
                        if (name is None):
                            raise KeyError()

                        user = User.get_user(name)
                        if (user):
                            if (user.validate_password(input)):
                                _id = sessions.insert_one({"username": name})
                                session["session_id"] = str(_id.inserted_id)

                                response = "You are logged in! \n" \
                                           "Main menu. \n" \
                                           "0. Log out"
                                next_action = "main_selection"
                            else:
                                error = "Incorrect password.\n Try again or " \
                                        "type '1' to create an account."
                        else:
                            raise KeyError
                    except KeyError:
                        error = "Something went wrong. Try again."
                        response = "Login or create an account: \n " \
                                   "1. Login \n " \
                                   "2. Create an account"
                        next_action = "init"

            case "main":
                response = "0. Log out"
                next_action = "main_selection"

            case "main_selection":
                match input.strip():
                    case "0":
                        response = "Confirm logut:\n" \
                                   "1. Confirm. \n" \
                                   "2. Return to main menu"
                        next_action = "logout"

                    case _:
                        error = "Invalid input. Please try again."

            case "logout":
                match input.strip():
                    case "1":
                        terminate_session(session["session_id"])
                        response = "You logged out! \n" \
                                   "Login or create an account: \n " \
                                   "1. Login \n " \
                                   "2. Create an account"
                        next_action = "login_or_registration"
                    case "2":
                        response = "Main menu. \n" \
                                   "0. Log out"
                        next_action = "main_selection"
                    case _:
                        error = "Invalid input. Please try again."

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
