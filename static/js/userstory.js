// 유저스토리 수정
function enableEdit(storyId) {
    var storyContent = document.getElementById('story-content-' + storyId);
    var editForm = document.getElementById('edit-form-' + storyId);
    storyContent.style.display = 'none';
    editForm.style.display = 'inline';
    var inputField = editForm.querySelector('input[name="content"]');
    inputField.focus();
    inputField.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            editForm.submit();
        }
    });
}