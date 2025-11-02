OUTPUTS = {
  "main": "Main menu.\n"
          "1. Start a quest\n"
          "0. Log out",

  "login_or_registration": "Login or create an account:\n"
                           "1. Login\n "
                           "2. Create an account",

  "login_username": "Login into account. \n"
                    "Enter username:",

  "registration_username": "Create an account.\n"
                           "Enter username:",

  "enter_password": "Enter password:",

  "registration_success": "Account succesfuly created!\n",

  "login_success": "You are logged in!",

  "logout_success": "You are logged out!",

  "logout": "Confirm logout:\n"
            "1. Confirm. \n"
            "2. Return to main menu",

  "retry_or_create": "Try again or type '1' to create an account."
}


ERRORS = {
  "unexpected_error": "Something went wrong. Please try again.",

  "fatal_error": "An unexpected error occurred. Please press Enter.",

  "invalid_input": "Invalid input. Please try again.",

  "username_unavailable": "This username is unavailable. Try another.",

  "username_not_found": "This username is not exist. Try another.",

  "invalid_username": "Invalid username. Rules:\n"
                      "- Must start with a letter.\n"
                      "- Can contain letters, numbers, '.', '-', '_'.\n"
                      "- Length must be between 3 and 20 characters.",

  "incorrect_password": "Incorrect password."
}


# Combined dictionary to import
MESSAGES = OUTPUTS | ERRORS


# Default separator
SEPARATOR = "\n"


def combine_messages(*keys: str) -> str:
    """
    Retrieves and combines a sequence of strings from the MESSAGES
    dictionary using separator.

    Parameters:
    ----------
    *keys : str
        Message keys to combine from the MESSAGES dictionary.

    Returns:
        str: The combined message string.
    """

    parts = [MESSAGES.get(key) for key in keys]
    return SEPARATOR.join(parts)
