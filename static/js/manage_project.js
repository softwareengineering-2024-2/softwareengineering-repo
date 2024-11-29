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

document.addEventListener("DOMContentLoaded", function () {
  const exitButtons = document.querySelectorAll(".exit-button");

  exitButtons.forEach((button) => {
    button.addEventListener("click", function (event) {
      event.preventDefault(); // 폼 제출 방지
      const projectName = this.closest("li").querySelector("p").textContent; // 프로젝트 명 가져오기
      openExitModal(projectName);
    });
  });
});

let currentProjectName = "";

// 나가기 모달 열기
function openExitProjectModal(event) {
  event.preventDefault(); // 폼 제출 방지
  document.getElementById("exitProjectModal").style.display = "block";
}

// 모달 닫기
function closeModal(modalId) {
  document.getElementById(modalId).style.display = "none";
}

// 나가기 확인 버튼 클릭 시 폼 제출
function submitExitForm() {
  document.getElementById("exitProjectForm").submit();
}
