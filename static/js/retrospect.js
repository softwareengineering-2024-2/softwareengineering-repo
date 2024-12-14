function navigateToRetrospect(event, projectId, retrospectId) {
    // 버튼 클릭인 경우 이동 중지
    if (event.target.closest('.options-btn')) {
        return;
    }

    // 회고 조회 페이지로 이동
    window.location.href = `/retrospect/${projectId}/view/${retrospectId}`;
}

// 모달 열기
function openOptions(event, retrospectId) {
    event.stopPropagation();

    const modal = document.getElementById(`options-modal-${retrospectId}`);
    const targetRect = event.target.getBoundingClientRect();

    // 모달이 이미 열려 있는 경우 닫기
    if (!modal.classList.contains('hidden')) {
        modal.classList.add('hidden'); // hidden 클래스 추가로 닫기
        return;
    }

    // 모달을 버튼의 좌하단에 배치
    modal.style.position = 'absolute';
    modal.style.top = `${targetRect.bottom + window.scrollY}px`; // 버튼의 아래쪽
    modal.style.left = `${targetRect.left}px`; // 버튼의 왼쪽
    modal.classList.remove('hidden'); // hidden 클래스 제거로 표시
}

// 수정 함수
function editRetrospect(retrospectId) {
    // 수정 페이지로 이동
    const editUrl = `/retrospect/${projectId}/edit/${retrospectId}`;
    location.href = editUrl;
}

// 모든 모달 닫기 함수 선언
function closeAllSmallModals() {
    document.querySelectorAll('.modal').forEach((modal) => {
        modal.classList.add('hidden');
    });
}

// 삭제 버튼 클릭 시 삭제 확인 모달 표시
function deleteRetrospect(retrospectId) {
    // Small modal 닫기
    closeAllSmallModals();

    // 모달 메시지 설정
    document.getElementById("confirmDeleteMessage").textContent = "정말로 이 회고를 삭제하시겠습니까?";
    // 확인 버튼에 삭제 동작 연결
    document.querySelector(".custom-modal-confirm-btn").onclick = function () {
        confirmDelete(retrospectId);
    };
    // 삭제 확인 모달 표시
    document.getElementById("confirmDeleteModal").classList.remove("hidden");
}

// 삭제 확인 처리
function confirmDelete(retrospectId) {
    fetch(`/retrospect/${projectId}/delete/${retrospectId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => {
            if (response.ok) {
                showMessageModal("성공", "회고가 삭제되었습니다.");
                setTimeout(() => location.reload(), 2000); // 2초 후 새로고침
            } else {
                showMessageModal("오류", "회고 삭제에 실패했습니다.");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            showMessageModal("오류", "회고 삭제 중 오류가 발생했습니다.");
        });

    // 삭제 확인 모달 닫기
    closeConfirmDeleteModal();
}

// 모달 바깥 클릭 시 닫기
document.addEventListener('click', (event) => {
    const modals = document.querySelectorAll('.modal');
    modals.forEach((modal) => {
        if (!modal.contains(event.target) && !event.target.classList.contains('options-btn')) {
            modal.classList.add('hidden');
        }
    });
});

// 삭제 확인 모달 닫기
function closeConfirmDeleteModal() {
    document.getElementById("confirmDeleteModal").classList.add("hidden");
}

// 메시지 모달 열기
function showMessageModal(title, message) {
    document.getElementById("modalTitle").textContent = title;
    document.getElementById("modalMessage").textContent = message;
    document.getElementById("messageModal").classList.remove("hidden");
}

// 메시지 모달 닫기
function closeMessageModal() {
    document.getElementById("messageModal").classList.add("hidden");
}

// 파일 선택 시 호출
function handleFileSelect(input) {
    if (input.files.length > 0) {
        const fileName = input.files[0].name;
        document.querySelector('.file-upload-input').value = fileName;
    } else {
        document.querySelector('.file-upload-input').value = '';
    }
}

function startOnboarding() {
    const onboardingSteps = [
      {
        element: document.querySelector(".filter"),
        text: "여기에서 카테고리 및 스프린트를 선택하여 회고를 <br>필터링할 수 있습니다.",
        tooltipPosition: "bottom",
      },
      {
        element: document.querySelector(".btn-register"),
        text: "새로운 스프린트 회고를 등록하려면 이 버튼을 <br>클릭하세요.",
        tooltipPosition: "bottom",
      },
      {
        element: document.querySelector(".content-body"),
        text: "등록된 회고들은 이 영역에 카드 형식으로 표시됩니다.",
        tooltipPosition: "top",
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
        // 강조 스타일 추가
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
          default:
            tooltipTop = rect.bottom + 10;
            tooltipLeft = rect.left + rect.width / 2 - tooltipWidth / 2;
        }
  
        // 화면 밖으로 나가는 경우 위치 조정
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
        nextButton.innerText = "다음";
      } else if (currentStep === onboardingSteps.length - 1) {
        nextButton.innerText = "완료";
      }
  
      showStep(currentStep);
    };
  
    nextButton.addEventListener("click", nextStep);
  
    if (!document.cookie.includes("onboarding_done_retrospect=true")) {
      document.cookie = "onboarding_done_retrospect=true; path=/; max-age=31536000"; // 1년 유지
      overlay.classList.remove("hidden");
      showStep(currentStep);
    }
  }
  
  const endOnboarding = () => {
    const overlay = document.getElementById("onboarding-overlay");
    const tooltip = document.getElementById("onboarding-tooltip");
    overlay.classList.add("hidden");
    tooltip.style.display = "none";
  };
  
  document.addEventListener("DOMContentLoaded", () => {
    startOnboarding();
  });
  