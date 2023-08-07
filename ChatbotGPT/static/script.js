const form = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatMessages = document.getElementById('chat-messages');

form.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = userInput.value;
    displayMessage(message, 'user');
    userInput.value = '';
    sendMessage(message);
});

function displayMessage(text, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    if (sender === 'user') {
        messageElement.classList.add('user-message');
    } else {
        messageElement.classList.add('assistant-message');
    }
    messageElement.innerText = text;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function sendMessage(message) {
    fetch('/get', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ msg: message })
    })
    .then(response => response.json())
    .then(data => {
        const reply = data.reply;
        displayMessage(reply, 'assistant');
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
