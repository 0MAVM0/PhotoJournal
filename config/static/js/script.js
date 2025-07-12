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
                input.value = '';
            }
        }
    });
});
