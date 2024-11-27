// 캘린더 관련 변수
const calendarDates = document.getElementById("calendarDates");
const currentMonthElement = document.getElementById("currentMonth");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");

// 프로젝트 ID
const projectId = document.body.getAttribute("data-project-id");

const today = new Date();
let currentMonth = today.getMonth();
let currentYear = today.getFullYear();
const schedules = []; // 일정 데이터를 저장할 배열

function fetchSchedules() {
  $.ajax({
    url: "/calendar/" + projectId + "/schedules", // JSON 데이터를 요청할 URL
    type: "GET",
    data: {
      team: $("#team").is(":checked"),
      personal: $("#personal").is(":checked"),
    },
    success: function (response) {
      console.log("서버 응답:", response); // 응답 확인
      schedules.length = 0; // 기존 일정 데이터 초기화

      response.forEach((schedule) => {
        const title = schedule.title;
        const startDate = new Date(schedule.start_date);
        const dueDate = new Date(schedule.due_date);
        const colorKey = schedule.color;
        const color = colorMap[colorKey];

        // 유효한 날짜인지 확인
        if (!isNaN(startDate.getTime()) && !isNaN(dueDate.getTime())) {
          schedules.push({ title, start: startDate, end: dueDate, color });
        }
      });

      renderCalendar(); // 캘린더 렌더링
    },
    error: function (xhr, status, error) {
      console.error("AJAX 요청 실패:", status, error);
    },
  });
}

$(document).ready(function () {
  fetchSchedules();

  // 중요 체크박스에 대한 이벤트 리스너 추가
  $("#important").change(function () {
    if ($(this).is(":checked")) {
      // 중요 체크 시, 범주 색을 빨강으로 고정
      $("#color").val("1"); // 빨강 선택
      $("#color").prop("disabled", true); // 색상 선택을 비활성화
    } else {
      // 중요 체크 해제 시, 범주 색을 다시 선택 가능하게
      $("#color").prop("disabled", false); // 색상 선택 활성화
      // 중요 체크 해제 시 color 값 초기화
      $("#color").val("2"); // 기본값 설정 (선택을 다시 가능하게 하기 위해)
    }
  });
});

// 페이지가 로드될 때 일정 가져오기
$(document).ready(function () {
  fetchSchedules();
});

const colorMap = {
  1: "#f0ada6",
  2: "#f6c6ad",
  3: "#fffbce",
  4: "#b5e4a2",
  5: "#dee9f8",
  6: "#babdff",
  7: "#e9c8ff",
};

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

    // 일요일인지 확인
    const currentDate = new Date(currentYear, currentMonth, i);
    if (currentDate.getDay() === 0) {
      // 일요일
      dateElement.style.color = "red"; // 빨간색으로 설정
    }

    // 공휴일 체크
    if (isHoliday(currentDate)) {
      dateElement.style.color = "red"; // 빨간색으로 설정
    }

    schedules.forEach((schedule) => {
      const scheduleStart = schedule.start.getDate();
      const scheduleEnd = schedule.end.getDate();
      const scheduleMonth = schedule.start.getMonth();
      const scheduleYear = schedule.start.getFullYear();

      if (scheduleMonth === currentMonth && scheduleYear === currentYear) {
        if (i >= scheduleStart && i <= scheduleEnd) {
          const scheduleDiv = document.createElement("div");
          scheduleDiv.classList.add("schedule");
          scheduleDiv.textContent = schedule.title;
          scheduleDiv.style.backgroundColor = schedule.color || "gray"; // 색상 설정, 기본값 gray
          dateElement.appendChild(scheduleDiv);
        }
      }
    });

    // 클릭 이벤트 추가
    dateElement.addEventListener("click", () => {
      showScheduleDetails(currentYear, currentMonth, i);
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
    calendarDates.appendChild(emptyDate);
  }
}

// 공휴일 체크 함수 (예시)
function isHoliday(date) {
  const holidays = [
    new Date(currentYear, 0, 1), // 새해
    new Date(currentYear, 4, 5), // 부처님 오신 날
    new Date(currentYear, 7, 15), // 광복절
    new Date(currentYear, 9, 3), // 한글날
    new Date(currentYear, 11, 25), // 크리스마스
    // 추가 공휴일을 여기에 추가
  ];

  return holidays.some((holiday) => holiday.getTime() === date.getTime());
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

function showScheduleDetails(year, month, day) {
  const scheduleDetails = document.getElementById("scheduleDetails");
  scheduleDetails.innerHTML = ""; // 기존 내용 초기화

  const selectedDate = new Date(year, month, day);
  selectedDate.setHours(0, 0, 0, 0); // 시간 정보를 제거하여 비교

  // 선택한 날짜를 포함하여 필터링
  const dailySchedules = schedules.filter((schedule) => {
    const scheduleStart = new Date(schedule.start);
    const scheduleEnd = new Date(schedule.end);
    scheduleStart.setHours(0, 0, 0, 0); // 시간 정보를 제거
    scheduleEnd.setHours(0, 0, 0, 0); // 시간 정보를 제거

    return (
      selectedDate >= scheduleStart && // 선택한 날짜가 시작일 이후이거나 같고
      selectedDate <= scheduleEnd // 선택한 날짜가 종료일 이전이거나 같음
    );
  });

  if (dailySchedules.length === 0) {
    scheduleDetails.innerHTML = "<p>이 날짜에 일정이 없습니다.</p>";
  } else {
    dailySchedules.forEach((schedule) => {
      const scheduleItem = document.createElement("div");
      scheduleItem.textContent = `${
        schedule.title
      } (${schedule.start.toLocaleDateString()} - ${schedule.end.toLocaleDateString()})`;
      scheduleDetails.appendChild(scheduleItem);
    });
  }

  // 모달 표시
  const modal = document.getElementById("scheduleModal");
  modal.style.display = "block";

  // 모달 닫기 버튼 이벤트
  const closeButton = document.querySelector(".close-button");
  closeButton.onclick = function () {
    modal.style.display = "none";
  };

  // 모달 외부 클릭 시 닫기
  window.onclick = function (event) {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  };
}

// 초기 일정 데이터 가져오기
fetchSchedules();
