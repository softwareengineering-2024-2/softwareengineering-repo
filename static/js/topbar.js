// 알림 관련 js
function toggleNotificationDropdown(event) {
    event.preventDefault();
    const dropdown = document.querySelector('.notification-content');
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
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
