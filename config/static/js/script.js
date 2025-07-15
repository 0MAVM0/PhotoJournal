let page = 2;
let loading = false;
const trigger = document.getElementById('load-trigger');
const postContainer = document.getElementById('post-container');
const loader = document.getElementById('loading');

const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting && !loading) {
        loadMorePosts();
    }
}, { threshold: 1 });

observer.observe(trigger);

function loadMorePosts() {
    loading = true;
    loader.style.display = 'block';

    fetch(`?page=${page}`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(res => res.json())
    .then(data => {
        if (data.html.trim().length === 0) {
            observer.disconnect();
        } else {
            postContainer.insertAdjacentHTML('beforeend', data.html);
            page += 1;
        }
    })
    .catch(err => console.error(err))
    .finally(() => {
        loading = false;
        loader.style.display = 'none';
    });
}

document.addEventListener('DOMContentLoaded', () => {
    document.body.addEventListener('submit', async function (e) {
        const form = e.target;

        if (form.classList.contains('like-form')) {
            e.preventDefault();
            const postId = form.dataset.postId;
            const response = await fetch(`/like/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const data = await response.json();
            if (response.ok) {
                form.querySelector('button').textContent = data.liked ? 'Unlike' : 'Like';
                form.querySelector('button').className = 'btn btn-sm ' + (data.liked ? 'btn-outline-danger' : 'btn-outline-primary');
                form.querySelector('.like-count').textContent = data.likes_count;
            }
        }

        if (form.classList.contains('comment-form')) {
            e.preventDefault();
            const postId = form.dataset.postId;
            const input = form.querySelector('input[name=content]');
            const content = input.value.trim();
            if (!content) return;

            const response = await fetch(`/comment/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: new URLSearchParams({ content })
            });
            const data = await response.json();
            if (response.ok) {
                const commentList = form.closest('.card-body').querySelector('.comment-list');
                const newComment = document.createElement('div');
                newComment.classList.add('mb-1');
                newComment.innerHTML = `<strong>${data.user}</strong>: ${data.content}`;
                commentList.prepend(newComment);
                const emptyNote = commentList.querySelector('p.text-muted');
                if (emptyNote) {
                    emptyNote.remove();
                }
                input.value = '';
            }
        }
    });
    document.body.addEventListener('click', async function (e) {
        // Edit comment
        if (e.target.matches('.btn-edit-comment')) {
            const commentId = e.target.dataset.id;
            const newContent = prompt("Edit your comment:");
            if (!newContent) return;
    
            const res = await fetch(`/comments/${commentId}/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ content: newContent })
            });
    
            const data = await res.json();
            if (res.ok) {
                const commentText = e.target.closest('.mb-1');
                commentText.innerHTML = `<strong>${data.user}</strong>: ${data.content}`;
            } else {
                alert(data.detail || 'Failed to edit comment');
            }
        }
    
        // Delete comment
        if (e.target.matches('.btn-delete-comment')) {
            const commentId = e.target.dataset.id;
            if (!confirm("Delete this comment?")) return;
    
            const res = await fetch(`/comments/${commentId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
    
            if (res.ok) {
                e.target.closest('.mb-1').remove();
            } else {
                alert('Failed to delete comment');
            }
        }
    });
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }    
});
