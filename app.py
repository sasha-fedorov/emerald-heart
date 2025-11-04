import os
import re
import random
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session
from pymongo import MongoClient
from bson.objectid import ObjectId
from messages import GAME, MESSAGES, combine_messages

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
        if user:
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
    def get_user(cls, username):
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
        if data:
            name = data.get('_id')
            password = data.get('password')
            return cls(name=name, password=password)
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
    if session_id:
        stored_session = sessions.find_one({"_id": ObjectId(session_id)})
        if stored_session:
            username = stored_session["username"]
            user = User.get_user(username)
            if user:
                return user
            else:
                terminate_session(session_id)
        else:
            session.pop("session_id")


def terminate_session(session_id):
    sessions.delete_one({"_id": ObjectId(session_id)})
    session.clear()


@app.route('/')
def index():
    """ Returns page to show """
    return render_template('index.html')


@app.route('/action', methods=['POST'])
def action():
    """
    Event handler from user

    Returns result from action as:
        display:     next text to display on cleared screen
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
    display = ""

    session_user = get_session_user()

    try:
        match action:
            case "init":
                if session_user:
                    display = MESSAGES["main"]
                    next_action = "main"
                else:
                    response = MESSAGES["login_or_registration"]
                    next_action = "login_or_registration"

            case "main":
                match input.strip():
                    case "1":
                        display = GAME[1]
                        next_action = "game_1"
                    case "0":
                        response = MESSAGES["logout"]
                        next_action = "logout"

                    case _:
                        error = MESSAGES["invalid_input"]

            case "game_1":
                match input.strip():
                    case "1":
                        display = GAME[21]
                        next_action = "game_21"
                    case "2":
                        display = GAME[22]
                        next_action = "game_22"
                    case "3":
                        error = GAME[20]
                        response = MESSAGES["game_over"]
                        next_action = "game_over"
                    case _:
                        error = MESSAGES["invalid_input"]

            case "game_21":
                match input.strip():
                    case "1":
                        display = GAME[31]
                        next_action = "game_31"
                    case "2":
                        display = GAME[32]
                        next_action = "game_32"
                    case "3":
                        error = GAME[30]
                        response = MESSAGES["game_over"]
                        next_action = "game_over"
                    case _:
                        error = MESSAGES["invalid_input"]

            case "game_22":
                match input.strip():
                    case "1":
                        display = GAME[33]
                        next_action = "game_33"
                    case "2":
                        display = GAME[34]
                        next_action = "game_34"
                    case "3":
                        error = GAME[39]
                        response = MESSAGES["game_over"]
                        next_action = "game_over"
                    case _:
                        error = MESSAGES["invalid_input"]

            case "game_31":
                match input.strip():
                    case "1":
                        # 50/50 for the good ending
                        if bool(random.getrandbits(1)):
                            display = GAME[41]
                            response = MESSAGES["game_over"]
                            next_action = "game_over"
                        else:
                            error = GAME[40]
                            response = MESSAGES["game_over"]
                            next_action = "game_over"
                    case "2":
                        display = GAME[42]
                        next_action = "game_42"
                    case _:
                        error = MESSAGES["invalid_input"]

            case "game_32":
                match input.strip():
                    case "1":
                        display = GAME[43]
                        next_action = "game_43"
                    case "2":
                        error = GAME[40]
                        response = MESSAGES["game_over"]
                        next_action = "game_over"
                    case _:
                        error = MESSAGES["invalid_input"]

            case "game_33":
                match input.strip():
                    case "1":
                        display = GAME[21]
                        next_action = "game_21"
                    case "2":
                        error = GAME[48]
                        response = MESSAGES["game_over"]
                        next_action = "game_over"
                    case _:
                        error = MESSAGES["invalid_input"]

            case "game_34":
                match input.strip():
                    case "1":
                        display = GAME[44]
                        next_action = "game_44"
                    case "2":
                        error = GAME[47]
                        response = MESSAGES["game_over"]
                        next_action = "game_over"
                    case _:
                        error = MESSAGES["invalid_input"]

            case "game_42":
                match input.strip():
                    case "1":
                        display = GAME[51]
                        response = MESSAGES["game_over"]
                        next_action = "game_over"
                    case "2":
                        error = GAME[50]
                        response = MESSAGES["game_over"]
                        next_action = "game_over"
                    case _:
                        error = MESSAGES["invalid_input"]

            case "game_43":
                match input.strip():
                    case "1":
                        display = GAME[52]
                        response = MESSAGES["game_over"]
                        next_action = "game_over"
                    case "2":
                        error = GAME[59]
                        response = MESSAGES["game_over"]
                        next_action = "game_over"
                    case _:
                        error = MESSAGES["invalid_input"]

            case "game_44":
                match input.strip():
                    case "1":
                        display = GAME[51]
                        response = MESSAGES["game_over"]
                        next_action = "game_over"
                    case "2":
                        error = GAME[58]
                        response = MESSAGES["game_over"]
                        next_action = "game_over"
                    case _:
                        error = MESSAGES["invalid_input"]

            case "game_over":
                match input.strip():
                    case "1":
                        if session_user:
                            display = MESSAGES["main"]
                            next_action = "main"
                        else:
                            response = MESSAGES["login_or_registration"]
                            next_action = "login_or_registration"
                    case "2":
                        display = GAME[1]
                        next_action = "game_1"
                    case _:
                        error = MESSAGES["invalid_input"]

            case "login_or_registration":
                match input.strip():
                    case "1":
                        response = MESSAGES["login_username"]
                        next_action = "login_username"
                    case "2":
                        response = MESSAGES["registration_username"]
                        next_action = "registration_username"
                    case "3":
                        response = MESSAGES["unregistred_game"]
                        next_action = "unregistred_game"
                    case _:
                        error = MESSAGES["invalid_input"]

            case "unregistred_game":
                match input.strip():
                    case "1":
                        display = GAME[1]
                        next_action = "game_1"
                    case "2":
                        display = MESSAGES["login_or_registration"]
                        next_action = "login_or_registration"
                    case _:
                        error = MESSAGES["invalid_input"]

            case "registration_username":
                if is_username_valid(input):
                    if User.get_user(input):
                        error = MESSAGES["username_unavailable"]
                    else:
                        session["username"] = input
                        response = MESSAGES["enter_password"]
                        next_action = "registration_password"
                else:
                    error = MESSAGES["invalid_username"]

            case "registration_password":
                is_valid, error = is_password_valid(input)
                if is_valid:
                    try:
                        name = session.get("username")
                        user = User(name, input)
                        user.add_user()

                        response = combine_messages("registration_success",
                                                    "login_username")
                        next_action = "login_username"
                    except KeyError:
                        error = MESSAGES["unexpected_error"]
                        response = MESSAGES["login_or_registration"]
                        next_action = "init"

            case "login_username":
                if input.strip() == "1":
                    response = MESSAGES["registration_username"]
                    next_action = "registration_username"
                elif is_username_valid(input):
                    if User.get_user(input):
                        session["username"] = input
                        response = MESSAGES["enter_password"]
                        next_action = "login_password"
                    else:
                        error = combine_messages("username_not_found",
                                                 "retry_or_create")
                else:
                    error = combine_messages("invalid_username",
                                             "retry_or_create")

            case "login_password":
                if input.strip() == "1":
                    response = MESSAGES["registration_username"]
                    next_action = "registration_username"
                else:
                    try:
                        name = session.get("username")
                        user = User.get_user(name)
                        if user:
                            if user.validate_password(input):
                                _id = sessions.insert_one({"username": name})
                                session["session_id"] = str(_id.inserted_id)

                                response = combine_messages("login_success",
                                                            "main")
                                next_action = "main"
                            else:
                                error = combine_messages("incorrect_password",
                                                         "retry_or_create")
                        else:
                            raise KeyError
                    except KeyError:
                        error = MESSAGES["unexpected_error"]
                        response = MESSAGES["login_or_registration"]
                        next_action = "init"

            case "logout":
                match input.strip():
                    case "1":
                        terminate_session(session["session_id"])
                        response = combine_messages("logout_success",
                                                    "login_or_registration")
                        next_action = "login_or_registration"
                    case "2":
                        response = MESSAGES["main"]
                        next_action = "main"
                    case _:
                        error = MESSAGES["invalid_input"]

            case _:
                error = MESSAGES["fatal_error"]
                next_action = "init"

        result = {
            "response": response,
            "next_action": next_action,
            "error": error,
            "display": display
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f"Unexpected error: {e}. Please try again",
                        'next_action': 'init'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
