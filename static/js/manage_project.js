// 모달 요소와 배경 요소 선택
const modalBackground = document.getElementById("modalBackground");
const projectModal = document.getElementById("projectModal");
const cancelButtons = document.querySelectorAll(".cancel-button");
const modalButtons = document.querySelectorAll("#modalButton");

// 모달 열기 함수
function openModal() {
  modalBackground.style.display = "block"; // 배경 보이기
  projectModal.style.display = "block"; // 모달 보이기
}

// 모달 닫기 함수
function closeModal() {
  modalBackground.style.display = "none"; // 배경 숨기기
  projectModal.style.display = "none"; // 모달 숨기기
}

// 모달 열기 버튼에 이벤트 리스너 추가
modalButtons.forEach((button) => {
  button.addEventListener("click", openModal);
});

// 취소 버튼에 이벤트 리스너 추가
cancelButtons.forEach((button) => {
  button.addEventListener("click", closeModal);
});

// 초기 설정: 모달과 배경 숨기기
modalBackground.style.display = "none";
projectModal.style.display = "none";
