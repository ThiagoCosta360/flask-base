FROM python:3.8.5-slim-buster

COPY . .

RUN pip install -r ./requirements.txt

CMD ["python3", "run_server.py", "run", "-h", "0.0.0.0"]
