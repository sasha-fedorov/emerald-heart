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

  "retry_or_create": "Try again or type '1' to create an account.",

  "game_over": "1. Return to main menu\n"
               "2. Start a new game."

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


GAME = {
  1: "                          At the Crossroads\n"
     "---------------------------------------------------------------------\n"
     "You stand at the fork of an old forest road."
     "One path leads to the Cavern of Echoes,"
     "the other to the Old Watchtower.\n\n"
     "Your quest: find the Emerald Heart before the full moon sets.\n\n"
     "1. Go to the Cavern of Echoes\n"
     "2. Head toward the Old Watchtower\n"
     "3. Rest under the oak tree",

  11: "                        The Cavern of Echoes\n"
      "---------------------------------------------------------------------\n"
      "You reach a massive cave mouth glowing faintly with green mist.\n"
      "A faint rumble echoes from within - a dragon's breathing, perhaps.\n"
      "Near the entrance lies a rusty sword, half-buried in dirt.\n\n"
      "1. Enter the cave quietly\n"
      "2. Pick up the sword\n"
      "3. Shout into the cave",

  12: "                         The Old Watchtower\n"
      "---------------------------------------------------------------------\n"
      "The tower leans precariously over a cliff.\n"
      "Inside, dust and spiderwebs coat everything.\n"
      "At the top, you find an old knight's journal and a silver key."
      "1. Read the journal\n"
      "2. Take the key\n"
      "3. Leave immediately",

  13: "You drift to sleep as the wind whispers through the leaves.\n"
      "When you awaken, your supplies are gone,\n"
      "and the full moon has passed.\n"
      "You failed your quest.\n"
      "GAME OVER - You ran out of time.",

  23: "Your voice booms through the cavern.\n"
      "A moment later, the mountain trembles\n"
      "and a burst of fire erupts from the darkness.\n"
      "GAME OVER - Burned by dragon fire."
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
