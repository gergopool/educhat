
document.addEventListener('DOMContentLoaded', (event) => {
    const form = document.getElementById('new-task-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        let taskName = document.getElementById('task-name').value;
        let taskDescription = document.getElementById('task-description').value;
        let taskSolution = document.getElementById('task-solution').value;
        let markingScheme = document.getElementById('marking-scheme').value;

        console.log("running");

        // Validation
        if (taskName.length <= 1) {
            alert('Task name must be longer than 1 character.');
            return;
        }
        if (!/^[\w]+$/.test(taskName)) {
            alert('Task name can only contain alphanumeric characters and underscores.');
            return;
        }
        if (taskDescription.length < 10 || taskSolution.length < 10 || markingScheme.length < 10) {
            alert('Task description, solution, and marking scheme must be at least 10 characters each.');
            return;
        }
        
        // Check if task name is unique
        fetch('/check-task-name', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                taskName: taskName,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.unique) {
                // If the task name is unique, send the form data to the server
                let formData = new FormData(document.getElementById('new-task-form'));
                fetch('/save-task', {
                    method: 'POST',
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // If the task was saved successfully, navigate to the success page
                        window.location.href = '/task-saved';
                    } else {
                        alert('Error saving task. Please try again.');
                    }
                });
            } else {
                alert('Task name already exists. Please choose another name.');
            }
        });
    });
});


