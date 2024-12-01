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