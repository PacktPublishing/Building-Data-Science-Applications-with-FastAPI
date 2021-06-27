const addMessage = (message, sender) => {
  const messages = document.getElementById('messages');

  const messageItem = document.createElement('li');
  messageItem.innerText = message;
  if (sender === 'client') {
    messageItem.setAttribute('class', 'text-success');
  } else {
    messageItem.setAttribute('class', 'text-warning');
  }

  messages.appendChild(messageItem);
};

window.addEventListener('DOMContentLoaded', (event) => {
  const socket = new WebSocket('ws://localhost:8000/ws');

  // Connection opened
  socket.addEventListener('open', function (event) {

    // Send message on form submission
    document.getElementById('form').addEventListener('submit', (event) => {
      event.preventDefault();
      const message = document.getElementById('message').value;

      addMessage(message, 'client');

      socket.send(message);

      event.target.reset();
    });
  });

  // Listen for messages
  socket.addEventListener('message', function (event) {
    addMessage(event.data, 'server');
  });
});
