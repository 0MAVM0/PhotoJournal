document.addEventListener('DOMContentLoaded', () => {
    const likeButtons = document.querySelectorAll('.like-btn');
    const commentForms = document.querySelectorAll('.comment-form');
    const messageForms = document.querySelectorAll('.message-form');
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
                const heart = button.querySelector('i');
                heart.classList.toggle('text-red-500');
                heart.classList.add('animate-heart');
                setTimeout(() => heart.classList.remove('animate-heart'), 300);
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
                const comment = await response.json();
                const commentSection = form.previousElementSibling;
                const newComment = document.createElement('p');
                newComment.className = 'text-sm mb-2';
                newComment.innerHTML = `<strong>${comment.user}</strong> ${comment.content}`;
                commentSection.appendChild(newComment);
                form.querySelector('input[name="content"]').value = '';
            }
        });
    });

    messageForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const chatId = form.dataset.chatId;
            const content = form.querySelector('input[name="content"]').value;
            const response = await fetch(`/api/chats/${chatId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${sessionStorage.getItem('access_token')}`
                },
                body: JSON.stringify({ content })
            });
            if (response.ok) {
                const message = await response.json();
                const messageSection = form.previousElementSibling;
                const newMessage = document.createElement('div');
                newMessage.className = 'text-right mb-2';
                newMessage.innerHTML = `
                    <p class="inline-block p-2 rounded-lg bg-blue-100">${message.content}</p>
                    <p class="text-xs text-gray-500">${new Date().toLocaleString()}</p>
                `;
                messageSection.appendChild(newMessage);
                messageSection.scrollTop = messageSection.scrollHeight;
                form.querySelector('input[name="content"]').value = '';
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