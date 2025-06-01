document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.vote-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const questionId = this.dataset.questionId;
            const voteType = this.dataset.voteType;
            
            fetch(`/question/${questionId}/vote/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `vote_type=${voteType}`
            })
            .then(response => response.json())
            .then(data => {
                document.querySelector(`#question-rating-${questionId}`).textContent = data.new_rating;
            });
        });
    });

    document.querySelectorAll('.mark-correct-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const answerId = this.dataset.answerId;
            const questionId = this.dataset.questionId;
            
            fetch(`/question/${questionId}/mark_correct/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `answer_id=${answerId}`
            })
            .then(response => {
                if (response.ok) {
                    location.reload();
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    alert(data.error);
                }
            });
        });
    });
});


document.querySelectorAll('.vote-answer-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const answerId = this.dataset.answerId;
        const voteType = this.dataset.voteType;
        
        fetch(`/answer/${answerId}/vote/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `vote_type=${voteType}`
        })
        .then(response => response.json())
        .then(data => {
            document.querySelector(`#answer-rating-${answerId}`).textContent = data.new_rating;
        });
    });
});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}