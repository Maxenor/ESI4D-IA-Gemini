// static/js/script.js
document.addEventListener('DOMContentLoaded', () => {
    const messagesContainer = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');

    // Display the initial messages
    displayMessage('Hello ! What would you like to know?', 'bot');

    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function displayMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message', sender);

        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.textContent = message;

        messageElement.appendChild(messageContent);
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function sendMessage() {
        const message = messageInput.value.trim();
        if (message === '') return;

        displayMessage(message, 'user');
        messageInput.value = '';

        fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        })
        .then(response => response.json())
        .then(data => {
            displayMessage(data.reply, 'bot');
        })
        .catch(error => {
            console.error('Error:', error);
            displayMessage('Sorry, there was an error processing your request.', 'bot');
        });
    }
});