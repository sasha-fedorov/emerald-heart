const input = document.getElementById('input');
const consoleDiv = document.getElementById('output');

input.addEventListener('keydown', function (e) {
  if (e.key === 'Enter') {
    const command = input.value;
    printToConsole(`> ${command}`);
    sendCommand(command);
    input.value = '';
  }
});

function printToConsole(text) {
  consoleDiv.innerHTML += text + '<br>';
  consoleDiv.scrollTop = consoleDiv.scrollHeight;
}

async function sendCommand(command) {
  const res = await fetch('/command', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      command
    })
  });
  const data = await res.json();
  if (data.response)
    printToConsole(data.response);
}