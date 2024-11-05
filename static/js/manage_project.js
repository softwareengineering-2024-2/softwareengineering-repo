// 모달 요소와 배경 요소 선택
const modalBackground = document.getElementById("modalBackground");

// 모달 열기 함수
function openModal(modalId) {
  document.getElementById(modalId).style.display = "block";
  modalBackground.style.display = "block";
}

// 모달 닫기 함수
function closeModal(modalId) {
  document.getElementById(modalId).style.display = "none";
  modalBackground.style.display = "none";
}

// 버튼 클릭 이벤트 리스너
document
  .getElementById("openCreateButton")
  .addEventListener("click", function () {
    openModal("createProjectModal");
  });

document
  .getElementById("openJoinButton")
  .addEventListener("click", function () {
    openModal("joinProjectModal");
  });

// 초기 설정: 모달과 배경 숨기기
modalBackground.style.display = "none";
