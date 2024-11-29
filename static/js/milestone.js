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
for (let i = 0; i <= totalMilestones; i++) {
    const dot = document.createElement("div");
    dot.classList.add("milestone-dot");

    // 완료된 마일스톤 갯수만큼 초록색 적용
    if (i <= completedMilestones) {
        dot.classList.add("completed");

        // 마지막으로 완료된 점에 sprint.svg 아이콘 추가
        if (i == completedMilestones && totalMilestones > 0) {
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
    if (i == totalMilestones && totalMilestones > 0) {
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

// 마일스톤 수정 버튼 리스너
// document.getElementById("openModifyButton").addEventListener("click", function () {
//     openModal("modifyMilestoneModal");
//   });

// 초기 설정: 모달과 배경 숨기기
modalBackground.style.display = "none";

function startOnboarding() {
  const onboardingSteps = [
    {
      element: document.querySelector(".milestone-line-container"),
      text: "마일스톤 타임라인에서 현재 진행 상황과 <br>완료된 마일스톤을 확인할 수 있어요.",
    },
    {
      element: document.querySelector(".milestone-list-container"),
      text: "여기에서 마일스톤 목록을 관리할 수 있습니다.",
    },
    {
      element: document.querySelector(".create-milstone-btn"),
      text: "새로운 마일스톤을 추가하려면 이 버튼을 클릭하세요.",
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

    if (element) {
      // 강조 스타일 적용
      element.classList.add("onboarding-highlight");

      // 툴팁 내용 설정
      tooltipText.innerHTML = step.text;

      // 툴팁 위치 계산
      const rect = element.getBoundingClientRect();
      const tooltipWidth = tooltip.offsetWidth;
      const tooltipHeight = tooltip.offsetHeight;
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;

      // 기본 위치 설정
      let tooltipTop = rect.bottom + window.scrollY + 10; // 요소 아래
      let tooltipLeft = rect.left + window.scrollX; // 요소 왼쪽

      // 화면 밖으로 나가는 경우 위치 조정
      if (tooltipLeft + tooltipWidth > viewportWidth) {
          tooltipLeft = viewportWidth - tooltipWidth - 10; // 화면 오른쪽 여백 유지
      }
      if (tooltipTop + tooltipHeight > viewportHeight) {
          tooltipTop = rect.top + window.scrollY - tooltipHeight - 10; // 요소 위로 이동
      }
      if (tooltipLeft < 0) {
          tooltipLeft = 10; // 화면 왼쪽 여백 유지
      }

      // 툴팁 위치 적용
      tooltip.style.position = "absolute";
      tooltip.style.top = `${tooltipTop}px`;
      tooltip.style.left = `${tooltipLeft}px`;
      // 버튼 텍스트 및 동작 변경
      if (stepIndex === onboardingSteps.length - 1) {
        nextButton.textContent = "완료"; // 버튼 텍스트를 "완료"로 변경
      } else {
        nextButton.textContent = "다음"; // 버튼 텍스트를 "다음"으로 설정
      }
  }
  };

  const nextStep = () => {
    const previousStep = onboardingSteps[currentStep];
    if (previousStep && previousStep.element) {
      previousStep.element.classList.remove("onboarding-highlight");
    }

    currentStep++;
    showStep(currentStep);
  };

  nextButton.addEventListener("click", nextStep);

  // 첫 방문 시 온보딩 시작
  if (!document.cookie.includes("onboarding_done_milestone=true")) {
    overlay.classList.remove("hidden");
    showStep(currentStep);
  }
}

document.addEventListener("DOMContentLoaded", function () {
  startOnboarding();
});

const endOnboarding = () => {
  // 툴팁과 오버레이를 숨깁니다.
  const overlay = document.getElementById("onboarding-overlay");
  const tooltip = document.getElementById("onboarding-tooltip");
  overlay.classList.add("hidden");
  tooltip.style.display = "none";

  // 온보딩이 끝난 상태를 저장 (쿠키 또는 로컬 스토리지)
  document.cookie = "onboarding_done_milestone=true; path=/; max-age=31536000"; // 1년 유지
};
