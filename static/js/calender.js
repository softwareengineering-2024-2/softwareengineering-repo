// 캘린더 관련 변수
const calendarDates = document.getElementById("calendarDates");
const currentMonthElement = document.getElementById("currentMonth");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");

// 모달 관련 변수
const modal = document.getElementById("scheduleModal");
const openModalBtn = document.getElementById("openModalBtn");
const closeModalBtns = document.querySelectorAll(".close");

// 프로젝트 ID
const projectId = document.body.getAttribute("data-project-id");

const today = new Date();
let currentMonth = today.getMonth();
let currentYear = today.getFullYear();
const schedules = []; // 일정 데이터를 저장할 배열

// 일정 데이터 가져오기
function fetchSchedules() {
  $.ajax({
    url: "/calendar/" + projectId,
    type: "GET",
    data: {
      team: $("#team").is(":checked"),
      personal: $("#personal").is(":checked"),
    },
    success: function (response) {
      console.log("서버 응답:", response);
      schedules.length = 0; // 기존 일정 데이터 초기화
      $(response)
        .find(".schedule-item")
        .each((index, item) => {
          const title = $(item).data("title");
          const startDate = new Date($(item).data("start-date"));
          const dueDate = new Date($(item).data("due-date"));
          schedules.push({ title, start: startDate, end: dueDate });
        });
      renderCalendar(); // 일정 데이터를 받아온 후 캘린더 렌더링
    },
    error: function (xhr, status, error) {
      console.error("AJAX 요청 실패:", status, error);
    },
  });
}

function renderCalendar() {
  const firstDayOfMonth = new Date(currentYear, currentMonth, 1);
  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
  const startDayOfWeek = firstDayOfMonth.getDay();

  currentMonthElement.textContent = `${currentYear}년 ${currentMonth + 1}월`;
  calendarDates.innerHTML = "";

  // 이전 달 날짜 추가
  const prevMonthDays = new Date(currentYear, currentMonth, 0).getDate();
  for (let i = 0; i < startDayOfWeek; i++) {
    const emptyDate = document.createElement("div");
    emptyDate.classList.add("date", "empty");
    emptyDate.style.opacity = "0.5";
    emptyDate.textContent = prevMonthDays - startDayOfWeek + 1 + i;
    calendarDates.appendChild(emptyDate);
  }

  // 현재 달 날짜 추가
  for (let i = 1; i <= daysInMonth; i++) {
    const dateElement = document.createElement("div");
    dateElement.classList.add("date");
    dateElement.textContent = i;

    // 각 날짜에 일정 추가하기
    schedules.forEach((schedule) => {
      const scheduleStart = schedule.start.getDate();
      const scheduleEnd = schedule.end.getDate();
      const scheduleMonth = schedule.start.getMonth();
      const scheduleYear = schedule.start.getFullYear();

      // 현재 월의 날짜와 일치하는지 확인
      if (scheduleMonth === currentMonth && scheduleYear === currentYear) {
        if (i >= scheduleStart && i <= scheduleEnd) {
          dateElement.innerHTML += `<div class="schedule">${schedule.title}</div>`;
        }
      }
    });

    calendarDates.appendChild(dateElement);
  }

  // 다음 달 날짜 추가
  const remainingDays =
    6 - new Date(currentYear, currentMonth, daysInMonth).getDay();
  for (let i = 1; i <= remainingDays; i++) {
    const emptyDate = document.createElement("div");
    emptyDate.classList.add("date", "empty");
    emptyDate.style.opacity = "0.5";
    emptyDate.textContent = i;

    // 다음 달의 일정 추가하기
    schedules.forEach((schedule) => {
      const scheduleStart = schedule.start.getDate();
      const scheduleEnd = schedule.end.getDate();
      const scheduleMonth = schedule.start.getMonth();
      const scheduleYear = schedule.start.getFullYear();

      // 다음 월의 날짜와 일치하는지 확인
      if (scheduleMonth === currentMonth + 1 && scheduleYear === currentYear) {
        if (i <= scheduleEnd) {
          emptyDate.innerHTML += `<div class="schedule">${schedule.title}</div>`;
        }
      }
    });

    calendarDates.appendChild(emptyDate);
  }
}

// 초기 일정 데이터 가져오기
fetchSchedules();

// 이전 버튼 클릭 이벤트
prevBtn.addEventListener("click", () => {
  currentMonth--;
  if (currentMonth < 0) {
    currentMonth = 11;
    currentYear--;
  }
  renderCalendar();
});

// 다음 버튼 클릭 이벤트
nextBtn.addEventListener("click", () => {
  currentMonth++;
  if (currentMonth > 11) {
    currentMonth = 0;
    currentYear++;
  }
  renderCalendar();
});

// 체크박스 변경 시 일정 필터링
$("#team").change(fetchSchedules);
$("#personal").change(fetchSchedules);

// 모달 열기 버튼 클릭 시 모달 열기
openModalBtn.onclick = function () {
  modal.style.display = "flex";
};

// 모달 닫기 버튼 클릭 시 모달 닫기
closeModalBtns.forEach((btn) => {
  btn.onclick = function () {
    modal.style.display = "none";
  };
});

// 모달 바깥 클릭 시 모달 닫기
window.onclick = function (event) {
  if (event.target === modal) {
    modal.style.display = "none";
  }
};
