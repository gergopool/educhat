document.addEventListener('DOMContentLoaded', (event) => {
    const submitBtn = document.getElementById('submit-btn');
    if (submitBtn) {
        submitBtn.addEventListener('click', () => {
            const userAnswer = document.getElementById('user-input').value;
            console.log("Aha")
            fetch('/evaluate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    'student_answer': userAnswer
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.evaluation) {
                    document.getElementById('solution-feedback-area').innerHTML = data.evaluation;
                    // Refresh MathJax rendering in case the evaluation contains LaTeX
                    MathJax.typeset();
                } else if (data.error) {
                    console.error('Error:', data.error);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    } else {
        console.error('submit-btn element not found');
    }
});