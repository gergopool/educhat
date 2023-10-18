
function loadTopics() {
    fetch('/topics')
        .then(response => response.json())
        .then(data => {
            const taskList = document.getElementById('task-list');
            data.topics.forEach(topic => {
                const topicDiv = document.createElement('div');
                topicDiv.className = 'topic';
                topicDiv.onclick = () => selectTopic(topic.folder);
                topicDiv.innerHTML = `
                    <img src="/static/img/${topic.icon}" alt="${topic.name} Icon">
                    <p>${topic.name}</p>
                `;
                taskList.appendChild(topicDiv);
            });
        })
        .catch(error => console.error('Error fetching topics:', error));
}

function selectTopic(topic) {
    fetch('/select_topic', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'topic': topic
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/random_exercise';
        } else {
            alert(data.error);
        }
    });
}


document.addEventListener('DOMContentLoaded', (event) => {
    loadTopics();
    document.getElementById('random-exercise-btn').addEventListener('click', () => {
        window.location.href = '/random_exercise';
    });
});