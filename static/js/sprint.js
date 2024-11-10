// 스프린트 네비게이션 함수
let currentSprintIndex = 1;

function navigateSprints(direction) {
  const sprints = document.querySelectorAll(".sprint-container");
  const navBtnLt = document.querySelector(".nav-btn-lt");
  const navBtnGt = document.querySelector(".nav-btn-gt");

  // 현재 스프린트를 숨기기
  sprints[currentSprintIndex - 1].style.display = "none";

  // 스프린트 인덱스 업데이트
  currentSprintIndex += direction;

  // 첫 번째와 마지막 스프린트에서 버튼을 숨김
  if (currentSprintIndex <= 1) {
    currentSprintIndex = 1;
    navBtnLt.style.display = "none"; // 첫 번째 스프린트에서는 왼쪽 버튼 숨김
  } else {
    navBtnLt.style.display = "flex"; // 첫 번째가 아니면 왼쪽 버튼 표시
  }

  if (currentSprintIndex >= sprints.length) {
    currentSprintIndex = sprints.length;
    navBtnGt.style.display = "none"; // 마지막 스프린트에서는 오른쪽 버튼 숨김
  } else {
    navBtnGt.style.display = "flex"; // 마지막이 아니면 오른쪽 버튼 표시
  }

  // 새로 선택된 스프린트 표시
  sprints[currentSprintIndex - 1].style.display = "block";
}

// 초기화 시 버튼 상태 설정
document.addEventListener("DOMContentLoaded", function() {
  const sprints = document.querySelectorAll(".sprint-container");
  const navBtnLt = document.querySelector(".nav-btn-lt");
  const navBtnGt = document.querySelector(".nav-btn-gt");

  // 스프린트가 없을 때 네비게이션 버튼 숨기기
  if (sprints.length === 0) {
      navBtnLt.style.display = "none";
      navBtnGt.style.display = "none";
  } else {
      // 스프린트가 있을 때 초기 상태 설정
      navigateSprints(0);
  }
});

// 스프린트 생성 모달 열기 함수
function openSprintCreateModal() {
  document.getElementById("sprint_create_modal").style.display = "flex";
}

// 스프린트 생성 모달 닫기 함수
function closeSprintCreateModal() {
  document.getElementById("sprint_create_modal").style.display = "none";
}

// 스프린트 백로그 생성 모달 열기 함수
function openSprintBacklogModal(sprintId, productBacklogId) {
  const form = document.getElementById("add-sprint-backlog-form");

  // 동적으로 URL 설정
  const actionUrl = `/sprint/create-sprint-backlog/${sprintId}/${productBacklogId}`;
  form.action = actionUrl;

  // 숨겨진 필드에 스프린트 ID와 백로그 ID 설정
  document.getElementById("sprint-backlog-sprint-id").value = sprintId;
  document.getElementById("sprint-backlog-product-id").value = productBacklogId;

  // 모달 표시
  document.getElementById("sprint_backlog_modal").style.display = "flex";
}

// 스프린트 백로그 생성 모달 닫기 함수
function closeSprintBacklogModal() {
  document.getElementById("sprint_backlog_modal").style.display = "none";
}

// 스프린트 백로그 추가 함수
function addSprintBacklog() {
  document.getElementById("add-sprint-backlog-form").submit();
  closeSprintBacklogModal();
}

/////////////////////////////////////////////////////////////////////////////////////
// 스프린트 설정 팝업 모달 열기/닫기
function toggleSprintOptionsModal(
  event,
  sprintId,
  sprintName,
  startDate,
  endDate,
  editUrl
) {
  const modal = document.getElementById("sprint-options-modal");
  modal.style.display = modal.style.display === "none" ? "block" : "none";
  // 팝업 모달의 위치를 버튼 왼쪽에 맞게 설정
  modal.style.top = event.clientY + "px";
  modal.style.left = event.clientX - modal.offsetWidth + "px";

  modal.dataset.sprintId = sprintId;
  document.getElementById("edit-sprint-btn").onclick = function () {
    openSprintEditModal(sprintId, sprintName, startDate, endDate, editUrl);
  };
  document.getElementById("edit-sprint-btn").onclick = function () {
    openSprintEditModal(sprintId, sprintName, startDate, endDate, editUrl);
  };
}

// 백로그 설정 팝업 모달 열기/닫기
function toggleBacklogOptionsModal(event, backlogId, content, userId) {
  const modal = document.getElementById("backlog-options-modal");
  modal.style.display = modal.style.display === "none" ? "block" : "none";

  // 팝업 모달 위치 설정
  modal.style.top = event.clientY + "px";
  modal.style.left = event.clientX - modal.offsetWidth + "px";

  const form = document.getElementById("edit-sprint-backlog-form");
  form.action = `/sprint/edit-backlog-details/${backlogId}`;

  // 수정 폼의 action과 필드 설정
  document.getElementById("edit-backlog-id").value = backlogId;
  document.getElementById("edit-backlog-name").value = content;
  document.getElementById("edit-assignee").value = userId;

  currentBacklogId = backlogId;
}
// Small modal 닫기 함수 (small 모달에서 수정시 small 모달이 안닫혀서 생성)
function closeSmallModal() {
  document.querySelectorAll(".small-modal").forEach((modal) => {
    modal.style.display = "none";
  });
}

// 스프린트 수정 모달 열기 함수
function openSprintEditModal(
  sprintId,
  sprintName,
  startDate,
  endDate,
  editUrl
) {
  closeSmallModal();

  document.getElementById("edit-sprint-id").value = sprintId;
  document.getElementById("edit-sprint-name").value = sprintName;
  document.getElementById("edit-sprint-start-date").value = startDate;
  document.getElementById("edit-sprint-end-date").value = endDate;

  // 폼 액션 URL 설정
  const editForm = document.getElementById("edit-sprint-form");
  editForm.action = editUrl;
  document.getElementById("sprint_edit_modal").style.display = "flex";
}

// 스프린트 수정 모달 닫기 함수
function closeSprintEditModal() {
  document.getElementById("sprint_edit_modal").style.display = "none";
}

function deleteSprint() {
  if (confirm("정말로 이 스프린트를 삭제하시겠습니까?")) {
    // 현재 스프린트의 ID를 가져옵니다 (이 ID는 toggleSprintOptionsModal 함수 호출 시 전달되어야 합니다)
    const sprintId = document.getElementById("sprint-options-modal").dataset
      .sprintId;

    // Ajax 요청을 통해 삭제 수행
    fetch(`/sprint/delete-sprint/${sprintId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": "{{ csrf_token() }}", // CSRF 보호를 위해 토큰 포함
      },
    })
      .then((response) => {
        if (response.ok) {
          alert("스프린트가 삭제되었습니다.");
          location.reload(); // 페이지 새로고침
        } else {
          alert("스프린트 삭제에 실패했습니다.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("스프린트 삭제 중 오류가 발생했습니다.");
      });
  }
  closeSprintOptionsModal();
}

// 스프린트 백로그 수정 모달 열기 함수
function openSprintBacklogEditModal() {
  closeSmallModal(); // small modal 닫기
  document.getElementById("sprint_backlog_edit_modal").style.display = "flex";
}

// 스프린트 백로그 수정 모달 닫기 함수
function closeSprintBacklogEditModal() {
  document.getElementById("sprint_backlog_edit_modal").style.display = "none";
}

// 스프린트 백로그 수정 저장 함수
function saveBacklogChanges() {
  document.getElementById("edit-sprint-backlog-form").submit();
  closeSprintBacklogEditModal();
}

function deleteBacklog() {
  if (currentBacklogId) {
    fetch(`/sprint/delete-backlog/${currentBacklogId}`, {
      method: "POST",
    })
      .then((response) => {
        if (response.ok) {
          window.location.reload();
        } else {
          alert("백로그 삭제에 실패했습니다.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("백로그 삭제 중 오류가 발생했습니다.");
      });
  }
  closeBacklogOptionsModal();
}

// 팝업 모달 닫기
function closeSprintOptionsModal() {
  document.getElementById("sprint-options-modal").style.display = "none";
}

function closeBacklogOptionsModal() {
  document.getElementById("backlog-options-modal").style.display = "none";
}

// 화면 클릭 시 팝업 모달 닫기
window.addEventListener("click", function (event) {
  const sprintOptionsModal = document.getElementById("sprint-options-modal");
  const backlogOptionsModal = document.getElementById("backlog-options-modal");

  if (
    !event.target.closest(".header-options-btn") &&
    !event.target.closest("#sprint-options-modal")
  ) {
    closeSprintOptionsModal();
  }
  if (
    !event.target.closest(".options-btn") &&
    !event.target.closest("#backlog-options-modal")
  ) {
    closeBacklogOptionsModal();
  }
});


// 스프린트가 없는 경우 nav-btn 숨기기
window.addEventListener("DOMContentLoaded", function() {
  const sprintContainerNone = document.querySelector(".sprint-container-none");
  const navButtons = document.querySelectorAll(".nav-btn");

  if (sprintContainerNone) {
      navButtons.forEach(button => {
          button.style.display = "none";
      });
  }
});
