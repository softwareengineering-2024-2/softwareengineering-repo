function toggleNotificationDropdown(event) {
    event.preventDefault();
    const dropdown = document.querySelector('.notification-content');
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}
