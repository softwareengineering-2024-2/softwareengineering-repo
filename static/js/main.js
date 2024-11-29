// todo
document.addEventListener("DOMContentLoaded", function () {
  const projectId = document.getElementById("project-id").value; // 프로젝트 ID를 가져옵니다.
  fetchTodos(projectId); // 페이지 로드 시 투두리스트를 조회합니다.
});

function addNewTodoInput() {
  const addTodo = document.getElementById("add-todo");
  addTodo.style.display = "none";

  const todoList = document.getElementById("todo-list");
  const newTodoItem = document.createElement("li");
  newTodoItem.className = "todo-item";

  const inputField = document.createElement("input");
  inputField.type = "text";
  inputField.className = "todo-input";
  inputField.placeholder = "할 일을 입력하세요";
  inputField.addEventListener("keypress", function (event) {
    if (event.key === "Enter" && inputField.value.trim() !== "") {
      addTodoItem(inputField.value);
      saveTodoToServer(inputField.value);
      newTodoItem.remove();
      addTodo.style.display = "block";
    }
  });

  newTodoItem.appendChild(inputField);
  todoList.appendChild(newTodoItem);
  inputField.focus();
}

function addTodoItem(text, todoId, todoStatus) {
  const todoList = document.getElementById("todo-list");

  const todoItem = document.createElement("li");
  todoItem.className = "todo-item";
  todoItem.setAttribute("data-todos-todo_id", todoId); // todoId 저장
  todoItem.setAttribute("data-todos-status", todoStatus); // status 저장

  const todoText = document.createElement("span");
  todoText.className = "todo-text";
  todoText.innerText = text;

  const editButton = document.createElement("button");
  editButton.className = "todo-edit";
  editButton.innerText = "수정";

  editButton.onclick = function () {
    if (editButton.innerText === "수정") {
      const editInput = document.createElement("input");
      editInput.type = "text";
      editInput.className = "todo-input";
      editInput.value = todoText.innerText;

      editInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter" && editInput.value.trim() !== "") {
          todoText.innerText = editInput.value;
          todoItem.replaceChild(todoText, editInput);
          editButton.innerText = "수정";
          updateTodoToServer(todoId, editInput.value); // 수정된 내용을 서버로 전송
        }
      });

      todoItem.replaceChild(editInput, todoText);
      editInput.focus();
      editButton.innerText = "저장";
    } else {
      const editInput = todoItem.querySelector(".todo-input");
      if (editInput && editInput.value.trim() !== "") {
        todoText.innerText = editInput.value;
        todoItem.replaceChild(todoText, editInput);
        editButton.innerText = "수정";
        updateTodoToServer(todoId, editInput.value); // 수정된 내용을 서버로 전송
      }
    }
  };

  const completeButton = document.createElement("button");
  completeButton.className = "todo-complete";

  // 현재 상태 읽기
  const initStatus = todoItem.getAttribute("data-todos-status");

  // 초기 상태 UI 설정
  if (initStatus === "true") {
    todoText.style.textDecoration = "line-through";
    todoText.style.color = "grey";
    completeButton.innerText = "미완료";
    editButton.style.display = "none"; // 수정 버튼 숨기기
  } else {
    todoText.style.textDecoration = "none";
    todoText.style.color = "black";
    completeButton.innerText = "완료";
  }

  completeButton.onclick = function () {
    // 현재 상태를 동적으로 읽기
    const currentStatus = todoItem.getAttribute("data-todos-status");

    // 상태 반전
    const newStatus = currentStatus === "true" ? "false" : "true";
    todoItem.setAttribute("data-todos-status", newStatus);

    // 서버에 상태 변경 요청
    changeStatus(todoId, newStatus);
  };

  const deleteButton = document.createElement("button");
  deleteButton.className = "todo-delete";
  deleteButton.innerText = "삭제";

  deleteButton.onclick = function () {
    deleteTodoFromServer(todoId);
  };

  todoItem.appendChild(todoText);
  todoItem.appendChild(editButton);
  todoItem.appendChild(completeButton);
  todoItem.appendChild(deleteButton);
  todoList.appendChild(todoItem);
}

function fetchTodos(projectId) {
  fetch(`/project_main/get_todo/${projectId}`)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      const todoList = document.getElementById("todo-list"); // 수정: ID 맞춤
      todoList.innerHTML = ""; // 기존 리스트 초기화

      if (data && Array.isArray(data)) {
        data.forEach((todos) => {
          addTodoItem(todos.todo, todos.todo_id, todos.status); // 여기서도 todos.todo 사용
        });
      } else {
        console.error("Invalid data format received:", data);
      }
    })
    .catch((error) => {
      console.error("Error fetching todos:", error); // 에러 확인
    });
}

// 투두리스트를 서버에 저장하는 함수
function saveTodoToServer(todoContent) {
  const projectId = document.getElementById("project-id").value; // 프로젝트 ID를 가져옵니다.
  fetch(`/project_main/todo/${projectId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ todo_content: todoContent }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.message === "success") {
        const projectId = document.getElementById("project-id").value;
        fetchTodos(projectId); // 투두리스트 갱신
      } else {
        console.error("Failed to save todo");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// 투두리스트 업데이트 함수
function updateTodoToServer(todoId, newContent) {
  fetch(`/project_main/update_todo/${todoId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ todo_content: newContent }),
  })
    .then((response) => response.json())
    .then((data) => {
      const projectId = document.getElementById("project-id").value;
      fetchTodos(projectId); // 투두리스트 갱신
    })
    .catch((error) => {
      console.error("Error updating todo:", error);
    });
}

function deleteTodoFromServer(todoId) {
  fetch(`/project_main/delete_todo/${todoId}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.message === "success") {
        const projectId = document.getElementById("project-id").value;
        fetchTodos(projectId); // 투두리스트 갱신
      } else {
        console.error("Failed to delete todo");
      }
    })
    .catch((error) => {
      console.error("Error deleting todo:", error);
    });
}

// 상태변경 변경
function changeStatus(todoId, status) {
  fetch(`/project_main/change_status/${todoId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ status: status }),
  })
    .then((response) => response.json())
    .then((data) => {
      const projectId = document.getElementById("project-id").value;
      fetchTodos(projectId); // 투두리스트 갱신
    })
    .catch((error) => {
      console.error("Error changing status:", error);
    });
}

/////////////////////////////////////////////////////////////////////////
// 2주 캘린더
document.addEventListener("DOMContentLoaded", function () {
  const projectId = document.getElementById("project-id").value; // 프로젝트 ID 가져오기

  // 초기화
  initCalendar2();
  fetchSchedules(projectId);
  setupEventListeners2();
});

let currentMonth = new Date().getMonth();
let currentYear = new Date().getFullYear();
let currentWeek = new Date().getWeek();
let today = new Date().getDate();

const schedules = []; 

function initCalendar2() {
  renderCalendar2();
}

function setupEventListeners2() {
  document.getElementById("prevBtn").addEventListener("click", function () {
    changeWeek(-1);
  });

  document.getElementById("nextBtn").addEventListener("click", function () {
    changeWeek(1);
  });
}

function changeWeek(diff) {
  currentWeek += diff;
  if (currentWeek < 0){
    currentWeek = 51;
    currentYear -= 1;
  }
  else if (currentWeek > 51){
    currentWeek = 0;
    currentYear += 1;
  }
  renderCalendar2();
}

function renderCalendar2() {
  const calendarDates = document.getElementById("calendarDates");
    const today = new Date();

    // 초기화
    calendarDates.innerHTML = "";

    // 오늘 날짜 기준으로 속한 주의 일요일 계산
    const currentDay = today.getDay();
    const diffToSunday = currentDay === 0 ? 0 : currentDay; // 오늘이 일요일이면 차이는 0, 아니면 일요일까지의 차이 계산
    const sunday = new Date(today);
    sunday.setDate(today.getDate() - diffToSunday); // 일요일 날짜로 이동 (현재 일요일로부터 이전 날짜를 빼서 일요일로 이동)

    // 2주 간의 날짜 생성
    let calendarDays = [];
    let currentDate = new Date(sunday);

    // 2주 동안 날짜 배열
    for (let i = 0; i < 14; i++) {
      calendarDays.push(new Date(currentDate)); // 날짜 배열에 추가
      currentDate.setDate(currentDate.getDate() + 1); // 다음 날로 이동
    }

    // 날짜를 그리드로 표시
    calendarDays.forEach((date, index) => {
      const dateDiv = document.createElement("div");
      dateDiv.classList.add("date");

      dateDiv.textContent = date.getDate();

      schedules.forEach((schedule) => {
        if (date >= schedule.start && date <= schedule.end) {
          const scheduleDiv = document.createElement("div");
          scheduleDiv.textContent = schedule.title;
          scheduleDiv.style.backgroundColor = schedule.color;
          scheduleDiv.classList.add("schedule");

          dateElement.appendChild(scheduleDiv);
        }
      });

      // 오늘 날짜 강조 표시
      if (date.toDateString() === today.toDateString()) {
        dateDiv.style.fontWeight = "bold";
        dateDiv.style.color = "red";
      }

      calendarDates.appendChild(dateDiv);
    });
}


// 팔레트
const colorMap = {
  1: "#f0ada6",
  2: "#f6c6ad",
  3: "#fffbce",
  4: "#b5e4a2",
  5: "#dee9f8",
  6: "#babdff",
  7: "#e9c8ff",
};

// 일정 조회
function fetchSchedules(projectId){
  fetch(`/project_main/calendar/${projectId}`)
    .then((response) => response.json())
    .then((data) => {
      schedules.length = 0; // 초기화

      data.forEach((schedule) => {
        const{
          title,
          start_date,
          due_date,
          color,
          calendar_id,
        } = schedule;

        // 날짜만 사용하고 시간은 무시하도록 설정
        const start = new Date(start_date);
        const end = new Date(due_date);

        // 시간 부분을 00:00:00으로 설정하여 날짜만 비교
        start.setHours(0, 0, 0, 0); // 시작일의 시간을 00:00:00으로 설정
        end.setHours(23, 59, 59, 999); // 종료일의 시간을 23:59:59.999으로 설정

        if (!isNaN(start) && !isNaN(end)) {
          schedules.push({
            calendar_id,
            title,
            start_date,
            due_date,
            color: colorMap[color] || "#eeeeee",
          });
        }
      });

      renderCalendar();
    })
    .catch((error) => console.error("Error fetching schedules:", error));
}
