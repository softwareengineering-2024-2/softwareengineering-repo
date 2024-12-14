document.addEventListener("DOMContentLoaded", function() {
    const joinProjectButton = document.getElementById("joinProjectButton");
    const linkCheckValue = document.getElementById("linkCheckValue").value;
  
    // 링크 검증 상태에 따라 버튼 활성화/비활성화
    if (linkCheckValue === "-1" || linkCheckValue === "0") {
        joinProjectButton.style.opacity = "0.5"; // 반투명
        joinProjectButton.style.backgroundColor = "#ccc"; // 회색 톤 배경
    } else {
        joinProjectButton.style.opacity = ""; // 기본값으로 재설정
        joinProjectButton.style.backgroundColor = ""; // 기본값으로 재설정
    }

    // 참여하기 버튼에 이벤트 리스너 추가
    joinProjectButton.addEventListener("click", function(event) {
        // 링크 검증이 되지 않았을 때
        if (linkCheckValue === "-1" || linkCheckValue === "0") {
          event.preventDefault(); // 기본 폼 제출 막기
          alert("프로젝트 참여코드를 먼저 확인해주세요.");
        }
});
});
  
  