# 특정버전 파이썬을 설치해 놓은 alpine, 근데 python 을 바로 실행함....linux interactive mode에서 명령어 사용 안되는 것 같아 보임..
FROM python:3.12.0-alpine

# 필요한 종속성 도커이미지 에 저장 (refer to fastapi offical docker sample)
WORKDIR /code
COPY . .
RUN pip install --no-cache-dir --upgrade colorama
RUN pip install --no-cache-dir --upgrade bs4
RUN pip install --no-cache-dir --upgrade uvicorn
RUN pip install --no-cache-dir --upgrade fastapi
RUN pip install --no-cache-dir --upgrade mutagen
RUN pip install --no-cache-dir --upgrade numpy
RUN pip install --no-cache-dir --upgrade pyglet
RUN pip install --no-cache-dir --upgrade send2trash
RUN pip install --no-cache-dir --upgrade toml
RUN pip install --no-cache-dir --upgrade googletrans
RUN pip install --no-cache-dir --upgrade gtts
RUN pip install --no-cache-dir --upgrade mutagen
RUN pip install --no-cache-dir --upgrade pydantic
RUN pip install --no-cache-dir --upgrade pytube
RUN pip install --no-cache-dir --upgrade tqdm

# chcp 65001 대체
RUN export LANG=en_US.UTF-8

# RUN pip install --no-cache-dir --upgrade -r /code/server_fastapi_py_pkg_ver.log
CMD ["uvicorn", "server_fastapi:app", "--host", "0.0.0.0", "--port", "80"]
# CMD ["uvicorn", "server_fastapi:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"] # nginx 를 proxy 로 앞에 둘거면 "--proxy-headers" 옵션을 추가하세요 - fastapi 공식 문서 -


