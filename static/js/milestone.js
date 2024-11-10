// 모달 요소와 배경 요소 선택
const modalBackground = document.getElementById("modalBackground");

// 마일스톤 라인 요소 선택
const line = document.getElementById("line");

// 완료된 부분을 표시할 div 생성
const completedSection = document.createElement("div");
completedSection.classList.add("completed-section");
completedSection.style.width = `${(completedMilestones / totalMilestones) * 100}%`;
line.appendChild(completedSection);

// 마일스톤 점 생성 및 배치
for (let i = 0; i < totalMilestones+1; i++) {
    const dot = document.createElement("div");
    dot.classList.add("milestone-dot");

    // 완료된 마일스톤 갯수만큼 초록색 적용
    if (i <= completedMilestones) {
        dot.classList.add("completed");

        // 마지막으로 완료된 점에 sprint.svg 아이콘 추가
        if (i == completedMilestones) {
          const sprintIcon = document.createElement("img");
          sprintIcon.src = "/static/icons/sprint.svg"; // sprint.svg 이미지 경로 설정
          sprintIcon.classList.add("sprint-icon");
          dot.appendChild(sprintIcon);
        }
    }

    // 점 위치 조정
    dot.style.left = `${(i / (totalMilestones)) * 100}%`;
    line.appendChild(dot);

    // 마지막 점에 milestone.svg 추가
    if (i == totalMilestones) {
        const milestoneIcon = document.createElement("img");
        milestoneIcon.src = "/static/icons/milestone.svg"; // milestone.svg 이미지 경로 설정
        milestoneIcon.classList.add("milestone-icon");
        dot.appendChild(milestoneIcon);
    }
}


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
document.getElementById("openMilestone").addEventListener("click", function () {
  openModal("createMilestoneModal");
});

document
  .getElementById("openModifyButton")
  .addEventListener("click", function () {
    openModal("modifyMilestoneModal");
  });

// 초기 설정: 모달과 배경 숨기기
modalBackground.style.display = "none";
