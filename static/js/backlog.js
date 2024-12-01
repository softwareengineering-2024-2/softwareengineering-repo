new Sortable(document.getElementById("userstoryLists"), {
  group: "shared",
  animation: 150,
  onEnd: function () {
    checkEmptyBacklogs();
  },
});

function initializeSortableBacklogBoxes() {
  document
    .querySelectorAll(".user-stories")
    .forEach(function (backlogUserStories) {
      new Sortable(backlogUserStories, {
        group: "shared",
        animation: 150,
        filter: ".backlog-title-wrapper", // title-wrapper 드래그 제외
        preventOnFilter: false, // 제외한 요소의 기본 동작 유지
        onAdd: function (event) {
          checkEmptyBacklogs();
        },
        onEnd: function () {
          checkEmptyBacklogs();
        },
      });
    });
}

initializeSortableBacklogBoxes();

function allowDrop(event) {
  event.preventDefault();
}

function drag(event) {
  event.dataTransfer.setData(
    "story_id",
    event.target.getAttribute("data-story-id")
  );
}

function drop(event) {
  event.preventDefault();
  const story_id = event.dataTransfer.getData("story_id");
  const storyElement = document.querySelector(
    `.user-story[data-story-id='${story_id}']`
  );

  if (storyElement) {
    const backlogBox = event.target.closest(".backlog-box");
    const backlogUserStories = event.target.closest(".user-stories");

    if (backlogBox) {
      // Find the .user-stories container inside the backlog box
      const userStoriesContainer = backlogBox.querySelector(".user-stories");

      // If .user-stories container exists, append the story element to it
      if (userStoriesContainer) {
        userStoriesContainer.appendChild(storyElement);
      } else {
        // If .user-stories doesn't exist, create it and append the story
        const newUserStoriesContainer = document.createElement("div");
        newUserStoriesContainer.classList.add("user-stories");
        newUserStoriesContainer.appendChild(storyElement);
        backlogBox.appendChild(newUserStoriesContainer);
      }
    } else {
      // If no backlog box is found, handle creating a new one if needed (this logic can be customized)
      const newBacklogBox = createNewBacklogBox();
      const userStoriesContainer = document.createElement("div");
      userStoriesContainer.classList.add("user-stories");
      userStoriesContainer.appendChild(storyElement);
      newBacklogBox.appendChild(userStoriesContainer);
      document.getElementById("backlogs").appendChild(newBacklogBox);
      initializeSortableBacklogBoxes();
    }

    checkEmptyBacklogs();
  }
}

function createNewBacklogBox() {
  const backlogBox = document.createElement("div");
  backlogBox.classList.add("backlog-box");
  backlogBox.setAttribute("data-backlog-id", Date.now());

  // 백로그 제목과 삭제 버튼을 하나로 묶을 컨테이너 생성
  const titleWrapper = document.createElement("div");
  titleWrapper.classList.add("backlog-title-wrapper");

  const inputField = document.createElement("input");
  inputField.type = "text";
  inputField.placeholder = "백로그 이름 입력";

  const deleteButton = document.createElement("button");
  deleteButton.innerText = "x";
  deleteButton.onclick = () => {
    const backlogId = backlogBox.getAttribute("data-backlog-id");
    if (backlogId) {
      // Move the user stories back to user-container
      const userStories = backlogBox.querySelectorAll(".user-story");
      userStories.forEach((story) => {
        document.getElementById("userstoryLists").appendChild(story);
      });
    }
    backlogBox.remove(); // Remove the backlog box
    checkEmptyBacklogs(); // Check for any empty backlog boxes to remove
  };

  // titleWrapper에 input과 deleteButton을 추가
  titleWrapper.appendChild(inputField);
  titleWrapper.appendChild(deleteButton);

  // backlogBox에 titleWrapper 추가
  backlogBox.appendChild(titleWrapper);

  document.getElementById("backlogs").appendChild(backlogBox);
  return backlogBox;
}

function checkEmptyBacklogs() {
  document.querySelectorAll(".backlog-box").forEach(function (box) {
    if (box.querySelectorAll(".user-story").length === 0) {
      const backlogId = box.getAttribute("data-backlog-id");
      if (backlogId) {
        deleteBacklog(backlogId, false);
      }
      box.remove();
    }
  });
}

function saveBacklogGroup() {
  const backlogGroups = Array.from(
    document.querySelectorAll(".backlog-box")
  ).map((box) => {
    const backlogName = box.querySelector("input").value.trim();
    const storyIds = Array.from(box.querySelectorAll(".user-story")).map(
      (story) => story.getAttribute("data-story-id")
    );
    const backlogId = box.getAttribute("data-backlog-id");
    return { backlogName, storyIds, backlogId };
  });

  const unassignedStoryIds = Array.from(
    document.querySelectorAll(".userstoryLists .user-story")
  ).map((story) => story.getAttribute("data-story-id"));

  for (const group of backlogGroups) {
    if (!group.backlogName) {
      alert("모든 백로그에는 이름이 필요합니다. 이름을 입력해 주세요.");
      return;
    }
  }

  fetch("/productbacklog/product_backlog/save_groups", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ backlogGroups, unassignedStoryIds }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("백로그 목록이 저장되었습니다.");
        location.reload();
      } else {
        alert("백로그 목록 저장에 실패하였습니다.");
      }
    });
}

function deleteBacklog(backlogId, shouldReload = true) {
  fetch(`/productbacklog/product_backlog/delete/${backlogId}`, {
    method: "DELETE",
  })
    .then((response) => response.json())
    .then((data) => {
      if (shouldReload) {
        location.reload();
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("서버와의 통신 중 문제가 발생했습니다.");
    });
}

document.querySelectorAll(".user-story").forEach((element) => {
  element.addEventListener("dragstart", drag);
});

function startOnboarding() {
  const onboardingSteps = [
    {
      element: document.querySelector("#userStories"),
      text: "이곳에서 유저스토리의 목록을 확인할 수 있습니다. <br>유저스토리를 드래그하여 백로그로 이동할 수 있습니다.",
    },
    {
      element: document.querySelector("#productBacklog"),
      text: "이곳은 백로그 섹션입니다. 유저스토리를 드래그하여 <br>백로그 그룹을 만들 수 있습니다.",
    },
    {
      element: document.querySelector(".save-btn"),
      text: "변경 사항을 저장하려면 이 버튼을 클릭하세요. <br>버튼을 누르지 않고 다른 페이지로 이동하면 <br>저장되지 않습니다.",
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
  
      let tooltipTop, tooltipLeft;
  
      // 단계별 위치 설정
      if (stepIndex === 0) {
        // 유저스토리 목록 - 오른쪽으로 배치
        tooltipTop = rect.top + window.scrollY;
        tooltipLeft = rect.right + 10;
      } else if (stepIndex === 1) {
        // 프로덕트 백로그 - 왼쪽으로 배치
        tooltipTop = rect.top + window.scrollY;
        tooltipLeft = rect.left - tooltipWidth - 10;
      } else if (stepIndex === 2) {
        // 저장 버튼 - 아래쪽으로 배치
        tooltipTop = rect.bottom + window.scrollY + 10;
        tooltipLeft = rect.left + window.scrollX;
      } else {
        // 기본 위치 - 요소 아래쪽
        tooltipTop = rect.bottom + window.scrollY + 10;
        tooltipLeft = rect.left + window.scrollX;
      }
  
      // 화면 밖으로 나가는 경우 위치 조정
      if (tooltipLeft + tooltipWidth > viewportWidth) {
        tooltipLeft = viewportWidth - tooltipWidth - 10;
      }
      if (tooltipTop + tooltipHeight > viewportHeight) {
        tooltipTop = rect.top + window.scrollY - tooltipHeight - 10;
      }
      if (tooltipLeft < 0) {
        tooltipLeft = 10;
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
  if (!document.cookie.includes("onboarding_done_backlog=true")) {
    overlay.classList.remove("hidden");
    showStep(currentStep);
  }
}

const endOnboarding = () => {
  // 툴팁과 오버레이를 숨깁니다.
  const overlay = document.getElementById("onboarding-overlay");
  const tooltip = document.getElementById("onboarding-tooltip");
  overlay.classList.add("hidden");
  tooltip.style.display = "none";

  // 온보딩이 끝난 상태를 저장 (쿠키 또는 로컬 스토리지)
  document.cookie = "onboarding_done_backlog=true; path=/; max-age=31536000"; // 1년 유지
};

document.addEventListener("DOMContentLoaded", function () {
  startOnboarding();
});
