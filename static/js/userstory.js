// keywordList와 keywordWarningModal 요소 가져오기
const keywordWarningModal = document.getElementById("keywordWarningModal");
const keywordWarningBackground = document.getElementById("keywordWarningBackground");
const storyInputField = document.querySelector('.userstory-input-container input[name="content"]');
const editForms = document.querySelectorAll('.edit-input');

document.addEventListener('DOMContentLoaded', function() {
    if (typeof messages !== 'undefined' && messages.length > 0) {
        messages.forEach(([category, message]) => {
            if (category === 'error') {
                openMessageModal("오류", message);
            } else if (category === 'success') {
                openMessageModal("성공", message);
            }
        });
    }
});
//삭제시 오류, 성공 메시지

// 유저스토리 수정
function enableEdit(storyId) {
    var storyContent = document.getElementById('story-content-' + storyId);
    var editForm = document.getElementById('edit-form-' + storyId);
    storyContent.style.display = 'none';
    editForm.style.display = 'inline';
    var inputField = editForm.querySelector('input[name="content"]');
    inputField.focus();

    const length = inputField.value.length;
    inputField.setSelectionRange(length, length);

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

// 알림 내용을 서버에 저장하는 함수
async function saveToDB(alertMessage) {
    try {
        const response = await fetch('/userstory/alert/save_alert_to_db', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: alertMessage ,
                project_id: project_id          
            })
        });
        
        // if (response.ok) {
        //     alert("알림이 저장되었습니다!");
        //     return true; // 성공 시 true 반환
        // } else {
        //     alert("알림 저장에 실패했습니다.");
        //     return false; // 실패 시 false 반환
        // }
    } catch (error) {
        console.error("Error:", error);
        alert("오류가 발생했습니다.");
        return false; // 오류 발생 시 false 반환
    }
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
document.querySelector('.confirm-button').addEventListener('click', async function() {
    const alertMessage = "키워드가 포함된 유저스토리가 있습니다.";
    const isSaved = await saveToDB(alertMessage); //saveToDB 함수 호출
    if (isSaved) {
        closeKeywordWarningModal();
    }
    // storyInputField.form.submit();
});

document.querySelector('.cancel-button').addEventListener('click', function() {
    // 취소 버튼 클릭 시 모달 닫기
    closeKeywordWarningModal();
});

// 페이지 로드 시 유저스토리 텍스트를 강조
document.addEventListener('DOMContentLoaded', () => {
    highlightKeywordsInUserStories();
});


function openMessageModal(title, message) {
    document.getElementById("modalTitle").textContent = title;
    document.getElementById("modalMessage").textContent = message;
    document.getElementById("messageModal").style.display = "flex";
}

function closeMessageModal() {
    document.getElementById("messageModal").style.display = "none";
}