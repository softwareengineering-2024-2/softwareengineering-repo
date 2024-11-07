// 스프린트 생성 모달 열기 함수
function openSprintCreateModal() {
    document.getElementById('sprint_create_modal').style.display = 'flex';
}

// 스프린트 생성 모달 닫기 함수
function closeSprintCreateModal() {
    document.getElementById('sprint_create_modal').style.display = 'none';
}

// 스프린트 추가 함수 (추후 구현 가능)
function addSprint() {
    // 스프린트 추가 로직 구현
    closeSprintCreateModal();
}


// 스프린트 백로그 생성 모달 열기 함수
function openSprintBacklogModal() {
    document.getElementById('sprint_backlog_modal').style.display = 'flex';
}

// 스프린트 백로그 생성 모달 닫기 함수
function closeSprintBacklogModal() {
    document.getElementById('sprint_backlog_modal').style.display = 'none';
}

// 스프린트 백로그 추가 함수 (추후 구현 가능)
function addSprintBacklog() {
    // 스프린트 백로그 추가 로직 구현
    closeSprintBacklogModal();
}

/////////////////////////////////////////////////////////////////////////////////////
// 스프린트 설정 팝업 모달 열기/닫기
function toggleSprintOptionsModal(event) {
    const modal = document.getElementById('sprint-options-modal');
    modal.style.display = modal.style.display === 'none' ? 'block' : 'none';
    // 팝업 모달의 위치를 버튼 왼쪽에 맞게 설정
    modal.style.top = event.clientY + 'px';
    modal.style.left = (event.clientX - modal.offsetWidth) + 'px';
}

// 백로그 설정 팝업 모달 열기/닫기
function toggleBacklogOptionsModal(event) {
    const modal = document.getElementById('backlog-options-modal');
    modal.style.display = modal.style.display === 'none' ? 'block' : 'none';
    // 팝업 모달의 위치를 버튼 왼쪽에 맞게 설정
    modal.style.top = event.clientY + 'px';
    modal.style.left = (event.clientX - modal.offsetWidth) + 'px';
}

// Small modal 닫기 함수 (small 모달에서 수정시 small 모달이 안닫혀서 생성)
function closeSmallModal() {
    document.querySelectorAll('.small-modal').forEach(modal => {
        modal.style.display = 'none';
    });
}

// 스프린트 수정 모달 열기 함수
function openSprintEditModal() {
    closeSmallModal(); // small modal 닫기
    document.getElementById('sprint_edit_modal').style.display = 'flex';
}

// 스프린트 수정 모달 닫기 함수
function closeSprintEditModal() {
    document.getElementById('sprint_edit_modal').style.display = 'none';
}

// 스프린트 수정 저장 함수
function saveSprintChanges() {
    // 저장 로직 구현 (예: 데이터베이스에 업데이트)
    closeSprintEditModal();
}

function deleteSprint() {
    closeSprintOptionsModal();
}

// 스프린트 백로그 수정 모달 열기 함수
function openSprintBacklogEditModal() {
    closeSmallModal(); // small modal 닫기
    document.getElementById('sprint_backlog_edit_modal').style.display = 'flex';
}

// 스프린트 백로그 수정 모달 닫기 함수
function closeSprintBacklogEditModal() {
    document.getElementById('sprint_backlog_edit_modal').style.display = 'none';
}

// 스프린트 백로그 수정 저장 함수
function saveBacklogChanges() {
    // 수정된 데이터를 저장하는 로직 구현 (예: 데이터베이스 업데이트)
    closeSprintBacklogEditModal();
}


function deleteBacklog() {
    closeBacklogOptionsModal();
}

// 팝업 모달 닫기
function closeSprintOptionsModal() {
    document.getElementById('sprint-options-modal').style.display = 'none';
}

function closeBacklogOptionsModal() {
    document.getElementById('backlog-options-modal').style.display = 'none';
}

// 화면 클릭 시 팝업 모달 닫기
window.addEventListener('click', function(event) {
    const sprintOptionsModal = document.getElementById('sprint-options-modal');
    const backlogOptionsModal = document.getElementById('backlog-options-modal');
    
    if (!event.target.closest('.header-options-btn') && 
        !event.target.closest('#sprint-options-modal')) {
        closeSprintOptionsModal();
    }
    if (!event.target.closest('.options-btn') && 
        !event.target.closest('#backlog-options-modal')) {
        closeBacklogOptionsModal();
    }
});




