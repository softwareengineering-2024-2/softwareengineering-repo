document.addEventListener('DOMContentLoaded', () => {
    // 사이드바 링크 클릭 시 섹션 표시/숨김 처리
    document.querySelectorAll('.sidebar a').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetSection = e.target.dataset.section;

            // 모든 섹션 숨기기
            document.querySelectorAll('.guide-section').forEach(section => {
                section.classList.remove('active');
            });

            // 클릭된 섹션만 표시
            document.getElementById(targetSection).classList.add('active');
        });
    });
});
