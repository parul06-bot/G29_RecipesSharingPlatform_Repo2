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

function toggleLike(recipeId, button) {
    fetch(`/recipe/${recipeId}/like/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        const icon = button.querySelector('i');
        const countSpan = button.querySelector('.likes-count');
        
        if (data.is_liked) {
            icon.classList.remove('far');
            icon.classList.add('fas');
            button.classList.add('liked');
        } else {
            icon.classList.remove('fas');
            icon.classList.add('far');
            button.classList.remove('liked');
        }
        
        if (countSpan) {
            countSpan.textContent = data.likes_count;
        }
    });
}

function toggleWishlist(recipeId, button) {
    fetch(`/recipe/${recipeId}/wishlist/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        const icon = button.querySelector('i');
        const countSpan = button.querySelector('.wishlist-count');
        
        if (data.is_wishlisted) {
            icon.classList.remove('far');
            icon.classList.add('fas');
            button.classList.add('wishlisted');
        } else {
            icon.classList.remove('fas');
            icon.classList.add('far');
            button.classList.remove('wishlisted');
        }
        
        if (countSpan) {
            countSpan.textContent = data.wishlist_count;
        }
    });
} 