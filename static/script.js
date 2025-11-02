const inputField = document.getElementById('input');
const consoleDiv = document.getElementById('output');
var action = 'init';

window.onload = function () {
  sendInput()
};

document.addEventListener("click", () => {
  document.getElementById("input").focus();
});

inputField.addEventListener('keydown', function (e) {
  if (e.key === 'Enter') {
    const input = inputField.value;
    printToConsole(`> ${input} \n`);
    sendInput(input);
    inputField.value = '';
  }
});

function printToConsole(text, charDelay = 1) {
  const outputText = text.replace(/\n/g, '[BR]');
  let charIndex = 0;

  function typeCharacter() {
    if (charIndex < outputText.length) {

      let char = outputText[charIndex];

      // check for the newline marker
      if (char == '[' && outputText.substring(charIndex, charIndex + 4) == '[BR]') {
        consoleDiv.innerHTML += '<br>';
        charIndex += 4; // skip '[BR]'
      } else {
        // append the character
        consoleDiv.innerHTML += char;
        charIndex++;
      }

      // scroll to the bottom
      consoleDiv.scrollTop = consoleDiv.scrollHeight;

      // schedule the next character print with deley 1
      setTimeout(typeCharacter, 1);

    } else {

      isPrinting = false;
      // add final break line 
      consoleDiv.innerHTML += '<br>';
      consoleDiv.scrollTop = consoleDiv.scrollHeight;
    }
  }

  // start the typing process
  typeCharacter();
}

function clearConsole() {
  consoleDiv.innerHTML = ""
}

async function sendInput(input = '') {
  const res = await fetch('/action', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      input,
      action
    })
  });
  const data = await res.json();

  if (data.error) {
    printToConsole(`<span>${data.error}</span>`);
  }
  if (data.response) {
    printToConsole(data.response);
  }
  if (data.next_action) {
    action = data.next_action;
  }
}