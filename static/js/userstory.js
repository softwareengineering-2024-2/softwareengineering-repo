// 모달과 관련된 요소들 선택
const modalBackground = document.getElementById("modalBackground");
const notListModal = document.getElementById("notListModal");
const settingsIcon = document.querySelector(".settings-icon");
const newKeywordInput = document.getElementById("newKeywordInput");
const notListKeywordsDisplay = document.getElementById("notListKeywordsDisplay");
const modalKeywords = document.getElementById("modalKeywords");
const userStoryList = document.getElementById("userStoryList");
const newUserStoryInput = document.getElementById("newUserStoryInput");
const keywordWarningModal = document.getElementById("keywordWarningModal");
const keywordWarningBackground = document.getElementById("keywordWarningBackground");

// 유저 스토리 목록 배열
let userStories = [];

// 유저 스토리 렌더링 함수

function renderUserStories() {
    userStoryList.innerHTML = "";

    if (userStories.length === 0) {
        // 유저 스토리가 없을 때 안내 문구 추가
        const emptyMessage = document.createElement("p");
        emptyMessage.className = "empty-message-story";
        emptyMessage.textContent = "유저스토리를 입력하여 추가해보세요.";
        userStoryList.appendChild(emptyMessage);
    } else {
        userStories.forEach((story, index) => {
            const userStoryItem = document.createElement("div");
            userStoryItem.classList.add("userstory-item");

            if (story.editing) {
                // 수정 모드일 때는 원본 텍스트를 표시
                userStoryItem.innerHTML = `
                    <input type="text" value="${story.originalText || story.text}" class="edit-input">
                    <div class="buttons">
                        <button class="complete-edit" onclick="completeEdit(${index})">완료</button>
                        <button class="delete-story" onclick="deleteUserStory(${index})">삭제</button>
                    </div>
                `;
            } else {
                // 키워드 강조된 텍스트 표시
                userStoryItem.innerHTML = `
                    <span>${story.text}</span>
                    <div class="buttons">
                        <button class="edit-story" onclick="editUserStory(${index})">수정</button>
                        <button class="delete-story" onclick="deleteUserStory(${index})">삭제</button>
                    </div>
                `;
            }

            userStoryList.appendChild(userStoryItem);
        });
    }
}

// 엔터키로 유저 스토리 추가
newUserStoryInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        const newStory = newUserStoryInput.value.trim();
        addUserStory(newStory);
    }
});

// 유저 스토리 추가 함수
function addUserStory(storyText) {
    if (storyText) {
        if (checkForKeywords(storyText)) {
            // 키워드가 포함되어 있으면 경고 모달을 표시하고 텍스트를 임시 저장
            pendingUserStory = storyText;
            openKeywordWarningModal();
        } else {
            // 키워드가 없으면 바로 추가
            userStories.push({ text: storyText, editing: false });
            renderUserStories();
            newUserStoryInput.value = ""; // 입력 필드 초기화
        }
    }
}

// 키워드가 포함된 텍스트를 강조하는 함수
function highlightKeywords(text) {
    let highlightedText = text;
    keywords.forEach(keyword => {
        const keywordRegex = new RegExp(`(${keyword})`, 'gi');
        highlightedText = highlightedText.replace(keywordRegex, '<span class="highlight">$1</span>');
    });
    return highlightedText;
}

/*
// 유저 스토리 수정 모드 전환 함수
function editUserStory(index) {
    userStories[index].editing = true;
    renderUserStories();
}
    */

// 유저 스토리 수정 완료 함수
function completeEdit(index) {
    const editInput = userStoryList.querySelectorAll(".edit-input")[index];
    const updatedText = editInput.value;
    userStories[index].text = highlightKeywords(updatedText); // 키워드 강조 적용
    userStories[index].originalText = updatedText; // 원본 텍스트도 업데이트
    userStories[index].editing = false;
    renderUserStories();
}

// 유저 스토리 삭제 함수
function deleteUserStory(index) {
    userStories.splice(index, 1);
    renderUserStories();
}

function openModal() {
    modalBackground.style.display = "block";
    notListModal.style.display = "block";
}

function closeModal() {
    modalBackground.style.display = "none";
    notListModal.style.display = "none";
}

// 키워드 목록을 저장할 배열
let keywords = [];

// 엔터키로 키워드 추가
// newKeywordInput.addEventListener("keydown", (event) => {
//     if (event.key === "Enter") {
//         const newKeyword = newKeywordInput.value.trim();
//         addKeyword(newKeyword);
//     }
// });

// 키워드 추가 함수
// function addKeyword(keyword) {
//     if (keyword && !keywords.includes(keyword)) {
//         keywords.push(keyword);
//         renderKeywords();
//         newKeywordInput.value = ""; // 입력 필드 초기화
//     }
// }

// 키워드 삭제 함수
// function deleteKeyword(keyword) {
//     keywords = keywords.filter(item => item !== keyword);
//     renderKeywords();
// }

// 키워드 목록 렌더링 함수
// function renderKeywords() {
//     // Not List와 모달창 모두에 키워드 표시 업데이트
//     notListKeywordsDisplay.innerHTML = "";
//     modalKeywords.innerHTML = "";

//     if (keywords.length === 0) {
//         // 키워드가 없을 때 안내 문구 추가
//         const emptyMessage = document.createElement("p");
//         emptyMessage.className = "empty-message-key";
//         emptyMessage.textContent = "오른쪽 위 설정 버튼을 눌러 키워드를 추가하세요.";
//         notListKeywordsDisplay.appendChild(emptyMessage);
//     } else {
//         // 키워드가 있을 때 패딩 제거
//         notListKeywordsDisplay.style.padding = "0";
        
//         keywords.forEach(keyword => {
//             const keywordElem = document.createElement("span");
//             keywordElem.className = "keyword";
//             keywordElem.textContent = keyword;
//             notListKeywordsDisplay.appendChild(keywordElem);

//             const modalKeywordElem = document.createElement("div");
//             modalKeywordElem.className = "modal-keyword-item";
//             modalKeywordElem.innerHTML = `${keyword}`;

//             if (projectRole === "PM") {
//                 const deleteBtn = document.createElement("span");
//                 deleteBtn.className = "delete";
//                 deleteBtn.textContent = "삭제";
//                 deleteBtn.onclick = () => deleteKeyword(keyword);
//                 modalKeywordElem.appendChild(deleteBtn);
//             }

//             modalKeywords.appendChild(modalKeywordElem);
//         });
//     }
// }

let pendingUserStory = ""; // 임시로 저장할 유저 스토리 텍스트

// 키워드가 포함되었는지 확인하는 함수
function checkForKeywords(storyText) {
    return keywords.some(keyword => storyText.includes(keyword));
}

// 경고 모달 열기 함수
function openKeywordWarningModal() {
    keywordWarningModal.style.display = "block";
    keywordWarningBackground.style.display = "block";
}

// 경고 모달 닫기 함수
function closeKeywordWarningModal() {
    keywordWarningModal.style.display = "none";
    keywordWarningBackground.style.display = "none";
}

// 모달 확인 버튼 클릭 시 유저 스토리에 추가
function confirmKeywordWarning() {
    const highlightedText = highlightKeywords(pendingUserStory);
    userStories.push({ text: highlightedText, originalText: pendingUserStory, editing: false });
    renderUserStories();
    newUserStoryInput.value = ""; // 입력 필드 초기화
    closeKeywordWarningModal();
}


// 모달 취소 버튼 클릭 시 입력창에 그대로 텍스트 남기기
function cancelKeywordWarning() {
    newUserStoryInput.value = pendingUserStory;
    closeKeywordWarningModal();
}

// 초기 렌더링 호출
// renderKeywords();
renderUserStories();
