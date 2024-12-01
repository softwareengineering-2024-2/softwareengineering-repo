document.addEventListener("DOMContentLoaded", function () {
  const projectId = document.getElementById("project-id").value; // 프로젝트 ID 가져오기

  // 초기화
  initCalendar();
  fetchSchedules(projectId);
  setupEventListeners();
});

const schedules = []; // 일정 데이터를 저장할 배열

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

let currentMonth = new Date().getMonth();
let currentYear = new Date().getFullYear();

function initCalendar() {
  renderCalendar();
}

function setupEventListeners() {
  document.getElementById("prevBtn").addEventListener("click", function () {
    changeMonth(-1);
  });

  document.getElementById("nextBtn").addEventListener("click", function () {
    changeMonth(1);
  });

  document.getElementById("team").addEventListener("change", function () {
    const projectId = document.getElementById("project-id").value;
    fetchSchedules(projectId);
  });

  document.getElementById("personal").addEventListener("change", function () {
    const projectId = document.getElementById("project-id").value;
    fetchSchedules(projectId);
  });
}

// 일정 필터링 함수
function filterSchedules() {
  // 프로젝트 ID 가져오기
  const projectId = document.getElementById("project-id").value;

  // 일정을 새로 가져오고 렌더링하는 함수 호출
  fetchSchedules(projectId);
}

// 일정 가져오기 (필터링을 고려하여 가져옴)
function fetchSchedules(projectId) {
  const showTeamSchedules = document.getElementById("team").checked; // 팀 일정 체크 상태
  const showPersonalSchedules = document.getElementById("personal").checked; // 개인 일정 체크 상태

  fetch(`schedules/${projectId}`)
    .then((response) => response.json())
    .then((data) => {
      schedules.length = 0; // 기존 데이터 초기화

      data.forEach((schedule) => {
        const {
          title,
          start_date,
          due_date,
          color,
          place,
          content,
          important,
          calendar_id,
          team,
        } = schedule;

        // 날짜만 사용하고 시간은 무시하도록 설정
        const start = new Date(start_date);
        const end = new Date(due_date);

        // 시간 부분을 00:00:00으로 설정하여 날짜만 비교
        start.setHours(0, 0, 0, 0); // 시작일의 시간을 00:00:00으로 설정
        end.setHours(23, 59, 59, 999); // 종료일의 시간을 23:59:59.999으로 설정

        // 팀 일정과 개인 일정 필터링
        if (
          (showTeamSchedules && team) ||
          (showPersonalSchedules && !team) ||
          (showTeamSchedules && showPersonalSchedules)
        ) {
          if (!isNaN(start) && !isNaN(end)) {
            schedules.push({
              calendar_id, // schedule_id 추가
              title,
              start,
              end,
              color: colorMap[color] || "#eeeeee", // 색상 설정
              color_num: color,
              place, // 장소 추가
              content, // 내용 추가
              important, // 중요 여부 추가
              team, // team 속성 추가
            });
          }
        }
      });

      renderCalendar(); // 일정 렌더링
    })
    .catch((error) => console.error("Error fetching schedules:", error));
}

function renderCalendar() {
  const calendarDates = document.getElementById("calendarDates");
  const currentMonthElement = document.getElementById("currentMonth");

  const firstDay = new Date(currentYear, currentMonth, 1);
  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
  const startDayOfWeek = firstDay.getDay();

  calendarDates.innerHTML = ""; // 기존 달력 초기화
  currentMonthElement.textContent = `${currentYear}년 ${currentMonth + 1}월`;

  // 이전 달의 날짜 표시
  const prevMonthDays = new Date(currentYear, currentMonth, 0).getDate();
  for (let i = 0; i < startDayOfWeek; i++) {
    const date = new Date(currentYear, currentMonth - 1, prevMonthDays - startDayOfWeek + i + 1);
    const dateElement = createCalendarDate(date.getDate(), true);

    // 일정 렌더링
    renderSchedulesForDate(date, dateElement);

    calendarDates.appendChild(dateElement);
  }

  // 현재 달의 날짜 표시
  for (let i = 1; i <= daysInMonth; i++) {
    const date = new Date(currentYear, currentMonth, i);
    const dateElement = createCalendarDate(i, false);

    // 일정 렌더링
    renderSchedulesForDate(date, dateElement);

    calendarDates.appendChild(dateElement);
  }

  // 다음 달의 날짜 표시
  const remainingDays = 6 - new Date(currentYear, currentMonth, daysInMonth).getDay();
  for (let i = 1; i <= remainingDays; i++) {
    const date = new Date(currentYear, currentMonth + 1, i);
    const dateElement = createCalendarDate(i, true);

    // 일정 렌더링
    renderSchedulesForDate(date, dateElement);

    calendarDates.appendChild(dateElement);
  }
}

function renderSchedulesForDate(date, dateElement) {
  schedules.forEach((schedule) => {
    
    if (date >= schedule.start && date <= schedule.end) {
      const scheduleDiv = document.createElement("div");
      scheduleDiv.textContent = schedule.title;
      scheduleDiv.style.backgroundColor = schedule.color;
      scheduleDiv.classList.add("schedule");

      // 일정 클릭 시 해당 id 전달
      scheduleDiv.addEventListener("click", function () {
        showScheduleDetails(schedule); // 일정 상세보기 모달 표시
      });

      dateElement.appendChild(scheduleDiv);
    }
  });
}

function createCalendarDate(day, isOtherMonth) {
  const dateElement = document.createElement("div");
  dateElement.classList.add("date");
  if (isOtherMonth) {
    dateElement.classList.add("other-month");
  }
  dateElement.textContent = day;
  return dateElement;
}

// 달력 날짜 생성
function createCalendarDate(day, isEmpty) {
  const dateElement = document.createElement("div");
  dateElement.textContent = day;
  dateElement.classList.add("date");
  if (isEmpty) {
    dateElement.classList.add("empty");
    dateElement.style.opacity = "0.5";
  }
  return dateElement;
}

function changeMonth(offset) {
  currentMonth += offset;
  if (currentMonth < 0) {
    currentMonth = 11;
    currentYear -= 1;
  } else if (currentMonth > 11) {
    currentMonth = 0;
    currentYear += 1;
  }
  renderCalendar();
}

// 일정 추가 모달 관리
document.addEventListener("DOMContentLoaded", function () {
  const openModalButton = document.getElementById("openModalButton");
  const modal1 = document.getElementById("newscheduleModal");
  const cancelModalButton = document.getElementById("cancelModalButton");

  // 모달 열기
  openModalButton.addEventListener("click", function () {
    openModal("newscheduleModal"); // modal1을 화면에 표시
  });

  cancelModalButton.addEventListener("click", function () {
    closeModal("newscheduleModal"); // modal1을 닫기
    document.querySelector("#createForm").reset();
  });

  // 모달 외부 클릭 시 닫기
  window.addEventListener("click", function (event) {
    if (event.target === modal1) {
      closeModal("newscheduleModal"); // 외부 클릭 시 modal1 닫기
      document.querySelector("#createForm").reset();
    }
  });
});

// 일정 추가 폼 제출 처리 함수
function submitSchedule(event) {
  event.preventDefault(); // 기본 폼 제출 동작 방지

  const projectId = document.getElementById("project-id").value;

  // 폼 데이터 가져오기
  const title = document.querySelector("#title").value;
  const place = document.querySelector("#place").value;
  const startDate = document.querySelector("#start_date").value;
  const dueDate = document.querySelector("#due_date").value;
  const category = document.querySelector(
    'input[name="category"]:checked'
  ).value;
  const content = document.querySelector("#description").value;
  const important = document.querySelector("#important").checked;

  // important가 체크되었으면 color를 빨간색으로 설정
  const color = important ? 1 : document.querySelector("#color").value;

  // 'team'이면 true, 'personal'이면 false
  const isTeam = category === "team"; // 'team'이 선택되면 true, 아니면 false

  // 필수 입력 항목 검사
  if (!title || !startDate || !dueDate) {
    alert("제목, 시작일, 종료일은 필수로 입력해야 합니다.");
    return; // 폼 제출을 중단
  }

  const formData = {
    title,
    place,
    start_date: startDate,
    due_date: dueDate,
    team: isTeam, // boolean 값으로 변환
    color,
    content,
    important,
  };

  // AJAX 요청 (fetch 사용)
  fetch(`/calendar/${projectId}/`, {
    // URL에 projectId를 포함
    method: "POST",
    headers: {
      "Content-Type": "application/json", // JSON 형식으로 보냄
    },
    body: JSON.stringify(formData), // formData를 JSON으로 변환
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.message === "success") {
        alert("일정이 추가되었습니다!");
        // 폼 초기화 및 모달 닫기
        document.querySelector("#createForm").reset();
        document.querySelector("#newscheduleModal").style.display = "none";
        fetchSchedules(document.getElementById("project-id").value);
      } else {
        alert("일정 추가에 실패했습니다.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("서버 오류가 발생했습니다.");
    });
}

// 저장 버튼 클릭 시 submitSchedule 함수 호출
document.querySelector(".add-button").addEventListener("click", submitSchedule);

// 일정 상세
function showScheduleDetails(schedule) {
  const modal2 = document.getElementById("scheduleDetailModal");

  // 상세 정보 모달에 데이터를 표시
  document.getElementById("scheduleTitle").textContent = schedule.title;
  document.getElementById("schedulePlace").textContent =
    schedule.place || "없음";
  document.getElementById("scheduleStartDate").textContent =
    schedule.start.toLocaleDateString();
  document.getElementById("scheduleEndDate").textContent =
    schedule.end.toLocaleDateString();
  document.getElementById("scheduleDescription").textContent =
    schedule.content || "없음";
  document.getElementById("scheduleImportant").textContent = schedule.important
    ? "예"
    : "아니오";

  // 수정과 삭제 버튼 활성화
  document.getElementById("editScheduleButton").onclick = function () {
    closeModal("scheduleDetailModal"); // 상세보기 모달 닫기
    openEditModal(schedule); // 수정 모달 열기
  };

  document.getElementById("deleteScheduleButton").onclick = function () {
    // color 정보를 확인하여 삭제 가능 여부를 결정
    console.log(schedule.color);
    if (schedule.color === '#eeeeee') {
      alert("마일스톤과 스프린트 일정은 지울 수 없습니다."); // color가 0일 경우 삭제 방지
      return; // 함수 종료
    }
  
    deleteSchedule(schedule.calendar_id); // 일정 삭제
  };

  // 닫기 버튼
  const closeButton = document.getElementById("cancelModalButton2");
  closeButton.addEventListener("click", function () {
    closeModal("scheduleDetailModal");
  });

  // 모달 외부 클릭 시 닫기
  window.addEventListener("click", function (event) {
    if (event.target === modal2) {
      closeModal("scheduleDetailModal"); // 외부 클릭 시 modal1 닫기
    }
  });

  // 모달 열기
  openModal("scheduleDetailModal");
}

// 수정 모달 열기
function openEditModal(schedule) {
  // 기존 데이터 폼에 삽입
  document.getElementById("editTitle").value = schedule.title;
  document.getElementById("editPlace").value = schedule.place || "";
  document.getElementById("editStartDate").value = new Date(
    schedule.start
  ).toLocaleDateString("en-CA");
  document.getElementById("editEndDate").value = new Date(
    schedule.end
  ).toLocaleDateString("en-CA");
  document.getElementById("editDescription").value = schedule.content || "";
  document.getElementById("editImportant").checked = schedule.important;

  // category에 따라 라디오 버튼 선택 설정
  if (schedule.team == true) {
    document.getElementById("editTeam").checked = true;
  } else {
    document.getElementById("editPersonal").checked = true;
  }

  // 색상 선택 필드 설정
  document.getElementById("editColor").value = schedule.color_num;

  // 수정 버튼 클릭 시 일정 수정 처리
  const editedButton = document.getElementById("editbutton");
  editedButton.addEventListener("click", function () {
    submitEditSchedule(event, schedule.calendar_id); // calendar_id를 넘겨서 수정 처리
  });

  // 수정 모달 열기
  openModal("editScheduleModal");

  // 수정 모달 닫기
  const cancelEditModalButton = document.getElementById(
    "cancelEditModalButton"
  );
  cancelEditModalButton.addEventListener("click", function () {
    closeModal("editScheduleModal");
  });
}

// 일정 수정 폼 처리 함수
function submitEditSchedule(event, calendarId) {
  event.preventDefault(); // 기본 폼 제출 동작 방지

  // 수정된 일정 데이터 가져오기
  const title = document.querySelector("#editTitle").value;
  const place = document.querySelector("#editPlace").value;
  const startDate = document.querySelector("#editStartDate").value;
  const dueDate = document.querySelector("#editEndDate").value;
  const category = document.querySelector(
    'input[name="editCategory"]:checked'
  ).value;
  const color = document.querySelector("#editColor").value;
  const content = document.querySelector("#editDescription").value;
  const important = document.querySelector("#editImportant").checked;

  // 'team'이면 true, 'personal'이면 false
  const isTeam = category === "team"; // 'team'이 선택되면 true, 아니면 false

  // 수정된 일정 객체
  const updatedSchedule = {
    title,
    place,
    start_date: startDate,
    due_date: dueDate,
    team: isTeam, // boolean 값으로 변환
    color,
    content,
    important,
  };

  // 일정 수정 요청
  fetch(`/calendar/update/${calendarId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(updatedSchedule), // 수정된 일정 데이터 전송
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.message === "success") {
        alert("일정이 수정되었습니다!");
        closeModal("editScheduleModal");
        fetchSchedules(document.getElementById("project-id").value);
      } else {
        alert("일정 수정에 실패했습니다.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("서버 오류가 발생했습니다.");
    });
}

// 일정 삭제
function deleteSchedule(scheduleId) {
  if (confirm("정말로 이 일정을 삭제하시겠습니까?")) {
    fetch(`${scheduleId}`, {
      method: "DELETE",
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message === "success") {
          alert("일정이 삭제되었습니다.");
          document.querySelector("#scheduleDetailModal").style.display = "none";
          fetchSchedules(document.getElementById("project-id").value); // 일정 새로고침
        } else {
          alert("삭제에 실패했습니다.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("서버 오류가 발생했습니다.");
      });
  }
}

// 모달관리
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  modal.style.display = "flex";
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  modal.style.display = "none";
}
