# docker로 리눅스를 띄우고 그 안에서 python fastapi 서버를 구동하고 싶어
# python3.12.0 부터 지원된 문법인 f-string 문법을 전부 뜯어내야한다....다운그레이드..과도한시간소요예상
# 일단은 다운그래이드 방법을 조사해보니 requirement.txt 만들어서 pkg 명만 모두 추출해서 venv 날리고 새로 venv 설치 후 pip install 하면 된다.

# 베이스 이미지 선택 (예: Ubuntu 22.04)
# FROM ubuntu:20.04
#fail # ubuntu:22.04 도 python3.12.0 지원 안함...아... python 프로젝트의 버전을 너무 높이지 말걸 그랬다.
# ubuntu:22.04 에 python3.12.0 설치하는 방법이 있긴 한데, 추천되지 않는 방법이고, 잠재적인 문제가 있을 수 있다. 아니 있다고 가정하고 써야하나 보다.
# FROM ubuntu:22.04
# alpine linux 기반 이미지, 경량화에 특화된 docker 공식 이미지, pyton3.12.0 가능한 것 같아 보여 시도. 안되면 ubuntu22.02 로 진행하고 파이썬프로젝트를 다운그래이드 하자...
# FROM alpine:latest
FROM alpine:3.14

# 필요한 패키지 설치
# fail
# apt-get은 Debian 계열 리눅스에서 사용되는 패키지 관리 도구이므로 Alpine Linux에서 apt-get을 사용할 수 없습니다.
# 도커에서는 못 쓰는 것 같다.
# RUN run_command() {
#     $1 || (echo -e "\e[31m명령어 실행 실패했습니다.\e[0m" && sleep 600)
# }
# RUN run_command "apt install apt"
# RUN run_command "apt-get update"
# RUN run_command "apt-get install -y python3.12"
# RUN run_command "apt-get install -y python3-pip"
#fail
# RUN "apt-get update"
# RUN "apt-get install -y python3.12"
# RUN "apt-get install -y python3-pip"

# commands for alpine linux
RUN apk update
# RUN apk upgrade # upgrade 는 함부로 하면 안된다는데?
# RUN apk add py3-pip
# RUN apk add --no-cache mysql-client
# ENV PYTHONUNBUFFERED=1
# RUN apk add --update --no-cache python3
# RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
# RUN python3 -m ensurepip
# RUN pip3 install --no-cache --upgrade pip setuptools


# RUN apt-get update
# RUN apt-get upgrade -y
# # Ubuntu 22.04에 Python 3.12를 지원안됨.. Python 3.12를 설치하기 위한 써드파티 의존성 설치, https://www.linuxtuto.com/how-to-install-python-3-12-on-ubuntu-22-04/ 참고
# RUN apt-get install software-properties-common -y
# RUN add-apt-repository ppa:deadsnakes/ppa
# # 방금 새 패키지 저장소 소스를 추가했으므로 다음 명령을 사용하여 APT 데이터베이스를 동기화해야 합니다.
# RUN apt update


# 지역설정 답변을 자동화 해야하는데 어떻게 한데?
# python3.12.0 설치 시 => => # Geographic area: 라면서 진행이 안되는 문제 대안, Locale 설정을 해줌, Dockerfile 내에서 ARG로 환경 변수를 정의합니다.
# ARG LANG=en_US.UTF-8
# ENV LANG ${LANG}
# ENV LANGUAGE ${LANG}
# ENV LC_ALL ${LANG}

# Geographic area:  설정은 어떻게 해?
# Python 3.12 설치 전 "Geographic area" 설정
# RUN echo "tzdata tzdata/Areas select Asia" | debconf-set-selections
# RUN echo "tzdata tzdata/Zones/Asia select Seoul" | debconf-set-selections

# 명령어에 답변을 자동화 해야하는데 어떻게 한데?
# apt-get 명령어를 noninteractive 모드로 설정, reserved sentence 인 듯.
# ARG DEBIAN_FRONTEND=noninteractive
# ARG DEBIAN_FRONTEND=noninteractive 쓰면 추후에 문제 발생할 수 있는 부분 알려줘
# GPT-3.5 : 'ARG DEBIAN_FRONTEND=noninteractive'를 사용하면 추후에 문제가 발생할 수 있는 몇 가지 주의사항이 있습니다.
# 대화식 프롬프트 요구: 일부 패키지 설치 중에는 대화식 프롬프트를 통해 추가적인 설정이나 사용자 입력이 필요한 경우가 있을 수 있습니다. 이 경우 'noninteractive' 모드로 설정하면 자동으로 기본값이 선택되거나 오류가 발생할 수 있습니다. 따라서, 이러한 상황에서는 대화식 모드로 전환하여 사용자 입력을 받을 수 있도록 해야 합니다.
# 기본값 변경: 패키지 설치 중에는 기본값을 변경해야 하는 경우가 있을 수 있습니다. 예를 들어, 패키지의 라이선스 동의, 서버 설정 등을 변경해야 하는 경우가 있을 수 있습니다. 'noninteractive' 모드에서는 기본값이 자동으로 선택되므로, 필요한 설정을 변경하지 못하고 기본값으로 설치될 수 있습니다.
# 동작 일관성: 'noninteractive' 모드를 사용하면 Docker 이미지를 다른 환경에서 재사용할 때 동작 일관성이 보장되지 않을 수 있습니다. 다른 환경에서는 대화식 모드로 실행되어 추가적인 설정이 요구될 수 있으며, 이미지가 이러한 설정을 자동으로 처리하지 못할 수 있습니다.
# 따라서, 'noninteractive' 모드를 사용할 때는 이러한 주의사항을 염두에 두고 사용해야 합니다. 필요에 따라 대화식 모드로 전환하여 사용자 입력을 받거나 추가적인 설정을 변경할 수 있도록 처리해야 합니다.
# RUN apt-get update && apt-get install -y --no-install-recommends tzdata
# ENV TZ=Asia/Seoul


# RUN apt-get install -y curl
RUN apk --no-cache add curl
# RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12
# RUN pip3.12 -V


# /code 폴더 생성 후 이동
WORKDIR /code

# 현재작업디렉토리의 특정파일 특정디렉토리 도커이미지로 복사 한번에
# COPY . /code/

# 현재작업디렉토리의 특정파일 특정디렉토리 도커이미지로 복사 각각
# COPY ./py_pkg_ver_for_linux.log /code/py_pkg_ver_for_linux.log
# COPY ./pkg_park4139_for_linux /code/pkg_park4139_for_linux

# Python 3.12를 기본 Python3으로 사용
# RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 2
# RUN update-alternatives --config python3

# RUN apt-get remove -y python3.10
# RUN apt-get remove -y python3-pip
# RUN apt-get install -y python3-pip
# RUN apt-get update
# for python-pip3을 주로 설치하거나 get-pip.py file을 통하여 설치할 때가 많은데, 이 때 우분투 모듈과의 버전 문제 등 호환 문제 해결
# RUN apt-get install -y python3.12-distutils
# RUN apt-get install -y python3.12-dev
# RUN apt-get install -y python3-apt
# RUN python3 -m ensurepip --upgrade
# RUN python3.12 -m pip install setuptools
# RUN python3 -m pip install setuptools
# py_pkg_ver_for_linux.log 를 보고 파이썬 프로그램 종속 모듈 전체 설치(-r)
# Q. --no-cache-dir , 도커레이어 캐싱, 이 과정에서 개발자들은 좋은개발경험으로서 시간을절약. 이 옵션 뭐야? 새버전 패키지 설치할때 불안하니까 넣는 옵션으로 봐도 될까? 네, 캐시를 사용하지 않는 옵션입니다
# RUN pip install --no-cache-dir --upgrade -r /code/py_pkg_ver_for_linux.log
# RUN pip3.12 install --no-cache-dir --upgrade -r /code/py_pkg_ver_for_linux.log
# RUN pip3 install --no-cache-dir --upgrade -r /code/py_pkg_ver_for_linux.log
# RUN pip install --upgrade -r /code/py_pkg_ver_for_linux.log
# RUN pip install --no-cache-dir --upgrade -r /code/py_pkg_ver_for_linux.log
# COPY ./fastapi_server.py /code/
# alipine linux 에서는 systemctl 를 runit 로 대체하는 사용하는 경우가 높은 확률
# RUN apk --no-cache add runit
RUN apk --no-cache add vim
RUN apk --no-cache add git
RUN apk --no-cache add ffmpeg
RUN apk --no-cache add python3
RUN apk --no-cache add docker
RUN apk --no-cache add docker-compose
# RUN apk --no-cache add rc-service
# mutagen 패키지을 사용하기 위한 종속성
# RUN apk --no-cache add build-base libffi-dev
# docker 패키지을 사용하기 위한 종속성
# RUN apk --no-cache add --update docker-cli
# RUN apk --no-cache add --update docker openrc
# RUN rc-update add docker boot
# RUN reboot
# AWS CLI 설치
# RUN pip3 --no-cache-dir install awscli
RUN apk update


# Docker 서비스를 시작, 이게 도커데스크탑 실행하는 것과 동등한 것 같아 보이는데, 아 이게 도커데몬 실행을 의미하는 거구나.
# 알파인 리눅스에서 Docker 서비스를 부팅 시 자동으로 시작하도록 설정하는 방법
# 설정 전에는 interactive mode 로 alpine linux 를 실행해야하니 주석처리하고,
# 설정 후에는 docker container 랑 전부 정의하고 주석해제하자.
# CMD dockerd
# RUN systemctl enable docker
# Q. RUN systemctl enable docker 랑  CMD dockerd 는 둘 중 하나만 쓰면 되는거야? 네 맞습니다.
# docker 데몬 시작
# systemctl start docker
