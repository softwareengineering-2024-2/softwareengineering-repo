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
