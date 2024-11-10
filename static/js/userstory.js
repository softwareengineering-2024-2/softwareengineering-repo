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
    inputField.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            editForm.submit();
        }
    });
}

// 키워드 검증 및 모달 표시 함수
function checkForNotListKeywords(userStoryContent) {
    return keywordList.some(keyword => userStoryContent.includes(keyword));
}

// 모달 열기 함수
function openKeywordWarningModal() {
    keywordWarningModal.style.display = 'block';
    keywordWarningBackground.style.display = 'block';
}

// 모달 닫기 함수
function closeKeywordWarningModal() {
    keywordWarningModal.style.display = 'none';
    keywordWarningBackground.style.display = 'none';
}


// 유저스토리 입력 필드에 Enter 키 이벤트 추가
storyInputField.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();  // 폼이 바로 제출되는 것을 막음
        const userStoryContent = storyInputField.value.trim();
        
        // 키워드 검증 및 모달 표시
        if (checkForNotListKeywords(userStoryContent)) {
            openKeywordWarningModal();
        } else {
            // 키워드가 없으면 유저스토리 추가 폼 제출
            storyInputField.form.submit();
        }
    }
});

// 수정 입력 필드에 Enter 키 이벤트 추가
editForms.forEach(function(editForm) {
    const editInputField = editForm.querySelector('input[name="content"]');
    editInputField.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();  // 폼이 바로 제출되는 것을 막음
            const editedContent = editInputField.value.trim();
            
            // 키워드 검증 및 모달 표시
            if (checkForNotListKeywords(editedContent)) {
                openKeywordWarningModal();

                // 모달 내 확인 버튼 동작: 모달 닫고 폼 제출
                document.querySelector('.confirm-button').onclick = function() {
                    closeKeywordWarningModal();
                    editForm.submit();  // 수정 내용 폼 제출
                };
            } else {
                editForm.submit();  // 키워드가 없으면 폼 제출
            }
        }
    });
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