FROM python:3.10.4-slim-buster
WORKDIR /app
ADD requirements.txt /app/
ADD .env.example /app/.env

RUN pip install -r requirements.txt
ADD . /app/

# start app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]