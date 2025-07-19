document.addEventListener('DOMContentLoaded', () => {
    const likeButtons = document.querySelectorAll('.like-btn');
    const commentForms = document.querySelectorAll('.comment-form');
    const followButtons = document.querySelectorAll('.follow-btn');

    likeButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const postId = button.dataset.postId;
            const isLiked = button.dataset.liked === 'true';
            const method = isLiked ? 'DELETE' : 'POST';
            const response = await fetch(`/api/posts/${postId}/like/`, {
                method,
                headers: { 'Authorization': `Bearer ${sessionStorage.getItem('access_token')}` }
            });
            if (response.ok) {
                button.querySelector('i').classList.toggle('text-red-500');
                button.dataset.liked = !isLiked;
                const likesCount = button.nextElementSibling;
                likesCount.textContent = parseInt(likesCount.textContent) + (isLiked ? -1 : 1) + ' likes';
            }
        });
    });

    commentForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const postId = form.dataset.postId;
            const content = form.querySelector('input[name="content"]').value;
            const response = await fetch(`/api/posts/${postId}/comments/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${sessionStorage.getItem('access_token')}`
                },
                body: JSON.stringify({ content })
            });
            if (response.ok) {
                form.querySelector('input[name="content"]').value = '';
                location.reload(); // Temporary reload for simplicity
            }
        });
    });

    followButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const userId = button.dataset.userId;
            const isFollowing = button.dataset.following === 'true';
            const method = isFollowing ? 'DELETE' : 'POST';
            const response = await fetch(`/api/follows/${userId}/follow/`, {
                method,
                headers: { 'Authorization': `Bearer ${sessionStorage.getItem('access_token')}` }
            });
            if (response.ok) {
                button.textContent = isFollowing ? 'Follow' : 'Unfollow';
                button.dataset.following = !isFollowing;
            }
        });
    });
});