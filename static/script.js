const inputField = document.getElementById('input');
const consoleDiv = document.getElementById('output');
var action = 'init';

window.onload = function () {
  sendInput()
};

inputField.addEventListener('keydown', function (e) {
  if (e.key === 'Enter') {
    const input = inputField.value;
    printToConsole(`> ${input} <br>`);
    sendInput(input);
    inputField.value = '';
  }
});

function printToConsole(text) {
  const formatted = text.replace(/\n/g, '<br>') + '<br>';
  consoleDiv.innerHTML += formatted;
  consoleDiv.scrollTop = consoleDiv.scrollHeight;
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