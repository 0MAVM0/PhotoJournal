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
            observer.disconnect(); // больше нечего грузить
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
