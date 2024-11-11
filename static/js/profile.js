/* 화살표 함수 */
const label = document.querySelector(".label");
const options = document.querySelectorAll(".optionItem");
const selectBox = document.querySelector(".selectBox");
const roleSubmit = document.querySelector(".roleSubmit");
const optionList = document.querySelector(".optionList"); // 옵션 목록

// 클릭한 옵션의 텍스트를 라벨 안에 넣음
const handleSelect = (item) => {
  label.parentNode.classList.remove("active");
  label.innerHTML = item.textContent;
  roleSubmit.value = item.textContent;
  selectBox.classList.remove("active"); // 드롭다운 닫기
};

// 옵션 클릭 시 클릭한 옵션을 넘김
options.forEach((option) => {
  option.addEventListener("click", (event) => {
    event.stopPropagation(); // 클릭 이벤트 전파 방지
    handleSelect(option);
  });
});

// selectBox 클릭 시 옵션 목록이 열림/닫힘
selectBox.addEventListener("click", (event) => {
  event.stopPropagation(); // 이벤트 전파 방지
  selectBox.classList.toggle("active");
});

// 문서 전체에 클릭 이벤트 추가 (selectBox 외부 클릭 시 닫기)
document.addEventListener("click", () => {
  selectBox.classList.remove("active");
});
