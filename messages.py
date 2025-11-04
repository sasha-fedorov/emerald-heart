OUTPUTS = {
  "main": "Main menu.\n"
          "1. Start a quest\n"
          "2. Quest History\n"
          "0. Log out",

  "login_or_registration": "Login or create an account:\n"
                           "1. Login\n"
                           "2. Create an account\n"
                           "3. Start a quest",

  "unregistred_game": "Without login your Quest History will not be saved.\n"
                      "1. Start a quest\n"
                      "2. Return to login",

  "login_username": "Login into account. \n"
                    "Enter username:",

  "registration_username": "Create an account.\n"
                           "Enter username:",

  "enter_password": "Enter password:",

  "registration_success": "Account succesfuly created!\n",

  "logout": "Confirm logout:\n"
            "1. Confirm. \n"
            "2. Return to main menu",

  "retry_or_create": "Try again or type '1' to create an account.",

  "game_over": "1. Return to main menu\n"
               "2. Start a new quest.",

  "stats": "                          Quest History\n"
            "-----------------------------------"
            "----------------------------------\n"
            "Your efforts are recorded below:\n\n"
            "Victories:      {wins_count}\n"
            "Loses:          {loses_count}\n"
            "Quests Started: {total_count}\n\n"
            "1. Return to main menu\n"
            "2. Reset Quest History",

  "stats_reset": "Confirm resetting your Quest History:\n"
            "1. Confirm. \n"
            "2. Deny",

  "stats_reset_done": "\nYour quest history has been successfully reset."
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

  21: "                        The Cavern of Echoes\n"
      "---------------------------------------------------------------------\n"
      "You reach a massive cave mouth glowing faintly with green mist.\n"
      "A faint rumble echoes from within - a dragon's breathing, perhaps.\n"
      "Near the entrance lies a rusty sword, half-buried in dirt.\n\n"
      "1. Enter the cave quietly\n"
      "2. Pick up the sword\n"
      "3. Shout into the cave",

  22: "                         The Old Watchtower\n"
      "---------------------------------------------------------------------\n"
      "The tower leans precariously over a cliff.\n"
      "Inside, dust and spiderwebs coat everything.\n"
      "At the top, you find an old knight's journal and a silver key.\n\n"
      "1. Read the journal\n"
      "2. Take the key\n"
      "3. Leave immediately",

  20: "You drift to sleep as the wind whispers through the leaves.\n"
      "When you awaken, your supplies are gone,\n"
      "and the full moon has passed.\n"
      "You failed your quest.\n\n"
      "GAME OVER - You ran out of time.\n",

  31: "                      Sneaking Inside the Cave\n"
      "---------------------------------------------------------------------\n"
      "You move carefully through tunnels until you reach a glowing chamber.\n"
      "A huge dragon sleeps atop a mound of gold. Behind it, on a pedestal,"
      "lies the Emerald Heart.\n\n"
      "1. Try to sneak past and grab the gem\n"
      "2. Search the side tunnel for another way",

  32: "                        Picking up the Sword\n"
      "---------------------------------------------------------------------\n"
      "You lift the rusty blade - it glows faintly.\n"
      "The inscription reads: 'Forged to slay the fireborn'\n"
      "You feel a surge of courage.\n\n"
      "1. Enter the cave with sword drawn\n"
      "2. Drop the sword - it feels cursed",

  33: "                        Reading the Journal\n"
      "---------------------------------------------------------------------\n"
      "The journal speaks of an ancient oath:\n"
      "'The dragon fears its reflection, and the blade that mirrors its flame."
      "'You also find a sketch of a mirror shield hidden in the caves.\n\n"
      "1. Take notes and head for the Cavern of Echoes\n"
      "2. Stay and rest in the tower",

  34: "                       Taking the Silver Key\n"
      "---------------------------------------------------------------------\n"
      "You take the key. Suddenly, you hear rumbling - a hidden door in the "
      "tower wall opens, revealing a secret tunnel leading underground.\n\n"
      "1. Enter the secret tunnel\n"
      "2. Leave the key and back away",

  30: "Your voice booms through the cavern.\n"
      "A moment later, the mountain trembles\n"
      "and a burst of fire erupts from the darkness.\n\n"
      "GAME OVER - Burned by dragon fire.\n",

  39: "As you descend, the floor collapses under your feet.\n"
      "You plummet into darkness.\n\n"
      "GAME OVER - Fell to your death.\n",

  41: "                        The Thief of Fire\n"
      "---------------------------------------------------------------------\n"
      "You slip through the gold like smoke."
      "The dragon stirs but doesn't wake."
      "The Emerald Heart is yours before dawn.\n"
      "Behind you, the beast still dreams.\n"
      "You stole the Emerald Heart without a single drop of blood.\n\n"
      "VICTORY! The clever thief who outwitted a dragon.\n",

  42: "                           Side Tunnel\n"
      "---------------------------------------------------------------------\n"
      "You discover a mirror shield lying in a pool of water, shining faintly."
      "\nThis must be the 'reflection' weapon from the knight's journal.\n\n"
      "1. Take the shield and confront the dragon\n"
      "2. Ignore it and return to the main chamber",

  43: "                      Confronting the Dragon\n"
      "---------------------------------------------------------------------\n"
      "With the glowing sword in hand, you challenge the sleeping beast.\n"
      "It awakens, roaring - fire fills the air.\n\n"
      "1. Attack the dragon's heart directly\n"
      "2. Try to talk to it",

  44: "                          Secret Tunnel\n"
      "---------------------------------------------------------------------\n"
      "You follow the tunnel and find yourself behind the dragon's lair.\n"
      "You can see the Emerald Heart through cracks in the wall.\n\n"
      "1. Use the key on the stone door\n"
      "2. Try to break the wall",

  47: "The tunnel seals shut forever, and your chance is lost.\n\n"
      "GAME OVER - Missed your destiny.\n",

  48: "As you sleep, goblins raid the tower. You are never seen again.\n\n"
      "GAME OVER - Ambushed.\n",

  49: "The moment you release the sword, a serpent of fire bursts from "
      "the ground and devours you.\n\n"
      "GAME OVER - Never drop the blade.\n",

  40: "You step on a loose coin - clink. The dragon's eyes flare open.\n"
      "A blast of flame ends your story.\n\n"
      "GAME OVER - Fried hero.\n",

  51: "                        The Mirror Shield\n"
      "---------------------------------------------------------------------\n"
      "You raise the mirror shield as the dragon breathes fire.\n"
      "The flames rebound - the dragon turns to stone!\n"
      "You take the Emerald Heart from its frozen claws.\n\n"
      "VICTORY! You claimed the Emerald Heart and saved the realm!\n",

  52: "                        The Dragon Slayer\n"
      "---------------------------------------------------------------------\n"
      "Your sword burns brighter than the dragon's fire.\n"
      "You leap, striking through the dragon's heart.\n"
      "With a roar, it collapses, defeated.\n"
      "You seize the Emerald Heart and leave the cave as dawn breaks.\n\n"
      "VICTORY! You slew the dragon and reclaimed the Emerald Heart!\n",

  58: "The noise wakes the dragon - the wall explodes in fire.\n\n"
      "GAME OVER - Burned alive.\n",

  59: "The dragon doesn't do diplomacy.\n\n"
      "GAME OVER - Roasted alive.\n",

  50: "Without protection, you face the dragon - "
      "and the last thing you see is flame.\n\n"
      "GAME OVER - No shield, no chance.\n",
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
