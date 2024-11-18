// 드래그가 가능한 항목을 끌 때 발생하는 이벤트
function drag(ev) {
  ev.dataTransfer.setData("text", ev.target.id); // 드래그된 요소의 ID를 저장
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
  }
}

// 각 scrum-sprint-item 요소에 드래그, 드롭 이벤트 핸들러 추가
document.querySelectorAll(".scrum-sprint-item").forEach((item) => {
  item.addEventListener("dragstart", function (event) {
    drag(event); // 드래그 시작 시
  });
});

// 각 scrum-content 영역에 allowDrop 이벤트 핸들러 추가
document.querySelectorAll(".scrum-content").forEach((content) => {
  content.addEventListener("dragover", function (event) {
    allowDrop(event); // 드래그오버 시
  });
  content.addEventListener("drop", function (event) {
    drop(event); // 드롭 시
  });
});

// 드롭다운 토글 함수
function toggleSprintDropdown() {
  var dropdown = document.getElementById("sprintDropdown");

  // 드롭다운 메뉴 토글
  if (dropdown.style.display === "block") {
    dropdown.style.display = "none";
  } else {
    dropdown.style.display = "block";
  }
}

// 페이지가 로드된 후 이벤트 리스너 추가
document.addEventListener("DOMContentLoaded", function () {
  var sprintChangeBtn = document.querySelector(".sprint-change-btn");

  // sprintChangeBtn 클릭 시 드롭다운 토글
  sprintChangeBtn.addEventListener("click", toggleSprintDropdown);
});
