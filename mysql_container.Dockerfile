FROM mysql:8.3.0


WORKDIR /code
#COPY . .




# chcp 65001 대체
RUN export LANG=en_US.UTF-8







CMD ["uvicorn", "server_fastapi:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
