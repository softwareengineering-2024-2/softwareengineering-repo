// keywordList와 keywordWarningModal 요소 가져오기
const keywordWarningModal = document.getElementById("keywordWarningModal");
const keywordWarningBackground = document.getElementById("keywordWarningBackground");
const storyInputField = document.querySelector('.userstory-input-container input[name="content"]');
const editForms = document.querySelectorAll('.edit-input');

// 유저스토리 수정
function enableEdit(storyId) {
    var storyContent = document.getElementById('story-content-' + storyId);
    var editForm = document.getElementById('edit-form-' + storyId);
    storyContent.style.display = 'none';
    editForm.style.display = 'inline';
    var inputField = editForm.querySelector('input[name="content"]');
    inputField.focus();

    // Enter 키 이벤트 리스너 추가 및 이전 리스너 제거
    const handleEnterKeyPress = function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            checkForNotListKeywords(inputField.value.trim(), () => {
                inputField.removeEventListener('keypress', handleEnterKeyPress);
                editForm.submit();
            });
        }
    };

    inputField.removeEventListener('keypress', handleEnterKeyPress); // 중복 방지
    inputField.addEventListener('keypress', handleEnterKeyPress);
}

// 키워드 검증 및 모달 표시 함수
function checkForNotListKeywords(userStoryContent, submitCallback) {
    if (keywordList.some(keyword => userStoryContent.includes(keyword))) {
        openKeywordWarningModal(submitCallback);
    } else {
        submitCallback(); // 키워드가 없으면 폼을 바로 제출
    }
}

// 모달 열기 함수
function openKeywordWarningModal(confirmCallback) {
    keywordWarningModal.style.display = 'block';
    keywordWarningBackground.style.display = 'block';

    // 확인 버튼에 콜백 설정
    const handleConfirmClick = function() {
        closeKeywordWarningModal();
        confirmCallback();
        document.querySelector('.confirm-button').removeEventListener('click', handleConfirmClick); // 기존 이벤트 제거
    };

    document.querySelector('.confirm-button').addEventListener('click', handleConfirmClick);
}

// 모달 닫기 함수
function closeKeywordWarningModal() {
    keywordWarningModal.style.display = 'none';
    keywordWarningBackground.style.display = 'none';
}


// 유저스토리 입력 필드에 Enter 키 이벤트 추가
const handleInputEnterKeyPress = function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();  // 폼이 바로 제출되는 것을 막음
        checkForNotListKeywords(storyInputField.value.trim(), () => {
            storyInputField.removeEventListener('keypress', handleInputEnterKeyPress); // 중복 방지
            storyInputField.form.submit();
        });
    }
};

storyInputField.addEventListener('keypress', handleInputEnterKeyPress);

// 수정 입력 필드에 Enter 키 이벤트 추가
editForms.forEach(function(editForm) {
    const editInputField = editForm.querySelector('input[name="content"]');

    const handleEditEnterKeyPress = function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();  // 폼이 바로 제출되는 것을 막음
            checkForNotListKeywords(editInputField.value.trim(), () => {
                editInputField.removeEventListener('keypress', handleEditEnterKeyPress); // 중복 방지
                editForm.submit();
            });
        }
    };

    editInputField.addEventListener('keypress', handleEditEnterKeyPress);
});


// 유저스토리 텍스트 강조 함수
function highlightKeywordsInUserStories() {
    document.querySelectorAll('.userstory-item span[id^="story-content-"]').forEach(storyElement => {
        const originalContent = storyElement.textContent;
        const highlightedContent = highlightKeywords(originalContent);
        storyElement.innerHTML = highlightedContent;
    });
}

// 키워드 강조 로직
function highlightKeywords(storyContent) {
    // 키워드 리스트에 있는 각 단어를 찾고, 그 단어만 빨간색으로 강조
    keywordList.forEach(keyword => {
        const regex = new RegExp(`(${keyword})`, 'gi');
        storyContent = storyContent.replace(regex, '<span class="highlight-keyword">$1</span>');
    });
    return storyContent;
}

// 모달 내 버튼 동작 설정
document.querySelector('.confirm-button').addEventListener('click', function() {
    // 확인을 눌렀을 때 모달 닫기 및 폼 제출
    closeKeywordWarningModal();
    storyInputField.form.submit();  // 무시하고 추가 진행
});

document.querySelector('.cancel-button').addEventListener('click', function() {
    // 취소 버튼 클릭 시 모달 닫기
    closeKeywordWarningModal();
});

// 페이지 로드 시 유저스토리 텍스트를 강조
document.addEventListener('DOMContentLoaded', () => {
    highlightKeywordsInUserStories();
});