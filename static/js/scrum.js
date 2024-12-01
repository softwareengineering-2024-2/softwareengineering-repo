// 드래그가 가능한 항목을 끌 때 발생하는 이벤트
function drag(ev) {
  ev.dataTransfer.setData("text", ev.target.id); // 드래그된 요소의 ID를 저장
  ev.dataTransfer.setDragImage(ev.target, 0, 0); // 원본 요소를 그대로 표시
}

// 드롭이 가능한 구역에 드래그된 항목이 올 때 발생하는 이벤트
function allowDrop(ev) {
  ev.preventDefault(); // 기본 동작을 방지하여 드롭을 허용
}

// 항목을 드롭했을 때 발생하는 이벤트
function drop(ev) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData("text"); // 드래그된 항목의 ID 가져오기
  var draggedItem = document.getElementById(data); // ID로 요소를 찾기
  var dropTarget = ev.target; // 드롭된 위치를 찾기

  // 드롭된 위치가 scrum-content 영역인지 확인
  while (dropTarget && !dropTarget.classList.contains("scrum-content")) {
    dropTarget = dropTarget.parentNode; // 부모 요소로 이동하여 scrum-content 확인
  }

  // 드롭 대상이 scrum-content이고, 드래그된 항목이 해당 scrum-content의 자식이 아닐 경우 항목을 추가
  if (dropTarget && dropTarget !== draggedItem.parentNode) {
    dropTarget.appendChild(draggedItem); // 드래그된 항목을 드롭된 scrum-content에 추가
    // 상태 업데이트
    var newStatus = dropZone.id.replace("-", " ").titleCase();
    var backlogId = draggedItem.getAttribute("data-backlog-id");

    // 서버에 상태 업데이트 요청 보내기
    fetch("/update_sprint_backlog_status", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrf_token"), // CSRF 토큰이 필요한 경우
      },
      body: JSON.stringify({
        backlog_id: backlogId,
        new_status: newStatus,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (!data.success) {
          alert("상태 업데이트에 실패했습니다.");
          location.reload();
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("상태 업데이트 중 오류가 발생했습니다.");
        location.reload();
      });
  }
}

// 각 scrum-sprint-item 요소에 드래그 이벤트 핸들러 추가
document.querySelectorAll(".scrum-sprint-item").forEach((item) => {
  item.addEventListener("dragstart", drag); // 드래그 시작 시
});

// 각 scrum-content 영역에 드롭 이벤트 핸들러 추가
document.querySelectorAll(".scrum-content").forEach((content) => {
  content.addEventListener("dragover", allowDrop); // 드래그 오버 시
  content.addEventListener("drop", drop); // 드롭 시
});

document.addEventListener("DOMContentLoaded", () => {
  const scrumContents = document.querySelectorAll(".scrum-content");

  scrumContents.forEach((scrumContent) => {
    let draggedItem = null;

    // 드래그 시작
    scrumContent.addEventListener("dragstart", (event) => {
      draggedItem = event.target; // 드래그 중인 요소 저장
    });

    // 드래그 종료
    scrumContent.addEventListener("dragend", (event) => {
      event.target.style.opacity = "1"; // 반투명 복원
      draggedItem = null; // 드래그 요소 초기화
    });

    // 드래그 중 요소가 다른 요소 위로 올 때
    scrumContent.addEventListener("dragover", (event) => {
      event.preventDefault(); // 기본 동작 방지
      const target = event.target;

      // 현재 대상이 드래그 가능한 아이템인지 확인
      if (
        target &&
        target !== draggedItem &&
        target.classList.contains("scrum-sprint-item")
      ) {
        const bounding = target.getBoundingClientRect();
        const offset = event.clientY - bounding.top;

        // 마우스 위치에 따라 위/아래로 이동
        if (offset > bounding.height / 2) {
          target.parentNode.insertBefore(draggedItem, target.nextSibling); // 아래로 이동
        } else {
          target.parentNode.insertBefore(draggedItem, target); // 위로 이동
        }
      }
    });

    // 드롭 처리
    scrumContent.addEventListener("drop", (event) => {
      event.preventDefault(); // 기본 동작 방지
    });
  });
});

// 스프린트 변경 함수
function changeSprint(sprint_id) {
  const urlParams = new URLSearchParams(window.location.search);
  urlParams.set("sprint_id", sprint_id);
  window.location.search = urlParams.toString();
}

// 스프린트 드롭다운 토글 함수
function toggleSprintDropdown() {
  const dropdowns = document.getElementsByClassName("sprint-dropdown");
  if (dropdowns.length > 0) {
    const dropdown = dropdowns[0];
    dropdown.classList.toggle("show");
  } else {
    console.error("No dropdown elements found.");
  }
}

// 드롭다운 외부 클릭 시 닫기
window.onclick = function (event) {
  const dropdown = document.getElementById("sprintDropdown");
  if (
    !event.target.matches(".sprint-change-btn") &&
    !event.target.closest(".sprint-change-btn") &&
    dropdown.classList.contains("show")
  ) {
    dropdown.classList.remove("show");
  }
};

// 문자열의 첫 글자를 대문자로 변환하는 함수
String.prototype.titleCase = function () {
  return this.toLowerCase()
    .split(" ")
    .map(function (word) {
      return word.replace(word[0], word[0].toUpperCase());
    })
    .join(" ");
};

function saveStatuses() {
  // 모든 백로그 아이템의 현재 상태를 수집합니다.
  var updatedBacklogs = [];
  document.querySelectorAll(".scrum-sprint-item").forEach(function (item) {
    var backlogId = item.getAttribute("data-backlog-id");
    var parentColumn = item.parentElement;
    var status = "";
    if (parentColumn.id === "to-do") {
      status = "To Do";
    } else if (parentColumn.id === "in-progress") {
      status = "In Progress";
    } else if (parentColumn.id === "done") {
      status = "Done";
    }
    updatedBacklogs.push({
      backlog_id: backlogId,
      new_status: status,
    });
  });

  // 서버에 업데이트된 상태를 전송합니다.
  fetch("/scrum/update_sprint_backlog_statuses", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      updated_backlogs: updatedBacklogs,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("상태가 성공적으로 저장되었습니다.");
        // 필요하다면 페이지를 새로고침하거나 추가 작업을 수행합니다.
      } else {
        alert("상태 저장에 실패했습니다: " + data.message);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("상태 저장 중 오류가 발생했습니다.");
    });
}

function startOnboarding() {
  const onboardingSteps = [
    {
      element: document.querySelector(".sprint-change-btn"),
      text: "스프린트를 선택하려면 이 버튼을 클릭하세요.",
      tooltipPosition: "bottom", // 툴팁 위치
    },
    {
      element: document.querySelector(".save-button"),
      text: "현재 스프린트의 상태를 저장할 수 있습니다.",
      tooltipPosition: "bottom", // 툴팁 위치
    },
    {
      element: document.querySelector(".sprint-percentage-container"),
      text: "현재 스프린트의 작업 진도율을 확인할 수 있습니다.",
      tooltipPosition: "top", // 툴팁 위치
    },
    {
      element: document.querySelector(".scrum-board-container"),
      text: "각각의 스프린트 백로그 진행 상태를 드래그를 통해 <br>이동시켜 관리할 수 있습니다.",
      tooltipPosition: "top", // 툴팁 위치
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

      let tooltipTop, tooltipLeft;

      switch (step.tooltipPosition) {
        case "top":
          tooltipTop = rect.top - tooltipHeight - 10;
          tooltipLeft = rect.left + rect.width / 2 - tooltipWidth / 2;
          break;
        case "bottom":
          tooltipTop = rect.bottom + 10;
          tooltipLeft = rect.left + rect.width / 2 - tooltipWidth / 2;
          break;
        case "left":
          tooltipTop = rect.top + rect.height / 2 - tooltipHeight / 2;
          tooltipLeft = rect.left - tooltipWidth - 10;
          break;
        case "right":
          tooltipTop = rect.top + rect.height / 2 - tooltipHeight / 2;
          tooltipLeft = rect.right + 10;
          break;
        default:
          tooltipTop = rect.bottom + 10;
          tooltipLeft = rect.left + rect.width / 2 - tooltipWidth / 2;
          break;
      }

      // 화면 밖으로 나가는 경우 조정
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;

      if (tooltipLeft + tooltipWidth > viewportWidth) {
        tooltipLeft = viewportWidth - tooltipWidth - 10;
      }
      if (tooltipTop + tooltipHeight > viewportHeight) {
        tooltipTop = rect.top - tooltipHeight - 10;
      }
      if (tooltipLeft < 0) {
        tooltipLeft = 10;
      }
      if (tooltipTop < 0) {
        tooltipTop = rect.bottom + 10;
      }

      // 툴팁 위치 적용
      tooltip.style.top = `${tooltipTop}px`;
      tooltip.style.left = `${tooltipLeft}px`;
    }
  };

  const nextStep = () => {
    const previousStep = onboardingSteps[currentStep];
    if (previousStep && previousStep.element) {
      previousStep.element.classList.remove("onboarding-highlight");
    }

    currentStep++;
    if (currentStep < onboardingSteps.length - 1) {
      nextButton.innerText = "다음"; // 다음 버튼
    } else if (currentStep === onboardingSteps.length - 1) {
      nextButton.innerText = "완료"; // 마지막 단계에서 완료 버튼
    }

    showStep(currentStep);
  };

  nextButton.addEventListener("click", nextStep);

  // 첫 방문 시 온보딩 시작
  if (!document.cookie.includes("onboarding_done_scrum=true")) {
    overlay.classList.remove("hidden");
    showStep(currentStep);
  }
}

const endOnboarding = () => {
  const overlay = document.getElementById("onboarding-overlay");
  const tooltip = document.getElementById("onboarding-tooltip");
  overlay.classList.add("hidden");
  tooltip.style.display = "none";

  // 온보딩 완료 상태 저장
  document.cookie = "onboarding_done_scrum=true; path=/; max-age=31536000"; // 1년 유지
};

document.addEventListener("DOMContentLoaded", function () {
  startOnboarding();
});
