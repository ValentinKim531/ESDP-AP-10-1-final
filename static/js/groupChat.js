document.addEventListener('DOMContentLoaded', function() {
    const avatarLink = document.querySelector('a[href^="/uploads/groupchats/"]');
    if (avatarLink) {
        const avatarText = avatarLink.previousSibling;
        avatarLink.style.display = 'none';
        if (avatarText && avatarText.textContent.includes('Currently:')) {
            avatarText.remove();
        }
    }

    const clearLabel = document.querySelector('label[for="avatar-clear_id"]');
    if (clearLabel) {
        clearLabel.textContent = 'Удалить';
    }

    const avatarDiv = document.querySelector('input[id="id_avatar"]').parentElement;
    if (avatarDiv) {
        avatarDiv.innerHTML = avatarDiv.innerHTML.replace(/Change:/, '');
    }

    const avatarInput = document.querySelector('input[id="id_avatar"]');
    const avatarImage = document.querySelector('.avatar-display .group-chat-avatar');

    avatarInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                avatarImage.src = e.target.result;
            }
            reader.readAsDataURL(file);
        }
    });
});
