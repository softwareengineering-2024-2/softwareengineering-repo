// 메시지 조회 및 업데이트 함수
function fetchAlerts(projectId) {
    if (!projectId) {
        console.error('Project ID is not defined.');
        return;
    }
    fetch(`/userstory/get_alerts/${projectId}`) // 서버에 프로젝트 ID를 전달
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const alertList = document.querySelector('.notification-content ul');
            alertList.innerHTML = ''; // 기존 리스트 초기화

            // 최대 5개의 알림만 표시
            const alertsToShow = data.slice(0, 5);
            alertsToShow.forEach(alert => {
                const alertItem = document.createElement('li');
                alertItem.className = 'notification-item';
                alertItem.textContent = `${alert.content}`;
                alertList.appendChild(alertItem);
            });

            // 알림 개수 업데이트
            const alertCount = data.length;
            updateAlertIcon(alertCount);
        })
        .catch(error => {
            // console.error('Error fetching alerts:', error);
        });
}

// 알림 아이콘 옆에 알림 갯수 업데이트 함수
function updateAlertIcon(count) {
    const alertText = document.querySelector('.alert-text');
    if (!alertText) return;

    if (count > 0) {
        alertText.textContent = `알림[${count}]`; // 알림 텍스트와 개수 표시
    } else {
        alertText.textContent = '알림'; // 알림 개수 없을 때 기본 텍스트
    }
}

// 알림 드롭다운 토글 함수
function toggleNotificationDropdown(event, projectId) {
    event.preventDefault();
    const dropdown = document.querySelector('.notification-content');
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';

    if (dropdown.style.display === 'block') {
        fetchAlerts(projectId); // 드롭다운 내용 업데이트
    }
}

// 드롭다운 외부 클릭 시 닫기
document.addEventListener('click', function (event) {
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
