// 메시지 조회 함수
function fetchAlerts(projectId) {
    fetch(`/userstory/get_alerts/${projectId}`)  // projectId를 URL에 포함시켜서 요청
    .then(response => response.json())
    .then(data => {
        const alertList = document.querySelector('.notification-content ul');
        alertList.innerHTML = '';  // 기존 리스트 초기화
        data.forEach(alert => {
            const alertItem = document.createElement('li');
            alertItem.className = 'notification-item';
            alertItem.textContent = `${alert.content}`;
            alertList.appendChild(alertItem);
        });
    })
    .catch(error => {
        console.error('Error fetching alerts:', error);
    });
}

// 알림 드롭다운 토글 함수
function toggleNotificationDropdown(event, projectId) {
    event.preventDefault();
    const dropdown = document.querySelector('.notification-content');
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
    
    if (dropdown.style.display === 'block') {
        fetchAlerts(projectId);  // 알림 조회
    }
}

document.addEventListener('click', function(event) {
    const dropdown = document.querySelector('.notification-content');
    const isClickInside = dropdown.contains(event.target) || event.target.closest('.notification-dropdown');

    if (!isClickInside && dropdown.style.display === 'block') {
        dropdown.style.display = 'none';
    }
});

// 마이페이지 관련 js
function toggleMyPageDropdown(event) {
    event.preventDefault();
    const myPageContent = document.querySelector('.mypage-content');
    myPageContent.style.display = myPageContent.style.display === 'block' ? 'none' : 'block';
}

document.addEventListener('click', function(event) {
    const myPageContent = document.querySelector('.mypage-content');
    const isClickInside = myPageContent.contains(event.target) || event.target.closest('.my-page-dropdown');

    if (!isClickInside && myPageContent.style.display === 'block') {
        myPageContent.style.display = 'none';
    }
});
