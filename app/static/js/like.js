document.addEventListener("DOMContentLoaded", () => {
    const likeButton = document.getElementById('like_button');

    const addLike = (name) => {
        if (!name) return;

    sendToServer({ like_id: name }, "/post-order-like");

        // updateClasses(selector, classListToAdd = [], classListToRemove = [])
        updateClasses('.white-like', ['hidden'], ['block']);
        updateClasses('.black-like', ['block'], ['hidden']);
    };

    if (likeButton) {
        likeButton.addEventListener('click', () => {
            const name = likeButton.dataset.name;
            if (name) {
                addLike(name);
            } else {
                console.warn("No 'data-name' attribute found on like button.");
            }
        });
    }

    document.querySelectorAll('.closer').forEach(button => {
        button.addEventListener('click', () => window.close());
    });
});
