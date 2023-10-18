function appendUserMessage(message) {
    appendMessage(message, 'student');
}

function appendLLMMessage(message) {
    appendMessage(message, 'ai');
}

function appendMessage(message, icon) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <img src="/static/img/${icon}.png" alt="${icon} Icon">
            <p>${message}</p>
        </div>
    `;

    document.getElementById('messages').appendChild(messageDiv);
    MathJax.Hub.Queue(["Typeset", MathJax.Hub, messageDiv]);

}


document.addEventListener('DOMContentLoaded', (event) => {
    const submitBtn = document.getElementById('submit-btn');
    const hintBtn = document.getElementById('hint-btn');
    const userInput = document.getElementById('user-input');
    const randomExerciseBtn = document.getElementById('random-exercise-btn');
    const newBtn = document.getElementById('new-btn');
    
    if (userInput) {
        userInput.addEventListener('input', () => {
            userInput.style.height = 'auto'; // To reset textarea height
            userInput.style.height = (userInput.scrollHeight - 20) + 'px';
        });

        // Trigger submit on Enter, allow Shift+Enter for new lines
        userInput.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                submitBtn.click();
            }
        });
    }

    if (newBtn) {
        newBtn.addEventListener('click', () => {
            window.location.href = '/new-task';
        });
    }

    if (submitBtn) {

        submitBtn.addEventListener('click', () => {
            const message = userInput.value.trim();
            if (message) {
                userInput.value = '';
                userInput.style.height = 'auto';  // Reset textarea height
                appendUserMessage(message);
                fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({
                        'student_answer': message
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.ta_answer) {
                        appendLLMMessage(data.ta_answer);
                    } else if (data.error) {
                        console.error('Error:', data.error);
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        });
    } else {
        console.error('submit-btn element not found');
    }

    if (hintBtn) {

        hintBtn.addEventListener('click', () => {
            fetch('/hint', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.hint) {
                    appendLLMMessage(data.hint);
                } else if (data.error) {
                    console.error('Error:', data.error);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    } else {
        console.error('submit-btn element not found');
    }

    if (randomExerciseBtn) {
        randomExerciseBtn.addEventListener('click', () => {
            window.location.href = '/random_exercise';
        });
    }

    document.getElementById('home-btn').addEventListener('click', () => {
        window.location.href = '/';
    });
});