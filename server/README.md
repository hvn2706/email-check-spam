# Spam email detection

## 1. Description
This is a spam email detection service. It is a REST API that receives an email and returns a boolean value indicating whether the email is spam or not.

## 2. How to run
1. Install python ~ 3.10
2. Install the requirements

    ```pip install -r requirements.txt```
3. Run the server

    ```python main.py``` or ```uvicorn main:app --host 0.0.0.0 --port 8000```

- Recommend running on a virtual environment
## 3. Test api

```
curl --location 'http://localhost:8000/api/v1/email-spam-detection' \
--header 'Content-Type: application/json' \
--data '{
    "subject": "[TB] Báo cáo Thị trường chung cư Hà Nội 2023 mới cập nhật",
    "content": "Báo cáo tổng quan. Cung cấp thông tin về bối cảnh kinh tế cùng, tổng quan thực trạng phân khúc nhà ở Hà Nội. Góc nhìn của chuyên gia. Xu hướng chung cư trung, cao cấp dưới góc nhìn chính sách và pháp lý, xu thế tất yếu của đô thi hiện đại"
}'
```
