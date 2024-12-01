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

// 온보딩 기능 추가
document.addEventListener("DOMContentLoaded", function () {
    // PM인지 여부를 확인
    const isPM = "{{ userproject.user_role }}" === "PM(기획자)";   
    // 온보딩 스텝 정의
    const onboardingSteps = [
        {
            element: document.querySelector(".not-list-box"),
            text: isPM
                ? "Not List는 프로젝트에서 금지된 키워드를 관리할 수 있습니다. 금지된 키워드를 수정, 삭제할 수 있습니다."
                : "Not List는 프로젝트에서 금지된 키워드를 확인할 수 있습니다.",
        },
        {
            element: document.querySelector(".notlist-input-container"),
            text: "여기에서 새로운 키워드를 입력하여 Not List에 추가할 수 있습니다.",
        },
        {
            element: document.querySelector(".userstory-container"),
            text: "유저스토리 섹션에서 사용자 스토리를 관리할 수 있습니다. 스토리를 수정하거나 삭제할 수 있습니다.",
        },
        {
            element: document.querySelector(".userstory-input-container"),
            text: "여기에서 새로운 유저스토리를 입력하여 추가할 수 있습니다.",
        },
    ];

    let currentStep = 0;

    const overlay = document.getElementById("onboarding-overlay");
    const tooltip = document.getElementById("onboarding-tooltip");
    const tooltipText = document.getElementById("onboarding-text");
    const nextButton = document.getElementById("onboarding-next-button");

    const showStep = (stepIndex) => {
        const step = onboardingSteps[stepIndex];
        if (!step) {
            endOnboarding();
            return;
        }

        const element = step.element;

        // 강조 스타일 적용
        if (element) {
            element.classList.add("onboarding-highlight");
        }

        // 툴팁 내용 설정
        tooltipText.innerHTML = step.text;

        // 툴팁 위치 설정
        const rect = element.getBoundingClientRect();
        tooltip.style.position = "absolute";
        tooltip.style.top = `${rect.bottom + window.scrollY + 10}px`;
        tooltip.style.left = `${Math.min(rect.left + window.scrollX, window.innerWidth - tooltip.offsetWidth - 10)}px`;
        // 버튼 텍스트 및 동작 변경
        if (stepIndex === onboardingSteps.length - 1) {
            nextButton.textContent = "완료"; // 버튼 텍스트를 "완료"로 변경
        } else {
            nextButton.textContent = "다음"; // 버튼 텍스트를 "다음"으로 설정
        }

        // 오버레이 표시
        overlay.classList.remove("hidden");
    };

    const hideStep = (stepIndex) => {
        const step = onboardingSteps[stepIndex];
        if (step && step.element) {
            step.element.classList.remove("onboarding-highlight");
        }
    };

    const nextStep = () => {
        hideStep(currentStep);
        currentStep++;
        showStep(currentStep);
    };

    const endOnboarding = () => {
        hideStep(currentStep);
        overlay.classList.add("hidden");
        document.cookie = "onboarding_done_userstory=true; path=/; max-age=31536000"; // 1년 유지
    };

    nextButton.addEventListener("click", nextStep);

    // 온보딩 초기화
    if (!document.cookie.includes("onboarding_done_userstory=true")) {
        showStep(currentStep);
    }
});
