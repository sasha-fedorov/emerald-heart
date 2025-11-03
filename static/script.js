const inputField = document.getElementById('input');
const consoleDiv = document.getElementById('output');
var action = 'init';
var isPrinting = false

window.onload = function () {
  sendInput()
};

document.addEventListener("click", () => {
  document.getElementById("input").focus();
});

inputField.addEventListener('keydown', function (e) {
  //don't allow to interrupt printing process by input
  if (isPrinting) {
    return;
  }

  if (e.key === 'Enter') {
    const input = inputField.value;
    printToConsole(`> ${input}`).then(_ => {
      sendInput(input);
      inputField.value = '';
    });
  }
});

function printToConsole(text, element = consoleDiv, charDelay = 1) {
  // don't allow to interrupt printing process by input
  isPrinting = true;

  // return a promise to enable await
  return new Promise(resolve => {
    const outputText = text.replace(/\n/g, '[BR]');
    let charIndex = 0;

    function typeCharacter() {
      if (charIndex < outputText.length) {

        let char = outputText[charIndex];

        // check for the newline marker
        if (char == '[' && outputText.substring(charIndex, charIndex + 4) == '[BR]') {
          element.innerHTML += '<br>';
          charIndex += 4; //skip '[BR]'
        } else {
          //append the character
          element.innerHTML += char;
          charIndex++;
          // scroll to the bottom
          element.scrollTop = element.scrollHeight;
        }

        // scroll to the bottom
        element.scrollTop = element.scrollHeight;

        // schedule the next character print with delay
        setTimeout(typeCharacter, charDelay);

      } else {
        // allow input
        isPrinting = false;
        // add final break line
        element.innerHTML += '<br>';
        // scroll to the bottom
        element.scrollTop = element.scrollHeight;
        // resolve promise
        resolve();
      }
    }

    // start typing process
    typeCharacter();
  });
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

  if (data.display) {
    clearConsole();
    await printToConsole(data.display)
  }
  if (data.error) {
    let span = document.createElement("span")
    consoleDiv.appendChild(span)
    await printToConsole(data.error, span);
  }
  if (data.response) {
    await printToConsole(data.response);
  }
  if (data.next_action) {
    action = data.next_action;
  }
}