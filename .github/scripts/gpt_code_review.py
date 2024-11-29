import os
import openai
from github import Github

# 환경 변수 설정
openai.api_key = os.environ.get("OPENAI_API_KEY")
github_token = os.environ.get("GITHUB_TOKEN")
repo_name = os.environ.get("GITHUB_REPOSITORY")
pr_number = os.environ.get("PR_NUMBER")

if not all([openai.api_key, github_token, repo_name, pr_number]):
    raise Exception("필요한 환경 변수가 설정되지 않았습니다.")

# GitHub 클라이언트 생성
g = Github(github_token)
repo = g.get_repo(repo_name)
pr = repo.get_pull(int(pr_number))

# 변경된 파일 가져오기
changed_files = pr.get_files()

# GPT에게 보낼 프롬프트 생성 및 리뷰 수행
review_comments = []

for file in changed_files:
    filename = file.filename
    # 원하는 파일 확장자 필터링
    if filename.endswith(('.py', '.js', '.html', '.css')):
        diff = file.patch
        prompt = f"다음은 PR에서 변경된 코드의 diff입니다:\n{diff}\n\n이 변경 사항에 대한 상세한 코드 리뷰를 한국어로 작성해 주세요. 개선점, 잠재적 버그, 코드 스타일 등에 대해 언급해 주세요."

        # GPT에게 리뷰 요청
        createChatCompletion({
            model: "gpt-3.5-turbo",
            messages: [
              { role: "system", content: "You are a helpful code reveiwer." },
              { role: "user", content: prompt }
            ]
          });

        review = response.choices[0].text.strip()

        # 리뷰 코멘트를 리스트에 추가
        review_comments.append(f"### `{filename}`에 대한 코드 리뷰\n\n{review}\n")

# 리뷰 코멘트를 하나의 문자열로 결합
full_review_comment = "\n---\n".join(review_comments)

# PR에 코멘트 작성
pr.create_issue_comment(full_review_comment)
