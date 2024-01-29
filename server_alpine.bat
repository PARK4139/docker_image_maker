@REM @echo off
chcp 65001

@Rem 윈도우즈에서는 docker desktop 을 실행시켜야 한다. 그렇지 않으면 error during connect: This error may indicate that the docker daemon is not running.: Post~~~ 에러 나온다
@Rem 자꾸 에러떠서 docker desktop 재설치를 했다.
@Rem 깃 허브로 docker 로그인
@Rem docker desktop 재실행

@REM 도커이미지 빌드
docker build -t server_alpine_image -f server_alpine.Dockerfile . || wsl -e sh -c "echo -e '\033[0;31m도커이미지 빌드 실패\033[0m';" && timeout 600 > nul

@REM 도커이미지 빌드 확인
docker image ls

@REM 도커컨테이너 실행 via interactive mode
@REM docker run -it server_alpine_image /bin/bash
docker run -it --name server_alpine_container -p 5000:5000 server_alpine_image:latest
docker run -d -it --name server_alpine_container -p 5000:5000 server_alpine_image:latest
@REM -d : Detached 모드(백그라운드 모드)

@REM # 실행된 도커컨테이너 에 명령 via interactive mode
ls
@REM # 현재 머신에 설치가능한 python3 최신 버전 확인
apk policy python3
python --version
python3 --version
pip --version
pip3 --version
@REM apt-get install python3.12-dev
@REM python3.12 -m pip install --upgrade setuptools
@REM python3 -m ensurepip --upgrade
@REM python3 get-pip.py
@REM python3 -m pip.pyz --help
@REM pip install --upgrade setuptools
@REM pip install --no-cache-dir --upgrade -r /code/py_pkg_ver_for_linux.log
@REM # alphine linux 에 python3.12 가 설치되어 있는 도커이미지 발견, 이거 써보자
exit
@rem 도커컨테이너 수행내용 새로운이미지에 저장
docker commit 컨테이너ID 새로운이미지명

@REM 실행중인 도커컨테이너 확인
docker ps

@REM 모든 도커컨테이너 확인
docker ps -a

@REM 특정 도커컨테이너 실행(attached mode, interactive mode)
docker ps -a
docker start -ai 도커컨테이너ID
docker start -ai 99daddc88ffd

@REM 도커컨테이너 중지
docker container ls -a | findstr server_alpine_container
docker container ls -a | clip
docker stop 도커컨테이너ID
docker stop 99daddc88ffd
docker container ls -a
docker ps -a

@REM 도커컨테이너 삭제
docker container ls -a | findstr server_alpine_container
docker container ls -a | clip
docker rm 도커컨테이너ID
docker rm 99daddc88ffd
docker container ls -a
docker ps -a

@REM 도커이미지 삭제
@REM docker rmi $(docker images -q)   linux 용
docker image ls | clip
docker rmi 도커이미지ID
docker rmi ef3c64bd5725
docker image ls



@REM  GIT PUSH
set commit_ment=fastapi 서버 도커파일 local test 완료
git add *
git commit -m "%commit_ment%"
git push -u origin main
git status | find "working tree clean"



@REM 익숙해지면 docker-compose 또는 k8s 써보자
