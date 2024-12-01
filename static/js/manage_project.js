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
  modalBackground.style.display = "none";
}

// 나가기 확인 버튼 클릭 시 폼 제출
function submitExitForm() {
  document.getElementById("exitProjectForm").submit();
}

document.addEventListener("DOMContentLoaded", () => {
  const onboardingSteps = [
    {
      element: document.getElementById("openCreateButton"),
      text: "이 버튼은 프로젝트를 생성하는 버튼입니다.",
    },
    {
      element: document.getElementById("openJoinButton"),
      text: "프로젝트 코드를 받았다면 여기를 눌러주세요.",
    },
  ];

  const projectLists = document.getElementById("projectLists");

  // 임시 프로젝트 추가 함수
  const addTemporaryProject = () => {
    const tempProjectHTML = `
        <li class="project-list temp-project" style="list-style-type: none">
            <a href="#" id="tempProjectLink" class="temp-project-link">
                <p>TEST</p>
            </a>
            <div class="project-list-options">
                <button id="tempCopyLinkButton" class="temp-copy-link-button">
                    <p>링크복사</p>
                </button>
                <button id="tempSetProfileButton" class="temp-set-profile-button">
                    <p>프로필설정</p>
                </button>
                <button id="tempExitProjectButton" class="temp-exit-project-button">
                    <p>나가기</p>
                </button>
            </div>
        </li>`;
    projectLists.insertAdjacentHTML("beforeend", tempProjectHTML);

    // 임시 프로젝트의 버튼 요소를 온보딩 단계에 추가
    onboardingSteps.push(
      {
        element: document.getElementById("tempProjectLink"),
        text: "해당 프로젝트의 메인화면으로 이동합니다.",
      },
      {
        element: document.getElementById("tempCopyLinkButton"),
        text: "링크를 복사하여 팀원들에게 공유해주세요.",
      },
      {
        element: document.getElementById("tempSetProfileButton"),
        text: "해당 프로젝트에서 사용할 <br>닉네임 및 역할을 선택해주세요.",
      },
      {
        element: document.getElementById("tempExitProjectButton"),
        text: "해당 프로젝트를 나갈 수 있는 버튼입니다.",
      }
    );
  };

  const removeTemporaryProject = () => {
    const tempProject = document.querySelector(".temp-project");
    if (tempProject) {
      tempProject.remove();
    }
  };

  let currentStep = 0;
  const overlay = document.getElementById("onboarding-overlay");
  const tooltip = document.getElementById("onboarding-tooltip");
  const tooltipText = document.getElementById("onboarding-text");
  const nextButton = document.getElementById("onboarding-next-button");

  const startOnboarding = () => {
    overlay.classList.remove("hidden");
    addTemporaryProject();
    showStep(currentStep);
  };

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

      // 툴팁 위치 계산
      const rect = element.getBoundingClientRect();
      tooltipText.innerHTML = step.text;
      tooltip.style.top = `${rect.bottom + window.scrollY + 10}px`;
      tooltip.style.left = `${rect.left + window.scrollX}px`;
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
      // 이전 강조 스타일 제거
      previousStep.element.classList.remove("onboarding-highlight");
    }

    currentStep++;
    showStep(currentStep);
  };

  const endOnboarding = () => {
    overlay.classList.add("hidden");
    removeTemporaryProject();
    onboardingSteps.forEach((step) => {
      if (step.element) {
        step.element.classList.remove("onboarding-highlight");
      }
    });
  };

  nextButton.addEventListener("click", nextStep);

  // 첫 방문 시 온보딩 시작
  if (!document.cookie.includes("onboarding_done_manage_project=true")) {
    startOnboarding();
    document.cookie =
      "onboarding_done_manage_project=true; path=/; max-age=31536000"; // 1년간 유지
  }
});
