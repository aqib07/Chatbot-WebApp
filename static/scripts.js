$(document).ready(function() {
    $('#send-button').click(function() {
        sendMessage();
    });

    $('#message-input').keypress(function(e) {
        if (e.which == 13) {
            sendMessage();
        }
    });

    function sendMessage() {
        const message = $('#message-input').val().trim();
        if (message === '') {
            alert('Please enter a message.');
            return;
        }

        appendMessage('user', message);
        $('#message-input').val('');

        $.ajax({
            url: '/get_response',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({'message': message}),
            success: function(response) {
                appendMessage('bot', response.response);
            },
            error: function() {
                appendMessage('bot', 'Sorry, there was an error processing your request.');
            }
        });
    }

    function appendMessage(sender, message) {
        const messageElement = $('<div>').addClass('message');
        messageElement.addClass(sender === 'user' ? 'user-message' : 'bot-message');
        messageElement.text(message);
        $('#chat-window').append(messageElement);
        $('#chat-window').scrollTop($('#chat-window')[0].scrollHeight);
    }
});
