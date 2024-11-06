// 모달과 관련된 요소들 선택
const modalBackground = document.getElementById("modalBackground");
const notListModal = document.getElementById("notListModal");
const settingsIcon = document.querySelector(".settings-icon");
const newKeywordInput = document.getElementById("newKeywordInput");
const notListKeywordsDisplay = document.getElementById("notListKeywordsDisplay");
const modalKeywords = document.getElementById("modalKeywords");

// 모달 열기/닫기
settingsIcon.addEventListener("click", openModal);
modalBackground.addEventListener("click", closeModal);

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

// 키워드 추가 함수
function addKeyword(keyword) {
    if (keyword && !keywords.includes(keyword)) {
        keywords.push(keyword);
        renderKeywords();
        newKeywordInput.value = ""; // 입력 필드 초기화
    }
}

// 키워드 삭제 함수
function deleteKeyword(keyword) {
    keywords = keywords.filter(item => item !== keyword);
    renderKeywords();
}

// 키워드 목록 렌더링 함수
function renderKeywords() {
    // Not List와 모달창 모두에 키워드 표시 업데이트
    notListKeywordsDisplay.innerHTML = "";
    modalKeywords.innerHTML = "";

    keywords.forEach(keyword => {
        // Not List에 키워드 표시
        const keywordElem = document.createElement("span");
        keywordElem.className = "keyword";
        keywordElem.textContent = keyword;
        notListKeywordsDisplay.appendChild(keywordElem);

        // 모달창에 키워드 항목 표시
        const modalKeywordElem = document.createElement("div");
        modalKeywordElem.className = "modal-keyword-item";
        modalKeywordElem.innerHTML = `${keyword}`;

        // PM이면 키워드 삭제 버튼 표시
        if (projectRole === "PM") {
            const deleteBtn = document.createElement("span");
            deleteBtn.className = "delete";
            deleteBtn.textContent = "삭제";
            deleteBtn.onclick = () => deleteKeyword(keyword);
            modalKeywordElem.appendChild(deleteBtn);
        }

        modalKeywords.appendChild(modalKeywordElem);
    });
}

// 엔터키로 키워드 추가
newKeywordInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        const newKeyword = newKeywordInput.value.trim();
        addKeyword(newKeyword);
    }
});

// 초기 렌더링 호출
renderKeywords();
