/* jshint esversion: 8 */

const inputField = document.getElementById('input');
const consoleDiv = document.getElementById('output');
var action = 'init'; // Global variable tracking the current game state
var isPrinting = false; // Flag to prevent user input on printing

// Function called when the page finishes loading
window.onload = function () {
  sendInput(); // Send an empty input to the backend to start the 'init' action
};

// Focus on the input field whenever the user clicks anywhere on the page
document.addEventListener("click", () => {
  document.getElementById("input").focus();
});

// Event listener for Enter key presses in the input field
inputField.addEventListener('keydown', function (e) {
  // Prevent input on printing to do not interrupt it
  if (isPrinting) {
    return;
  }

  // Check if the pressed key is 'Enter'
  if (e.key === 'Enter') {
    const input = inputField.value;

    // 1. Print the user's input to the console first
    printToConsole(`> ${input}`).then(_ => {
      // 2. Once printing is done, send the input to the backend
      sendInput(input);
      // 3. Clear the input field for the next turn
      inputField.value = '';
    });
  }
});


// Simulates a typing effect by printing text character by character.
function printToConsole(text, element = consoleDiv, charDelay = 1) {
  // Set flag to block user input
  isPrinting = true;

  // Return a promise to enable awaiting the print completion
  return new Promise(resolve => {
    // Replace actual newline characters (\n) with a custom marker for HTML <br> tags
    const outputText = text.replace(/\n/g, '[BR]');
    let charIndex = 0;

    // Recursive function to type each character
    function typeCharacter() {
      if (charIndex < outputText.length) {

        let char = outputText[charIndex];

        // Check for the newline marker
        if (char == '[' && outputText.substring(charIndex, charIndex + 4) == '[BR]') {
          element.innerHTML += '<br>';
          charIndex += 4; // Skip the '[BR]' marker
        } else {
          // Append the character
          element.innerHTML += char;
          charIndex++;
          // Scroll to the bottom to keep the newest text visible
          element.scrollTop = element.scrollHeight;
        }

        // Schedule the next character print with the specified delay
        setTimeout(typeCharacter, charDelay);

      } else {
        // Printing complete:
        isPrinting = false; // Allow input again
        element.innerHTML += '<br>'; // Add a final line break for spacing
        element.scrollTop = element.scrollHeight; // Final scroll to the bottom
        resolve(); // Resolve the promise
      }
    }

    // Start the recursive typing process
    typeCharacter();
  });
}

// Clears all content from the console output
function clearConsole() {
  consoleDiv.innerHTML = "";
}

// Sends user input and the current game state to the Flask backend via AJAX.
// Handles the response data (display, error, response text, and next action).
async function sendInput(input = '') {
  // Perform a POST request to the '/action' endpoint
  const res = await fetch('/action', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      input,
      action // Send the current game state/context
    })
  });
  // Parse the JSON response from the server
  const data = await res.json();

  // Handle 'display': New screen content (clears the console first)
  if (data.display) {
    clearConsole();
    await printToConsole(data.display);
  }
  // Handle 'error': Error message (prints directly to console)
  if (data.error) {
    let span = document.createElement("span"); // Use the span element to style errors
    consoleDiv.appendChild(span);
    await printToConsole(data.error, span);
  }
  // Handle 'response': Prompt or message (prints directly to console)
  if (data.response) {
    await printToConsole(data.response);
  }
  // Update the state for the next turn
  if (data.next_action) {
    action = data.next_action;
  }
}