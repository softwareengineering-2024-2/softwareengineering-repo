document.addEventListener('DOMContentLoaded', () => {
    const sidebarLinks = document.querySelectorAll('.sidebar a[href^="#"]');
    const sections = document.querySelectorAll('.guide-section');
    const nextButtons = document.querySelectorAll('.next-button'); // "다음 주제로" 버튼 선택

    // 초기 상태: 첫 번째 섹션 활성화
    if (sections.length > 0) {
        sections[0].classList.add('active'); // 첫 번째 섹션에 active 클래스 추가
    }
    if (sidebarLinks.length > 0) {
        sidebarLinks[0].classList.add('active'); // 첫 번째 링크에 active 클래스 추가
    }
    
    // 사이드바 링크 클릭 이벤트 처리
    sidebarLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();

            const targetId = link.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);

            if (!targetSection) return;

            // 모든 섹션 숨기기
            sections.forEach(section => section.classList.remove('active'));

            // 클릭된 섹션 표시
            targetSection.classList.add('active');

            // 사이드바 링크 강조
            sidebarLinks.forEach(link => link.classList.remove('active'));
            link.classList.add('active');
        });
    });

    // "다음 주제로" 버튼 클릭 이벤트 처리
    nextButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();

            const currentSection = button.closest('.guide-section'); // 현재 섹션
            const currentIndex = Array.from(sections).indexOf(currentSection); // 현재 섹션의 인덱스
            const nextIndex = currentIndex + 1; // 다음 섹션의 인덱스

            if (nextIndex < sections.length) {
                const nextSection = sections[nextIndex];

                // 모든 섹션 숨기기
                sections.forEach(section => section.classList.remove('active'));

                // 다음 섹션 표시
                nextSection.classList.add('active');

                // 사이드바 링크 강조
                sidebarLinks.forEach(link => link.classList.remove('active'));
                const nextLink = document.querySelector(`.sidebar a[href="#${nextSection.id}"]`);
                if (nextLink) nextLink.classList.add('active');

                // 다음 섹션으로 스크롤
                nextSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});
