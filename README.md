# softwareengineering-repo
2024년 2학기 소프트웨어공학론 수업 레포입니다.

## Commit Convention
| Commit Type | Description                                |
|-------------|--------------------------------------------|
| feat        | 새로운 기능 추가                                  |
| fix         | 버그 수정                                      |
| docs        | 문서 수정                                      |
| style       | 코드 스타일 변경(코드 형식, 세미콜록 누락 등 기능을 수정하지 않은 경우) |
| refactor    | 코드 리팩토링                                    |
| test        | 테스트 코드 추가 및 수정                             |
| chore       | 패키지 매니저 수정                                 |
| rename      | 파일 또는 폴더를 삭제만 한 경우                         
| remove      | 파일명 또는 폴더명을 수정만 한 경우                       |
| build       | 빌드 관련 파일 수정                                


## 개발 전 할 것!
1. issue 등록하기
  - 이슈 타이틀은 커밋 컨벤션을 지킨다
2. issue 등록 후 해당 이슈 branch 파기
  - 오른쪽 항목들 중 `development` - `create a branch` 클릭 - `reposiotory destination`을 포크한 개인레포로 설정
  - 브랜치 이름: `#이슈번호-commit Type/내용`

## 개발 후 할 것!
1. PR 보내기
   - development 브랜치에 PR 요청
   - PR 타이틀은 `commit type issue #이슈번호: 내용` (헷갈리면 이전 PR들 확인)
   - 연관된 이슈에 개발 전 등록한 이슈 번호를 작성 
2. 이슈 닫기
   - 개발이 끝났다면 `close issue`를 눌러 이슈 닫기
