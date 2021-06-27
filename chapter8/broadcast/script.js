const addMessage = (message, username, sender) => {
  const messages = document.getElementById('messages');

  const messageItem = document.createElement('li');
  messageItem.innerHTML = `<strong>${username}</strong> ${message}`;
  if (sender === 'client') {
    messageItem.setAttribute('class', 'text-success');
  } else {
    messageItem.setAttribute('class', 'text-warning');
  }

  messages.appendChild(messageItem);
};

const connectWebSocket = (username) => {
  document.cookie = 'token=SECRET_API_TOKEN';
  const socket = new WebSocket(`ws://localhost:8000/ws?username=${username}`);

  // Connection opened
  socket.addEventListener('open', function (event) {
    document.getElementById('message').removeAttribute('disabled');
    document.getElementById('button-send').removeAttribute('disabled');
    document.getElementById('username').setAttribute('disabled', 'true');
    document.getElementById('button-connect').setAttribute('disabled', 'true');

    // Send message on form submission
    document.getElementById('form-send').addEventListener('submit', (event) => {
      event.preventDefault();
      const message = document.getElementById('message').value;

      addMessage(message, username, 'client');

      socket.send(message);

      event.target.reset();
    });
  });

  // Listen for messages
  socket.addEventListener('message', function (event) {
    const { message, username } = JSON.parse(event.data);
    addMessage(message, username, 'server');
  });
}

window.addEventListener('DOMContentLoaded', (event) => {
  document.getElementById('form-connect').addEventListener('submit', (event) => {
    event.preventDefault();
    const username = document.getElementById('username').value;
    connectWebSocket(username);
  });
});
