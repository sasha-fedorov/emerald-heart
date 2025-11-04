import os
import re
import bcrypt
import random
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session
from pymongo import MongoClient
from bson.objectid import ObjectId
from messages import GAME, MESSAGES, combine_messages

# Load environment variables from a .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)
# Set a secret key for session management, loaded from environment variables
app.secret_key = os.getenv("SESSION_SECRET_KEY")

# Load MongoDB connection string and set up connection
CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING')
client = MongoClient(CONNECTION_STRING)
# Access the  database and collections
db = client["emerald-heart"]
sessions = db["sessions"]
users = db["users"]


class User:
    """
    A class to represent a user, handling user data and database interactions
    for stats and authentication.

    Attributes:
    ----------
    _id : str
        The name of the user (used as id).
    password_hash : str
        The user's password hash.
    wins: int
        Winned games count.
    loses: int
        Losed games count.
    """

    def __init__(self, _id: str, password_hash: str,
                 wins: int = 0, loses: int = 0):
        """
        Initializes a new User instance.
        """

        self._id = _id
        self.password_hash = password_hash
        self.wins = wins
        self.loses = loses

    @classmethod
    def add_user(cls, username: str, password: str):
        """
        Add a new user entry in the database after hashing the password.

        Raises:
            KeyError: If a user with the same name already exists.

        Returns: Created entitry
        """
        if cls.get_user(username):
            raise KeyError()  # When user with this name already exists
        else:
            # Generate a salt and hash the password using bcrypt
            salt = bcrypt.gensalt(rounds=8)
            hash = bcrypt.hashpw(password.encode('utf-8'), salt)
            password_hash = hash.decode('utf-8')
            user = cls(_id=username, password_hash=password_hash)
            # Insert the new user into the 'users' collection
            users.insert_one(user.__to_mongo_dict())
            return user

    def __to_mongo_dict(self):
        """
        Private method to convert entity to a MongoDB dictionary
        for saving and updating.

        Returns:
        MongoDB dictionary
        """
        return {
            "_id": self._id,
            "password_hash": self.password_hash,
            "wins": self.wins,
            "loses": self.loses
        }

    def increase_wins(self):
        """
        Increase wins of this user entry in the database. Update the object.
        """
        inc_wins = {"$inc": {"wins": 1}}
        # Update the database record
        result = users.update_one({"_id": self._id}, inc_wins)
        if result:
            self.wins = result

    def increase_loses(self):
        """
        Increase loses of this user entry in the database. Update the object.
        """
        inc_loses = {"$inc": {"loses": 1}}
        # Update the database record
        result = users.update_one({"_id": self._id}, inc_loses)
        if result:
            self.loses = result

    def reset_stats(self):
        """ Reset wins and loses of this user entry in the database. """
        self.wins = 0
        self.loses = 0
        # Use $set to explicitly overwrite the stats in the database
        res_stats = {"$set": self.__to_mongo_dict()}
        result = users.update_one({"_id": self._id}, res_stats)
        if result:
            return self

    def validate_password(self, password: str) -> bool:
        """
        Validates the provided password against the stored bcrypt hash.

        Parameters
        ----------
        password : str
            The password string provided by the user.

        Returns
        -------
        bool
            True if the provided password matches, False otherwise.
        """
        return bcrypt.checkpw(password.encode('utf-8'),
                              self.password_hash.encode('utf-8'))

    @classmethod
    def get_user(cls, username):
        """
        Get a User entry by username from the database and create a User object

        Parameters:
        ----------
        self : The class itself (User).
        username : str
            The name of the user.

        Returns:
        Found User class entry or None
        """

        # Find the user document by their unique ID (username)
        data = users.find_one({"_id": username})
        if data:
            _id = data.get('_id')
            password_hash = data.get('password_hash')
            # Use default 0 if 'wins' or 'loses' fields are missing
            wins = data.get('wins', 0)
            loses = data.get('loses', 0)
            # Create and return a User object
            return cls(_id=_id, password_hash=password_hash,
                       wins=wins, loses=loses)
        return data


def is_username_valid(username: str) -> bool:
    """
    Checks if the username conforms to the defined regex pattern.
    Pattern: Starts with a letter, 3 to 20 alphanumeric characters + ._-.
    """
    pattern = re.compile(r"^[A-Za-z][A-Za-z0-9._-]{2,19}$")
    return pattern.match(username)


def is_password_valid(password: str) -> tuple[bool, str]:
    """
    Checks if the password meets the basic complexity requirements.
    """
    if ' ' in password:
        return (False, "Password can not contain white spaces.")
    elif (len(password) < 3 or len(password) > 20):
        return (False, "Password must contain 3 and 20 characters.")
    return (True, "")


def get_session_user():
    """
    Retrieves the currently logged-in User object
    based on the session ID stored in Flask's session.
    It verifies the session ID against the 'sessions' collection
    and fetches the User from the 'users' collection.
    """
    session_id = session.get("session_id")
    if session_id:
        # Look up the session in the database
        stored_session = sessions.find_one({"_id": ObjectId(session_id)})
        if stored_session:
            username = stored_session["username"]
            user = User.get_user(username)
            if user:
                return user
            else:
                # If user no longer exists, terminate the session
                terminate_session(session_id)
        else:
            # If session ID is in Flask session but not in DB, remove it
            session.pop("session_id")


def terminate_session(session_id):
    """
    Deletes the session record from the database. Clears the Flask session.
    """
    sessions.delete_one({"_id": ObjectId(session_id)})
    session.clear()


def get_stats_dispay(user: User):
    """ Returns game stats information fufilled with user data. """
    wins = user.wins
    loses = user.loses
    total = wins + loses

    return MESSAGES["stats"].format(wins_count=wins,
                                    loses_count=loses,
                                    total_count=total)


@app.route('/')
def index():
    """ Renders the main HTML template for the game. """
    return render_template('index.html')


@app.route('/action', methods=['POST'])
def action():
    """
    Main event handler for user interactions (POST requests).
    This function acts as the state machine for the game flow, handling input,
    updating state, and determining the next action/display

    Returns a JSON object with:
        display:     next text to display on cleared screen (for main content)
        response:    next text to display (for prompts and information)
        next_action: the next action to exucute (selection validation)
        error:       error message when occured
    """

    data = request.get_json()

    action = data.get('action', '')  # Current state/context
    input = data.get('input', '')    # User's input

    # response variables
    response = ""
    next_action = action  # in case of invalid input/error
    error = ""
    display = ""

    # Get the logged-in user object, if any
    session_user = get_session_user()

    try:
        # State machine logic based on the current 'action'
        match action:
            case "init":
                # Initial load check
                if session_user:
                    # User logged in, go to main menu
                    display = MESSAGES["main"]
                    next_action = "main"
                else:
                    # Prompt for login/registration
                    response = MESSAGES["login_or_registration"]
                    next_action = "login_or_registration"

            case "main":
                # Main menu options
                match input.strip():
                    case "1":
                        # Start game
                        display = GAME[1]
                        next_action = "game_1"
                    case "2":
                        # View stats
                        display = get_stats_dispay(session_user)
                        next_action = "stats"
                    case "0":
                        # Logout prompt
                        response = MESSAGES["logout"]
                        next_action = "logout"

                    case _:
                        error = MESSAGES["invalid_input"]

            # --- Game States (game_X) ---
            # All game states follow similar input matching logic to finish
            # the quest, or apply a loss and transition to "game_over".

            case "game_1":
                match input.strip():
                    case "1":
                        display = GAME[21]
                        next_action = "game_21"
                    case "2":
                        display = GAME[22]
                        next_action = "game_22"
                    case "3":
                        # Loss scenario: update stats if user is logged in
                        if session_user:
                            session_user = session_user.increase_loses()

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
                        if session_user:
                            session_user = session_user.increase_loses()

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
                        if session_user:
                            session_user = session_user.increase_loses()

                        error = GAME[39]
                        response = MESSAGES["game_over"]
                        next_action = "game_over"
                    case _:
                        error = MESSAGES["invalid_input"]

            case "game_31":
                match input.strip():
                    case "1":
                        # Random chance for win/loss
                        if bool(random.getrandbits(1)):
                            # Win scenario
                            if session_user:
                                session_user = session_user.increase_wins()

                            display = GAME[41]
                            response = MESSAGES["game_over"]
                            next_action = "game_over"
                        else:
                            # Loss scenario
                            if session_user:
                                session_user = session_user.increase_loses()

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
                        if session_user:
                            session_user = session_user.increase_loses()

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
                        if session_user:
                            session_user = session_user.increase_loses()

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
                        if session_user:
                            session_user = session_user.increase_loses()

                        error = GAME[47]
                        response = MESSAGES["game_over"]
                        next_action = "game_over"
                    case _:
                        error = MESSAGES["invalid_input"]

            case "game_42":
                match input.strip():
                    case "1":
                        # Win scenario
                        if session_user:
                            session_user = session_user.increase_wins()

                        display = GAME[51]
                        response = MESSAGES["game_over"]
                        next_action = "game_over"
                    case "2":
                        # Loss scenario
                        if session_user:
                            session_user = session_user.increase_loses()

                        error = GAME[50]
                        response = MESSAGES["game_over"]
                        next_action = "game_over"
                    case _:
                        error = MESSAGES["invalid_input"]

            case "game_43":
                match input.strip():
                    case "1":
                        if session_user:
                            session_user = session_user.increase_wins()

                        display = GAME[52]
                        response = MESSAGES["game_over"]
                        next_action = "game_over"
                    case "2":
                        if session_user:
                            session_user = session_user.increase_loses()

                        error = GAME[59]
                        response = MESSAGES["game_over"]
                        next_action = "game_over"
                    case _:
                        error = MESSAGES["invalid_input"]

            case "game_44":
                match input.strip():
                    case "1":
                        if session_user:
                            session_user = session_user.increase_wins()

                        display = GAME[51]
                        response = MESSAGES["game_over"]
                        next_action = "game_over"
                    case "2":
                        if session_user:
                            session_user = session_user.increase_loses()

                        error = GAME[58]
                        response = MESSAGES["game_over"]
                        next_action = "game_over"
                    case _:
                        error = MESSAGES["invalid_input"]

            case "game_over":
                # Options after a game ends
                match input.strip():
                    case "1":
                        # Return to main menu (or login if not logged in)
                        if session_user:
                            display = MESSAGES["main"]
                            next_action = "main"
                        else:
                            display = MESSAGES["login_or_registration"]
                            next_action = "login_or_registration"
                    case "2":
                        # Restart the game immediately
                        display = GAME[1]
                        next_action = "game_1"
                    case _:
                        error = MESSAGES["invalid_input"]

            case "stats":
                # Stats menu options
                match input.strip():
                    case "1":
                        # Back to main menu
                        display = MESSAGES["main"]
                        next_action = "main"
                    case "2":
                        # Prompt for stats reset confirmation
                        response = MESSAGES["stats_reset"]
                        next_action = "stats_reset"
                    case _:
                        error = MESSAGES["invalid_input"]

            case "stats_reset":
                # Stats reset confirmation
                match input.strip():
                    case "1":
                        # Perform stats reset
                        session_user = session_user.reset_stats()
                        # Using display to update reseted stats
                        display = get_stats_dispay(session_user)
                        response = MESSAGES["stats_reset_done"]
                        next_action = "stats_reset"  # Stay on stats view
                    case "2":
                        # Cancel reset, redraw to stats menu
                        display = get_stats_dispay(session_user)
                        next_action = "stats"
                    case _:
                        error = MESSAGES["invalid_input"]

            # --- Authentication States ---

            case "login_or_registration":
                # Initial authentication choice
                match input.strip():
                    case "1":
                        response = MESSAGES["login_username"]
                        next_action = "login_username"
                    case "2":
                        response = MESSAGES["registration_username"]
                        next_action = "registration_username"
                    case "3":
                        # Play without registering
                        response = MESSAGES["unregistred_game"]
                        next_action = "unregistred_game"
                    case _:
                        error = MESSAGES["invalid_input"]

            case "unregistred_game":
                # Warning of no stats will be saved
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
                # Handle username input during registration
                if is_username_valid(input):
                    if User.get_user(input):
                        error = MESSAGES["username_unavailable"]
                    else:
                        # Store username temporarily in session
                        session["username"] = input
                        response = MESSAGES["enter_password"]
                        next_action = "registration_password"
                else:
                    error = MESSAGES["invalid_username"]

            case "registration_password":
                # Handle password input during registration
                is_valid, error_msg = is_password_valid(input)
                if is_valid:
                    try:
                        # Pull username temporarily from session
                        name = session.get("username")
                        # Create new user in DB
                        User.add_user(name, input)

                        # Success, prompt for login
                        response = combine_messages("registration_success",
                                                    "login_username")
                        next_action = "login_username"
                    except KeyError:
                        # Should not happen if previous checks were correct
                        error = MESSAGES["unexpected_error"]
                        response = MESSAGES["login_or_registration"]
                        next_action = "init"
                else:
                    error = error_msg  # Corresponding password error message

            case "login_username":
                # Handle username input during login
                if input.strip() == "1":
                    # Option to switch to registration
                    response = MESSAGES["registration_username"]
                    next_action = "registration_username"
                elif is_username_valid(input):
                    if User.get_user(input):
                        # Username found, proceed to password
                        session["username"] = input
                        response = MESSAGES["enter_password"]
                        next_action = "login_password"
                    else:
                        # Username not found
                        error = combine_messages("username_not_found",
                                                 "retry_or_create")
                else:
                    # Invalid format
                    error = combine_messages("invalid_username",
                                             "retry_or_create")

            case "login_password":
                # Handle password input during login
                if input.strip() == "1":
                    # Option to switch to registration
                    response = MESSAGES["registration_username"]
                    next_action = "registration_username"
                else:
                    try:
                        # Pull username temporarily from session
                        name = session.get("username")
                        user = User.get_user(name)
                        if user:
                            if user.validate_password(input):
                                # Create session in DB and Flask session
                                _id = sessions.insert_one({"username": name})
                                session["session_id"] = str(_id.inserted_id)

                                display = MESSAGES["main"]
                                next_action = "main"  # Successful login
                            else:
                                # Password incorrect
                                error = combine_messages("incorrect_password",
                                                         "retry_or_create")
                        else:
                            # User object or Flask session value read
                            # retrieval failed unexpectedly
                            raise KeyError
                    except KeyError:
                        error = MESSAGES["unexpected_error"]
                        response = MESSAGES["login_or_registration"]
                        next_action = "init"

            case "logout":
                # Logout confirmation
                match input.strip():
                    case "1":
                        # Confirm and terminate session
                        terminate_session(session["session_id"])
                        display = MESSAGES["login_or_registration"]
                        next_action = "login_or_registration"
                    case "2":
                        # Cancel logout, return to main menu
                        display = MESSAGES["main"]
                        next_action = "main"
                    case _:
                        error = MESSAGES["invalid_input"]

            case _:
                # Catch-all for unknown actions
                error = MESSAGES["fatal_error"]
                next_action = "init"

        # Construct the final JSON response
        result = {
            "response": response,
            "next_action": next_action,
            "error": error,
            "display": display
        }
        return jsonify(result)
    except Exception as e:
        # Catch any unexpected application errors and display them
        return jsonify({'error': f"Unexpected error: {e}. Please try again",
                        'next_action': 'init'})


if __name__ == '__main__':
    # Run the application
    app.run(host='0.0.0.0', port=5000)
