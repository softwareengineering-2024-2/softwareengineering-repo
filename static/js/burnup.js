document.addEventListener("DOMContentLoaded", function () {
  const ctx = document.getElementById("burnupChart").getContext("2d");
  if (!ctx) {
    console.error("Canvas element not found");
    return;
  }

  // 데이터 검증
  if (!chartData.labels || !chartData.totalTasks || !chartData.completedTasks) {
    console.error("Chart data is incomplete or incorrectly formatted");
    return;
  }

  // 차트 인스턴스 생성
  const burnupChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: chartData.labels,
      datasets: [
        {
          label: "Total Tasks",
          data: chartData.totalTasks,
          borderColor: "rgb(75, 192, 192)",
          backgroundColor: "rgba(75, 192, 192, 0.5)",
          fill: true,
        },
        {
          label: "Completed Tasks",
          data: chartData.completedTasks,
          borderColor: "rgb(255, 99, 132)",
          backgroundColor: "rgba(255, 99, 132, 0.5)",
          fill: true,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "작업 수",
          },
        },
        x: {
          title: {
            display: true,
            text: "프로젝트 기간",
          },
        },
      },
      plugins: {
        legend: {
          position: "top",
        },
        tooltip: {
          mode: "index",
          intersect: false,
        },
      },
    },
  });
  window.addEventListener("resize", function () {
    burnupChart.resize();
  });
});
function startOnboarding() {
  const onboardingSteps = [
    {
      element: document.querySelector(".burnup-chart-container"),
      text: "이곳은 번업 차트입니다. 프로젝트의 진행 상황을 <br>시각적으로 확인할 수 있습니다.",
      tooltipPosition: "left",
    },
    {
      element: document.querySelector("#burnupChartContainer"),
      text: "이 차트는 완료된 작업과 전체 작업의 관계를 <br>날짜별로 보여줍니다.",
      tooltipPosition: "bottom",
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
  if (!document.cookie.includes("onboarding_done_burnup=true")) {
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
  document.cookie = "onboarding_done_burnup=true; path=/; max-age=31536000"; // 1년 유지
};

document.addEventListener("DOMContentLoaded", function () {
  startOnboarding();
});
