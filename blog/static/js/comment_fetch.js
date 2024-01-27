import { getCookie } from "./get_cookie.js";

document.addEventListener("DOMContentLoaded", () => {
    const apiUrl = 'http://127.0.0.1:8000/api2/comments/';

    const fetchComments = async (postId) => {
        try {
            const response = await fetch(`${apiUrl}${postId}`);
            const comments = await response.json();

            const commentsContainer = document.getElementById(`comments-${postId}`);

            commentsContainer.innerHTML = '';

            // biome-ignore lint/complexity/noForEach: <explanation>
            comments.forEach(comment => {
                const commentElement = document.createElement('div');
                commentElement.classList.add('card', 'ml-2', 'my-2', 'p-2', 'card-no-border');

                commentElement.innerHTML = `
                    <div class="card-body">
                        <p class="card-text">${comment.content}</p>
                        <div class="d-flex justify-content-between">
                            <div class="d-flex flex-row align-items-center">
                                ${comment.user_photo ? `<img src="${comment.user_photo}" alt="avatar" width="25" height="25" />` : ''}
                                <p class="small mb-0 ms-2">${comment.author_name}</p>
                            </div>
                            <div class="d-flex flex-row align-items-center">
                                <p class="small text-muted mb-0">Like</p>
                                <i class="bi bi-hand-thumbs-up" style="margin-top: -0.16rem;"></i>
                            </div>
                        </div>
                    </div>
                `;

                commentsContainer.appendChild(commentElement);
            });
        } catch (error) {
            console.error('Error fetching comments:', error);
        }
    };

    document.body.addEventListener("click", async (event) => {
        const commentIcon = event.target.closest(".bi-chat-left-dots");
        if (commentIcon) {
            const postId = commentIcon.dataset.postId;
            await fetchComments(postId);
        }
    });
});
