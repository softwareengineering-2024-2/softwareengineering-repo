# Python 3.8 슬림 이미지 사용
FROM python:3.8-slim

# 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev \
    libmariadb-dev-compat \
    pkg-config \
    && apt-get clean

# 작업 디렉토리 설정
WORKDIR /app

# 프로젝트 파일 복사
COPY . /app

# Python 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# Flask 애플리케이션 실행
CMD ["python", "app.py"]
