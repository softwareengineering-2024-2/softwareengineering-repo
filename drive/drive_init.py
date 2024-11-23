from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import os
import tempfile

# 구글 드라이브 API 초기화 함수
def init_drive_api():
    service_account_file = os.environ.get('GOOGLE_DRIVE_KEY_PATH')
    if not service_account_file:
        raise ValueError("환경변수 GOOGLE_DRIVE_KEY_PATH가 설정되지 않았습니다.")
    scopes = ["https://www.googleapis.com/auth/drive"]
    credentials = Credentials.from_service_account_file(service_account_file, scopes=scopes)

    drive_service = build('drive', 'v3', credentials=credentials)
    return drive_service

# 파일 업로드 함수
def upload_to_drive(file, file_name, folder_id):
    drive_service = init_drive_api()
     # 임시 파일에 업로드된 파일을 저장
    temp_file_path = None
    try:
        # 임시 파일 생성 및 저장
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file.read())
            temp_file_path = temp_file.name

        # MediaFileUpload로 업로드
        media = MediaFileUpload(temp_file_path, mimetype=file.content_type, resumable=True)
        file_metadata = {
            "name": file_name,
            "parents": [folder_id]
        }
        uploaded_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, webViewLink"
        ).execute()

        # 파일 권한 설정
        permission = {
            "type": "anyone",
            "role": "reader"
        }
        drive_service.permissions().create(
            fileId=uploaded_file.get("id"),
            body=permission
        ).execute()
        
        return {
            "id": uploaded_file.get("id"),
            "webViewLink": uploaded_file.get("webViewLink")
        }

    finally:
        # 임시 파일 삭제
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except PermissionError:
                print(f"파일 삭제 실패: {temp_file_path}. 다른 프로세스에서 사용 중일 수 있습니다.")

# 파일 삭제 함수
def delete_file_from_drive(file_id):
    drive_service = init_drive_api()
    drive_service.files().delete(fileId=file_id).execute()
    return True