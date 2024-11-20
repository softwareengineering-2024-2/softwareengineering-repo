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

// 삭제 동작
function deleteRetrospect(retrospectId) {
    if (confirm('정말 삭제하시겠습니까?')) {
        fetch(`/retrospect/${projectId}/delete/${retrospectId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then((response) => {
                if (response.ok) {
                    alert('삭제되었습니다.');
                    location.reload(); // 페이지 새로고침
                } else {
                    alert('삭제에 실패했습니다.');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('오류가 발생했습니다.');
            });
    }
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

