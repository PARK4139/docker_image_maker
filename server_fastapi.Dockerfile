# 특정버전 파이썬을 설치해 놓은 alpine,
# 근데 python 을 바로 실행함....linux interactive mode에서 명령어 사용 안되는 것 같아 보임..
# python:3.12.0-alpine 는 alphine linux 에 python3.12 가 설치되어 도커허브 공식 도커이미지,
# python:3.12.0-alpine 선정이유는 alpine linux 최신버전에서 3.12 가 지원되지 않았기 때문
FROM python:3.12.0-alpine

# 필요한 종속성 도커이미지 에 저장 (refer to fastapi offical docker sample)
WORKDIR /code
# .dockerignore 에 작성해두어서 COPY . . 를 써도 필요한 것만 도커컨테이너 안으로 복제됨
COPY . .



# 종속성 도커레이어 캐싱
#RUN pip install --upgrade pip
# 리눅스 설치 불가# 특정버전으로 설치하는 것 모두실패
# RUN pip install psutil
#RUN pip install pynput
# RUN pip install PIL
RUN #pip install ffmpeg
RUN pip install BlurWindow
RUN pip install clipboard
RUN pip install keyboard
RUN pip install PyAutoGUI
RUN pip install moviepy
RUN pip install Jinja2
RUN pip install uvicorn
RUN pip install fastapi
RUN pip install colorama
#RUN pip install bs4
RUN pip install beautifulsoup4
RUN pip install mutagen
RUN pip install numpy
RUN pip install pyglet
RUN pip install Send2Trash
RUN pip install toml
RUN pip install googletrans
RUN pip install gTTS
RUN pip install pydantic
RUN pip install pytube
RUN pip install tqdm
RUN pip install itsdangerous
RUN pip install SQLAlchemy
RUN pip install PyMySQL
RUN pip install python-multipart
RUN pip install openpyxl
RUN pip install pandas
# RUN pip install pyJWT
# RUN pip install cryptography
RUN pip install passlib[bcrypt]
RUN pip install python-jose[cryptography]




# chcp 65001 대체
RUN export LANG=en_US.UTF-8


# RUN pip install --no-cache-dir --upgrade -r /code/server_fastapi_py_pkg_ver.log
# success dev/op
CMD ["uvicorn", "server_fastapi:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
# "--proxy-headers" 옵션을 추가 nginx 서버를 proxy 서버로서 앞에 둘거면 - fastapi 공식 문서 -