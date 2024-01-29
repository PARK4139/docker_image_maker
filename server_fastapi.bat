@REM @echo off
chcp 65001

@Rem 윈도우즈에서는 docker desktop 을 실행시켜야 한다. 그렇지 않으면 error during connect: This error may indicate that the docker daemon is not running.: Post~~~ 에러 나온다
@Rem 자꾸 에러떠서 docker desktop 재설치를 했다.
@Rem 깃 허브로 docker 로그인
@Rem docker desktop 재실행




@REM 모든 파이썬 패키지 삭제
run cmd.exe as admin
echo %cd% | clip
cd C:\projects\services\docker_image_maker
call ".\venv\Scripts\activate.bat"
pip freeze > server_fastapi_py_pkg_ver.log
echo y | pip uninstall -r server_fastapi_py_pkg_ver.log
call ".\venv\Scripts\deactivate.bat"


@REM 모든 파이썬 패키지 재설치 및 저장, jetbrain venv 연결이 invaild 되면서 안되는데.
call ".\venv\Scripts\deactivate.bat"
echo y | rmdir /s ".\venv"
python -m venv venv
call ".\venv\Scripts\activate.bat"
pip list
restart IDE
alt enter 로 직접 패키지 수동 설치
@rem 패키지 수동 설치 결과 확인
call ".\venv\Scripts\activate.bat"
pip list
python.exe -m pip install --upgrade pip
connect IDE python interpreter to this
shift shift
python interpreter
echo y | pip install -r server_fastapi_py_pkg_ver.log
pip list
pip freeze > server_fastapi_py_pkg_ver.log
type server_fastapi_py_pkg_ver.log


@REM 도커이미지 빌드
docker build -t server_fastapi_image -f server_fastapi.Dockerfile . || wsl -e sh -c "echo -e '\033[0;31m도커이미지 빌드 실패\033[0m';" && timeout 600 > nul

@REM 도커이미지 빌드 확인
docker image ls

@REM 도커컨테이너 실행 via interactive mode
@REM docker run -it --name server_fastapi_container -p 8080:80 server_fastapi_image:latest
@REM docker run --name server_fastapi_container -p 80:80 server_fastapi_image:latest
docker run --name server_fastapi_container -p 8080:80 server_fastapi_image:latest
@REM -d Detached 모드(백그라운드 모드)
@REM -v [호스트 디렉토리]:[컨테이너 디렉토리] 호스트의 디렉토리와 컨테이너의 디렉토리를 공유


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

@REM 도커컨테이너 중지/삭제
docker container ls -a | clip
docker stop 도커컨테이너ID
docker stop 4a6a3806c3ef
docker rm 도커컨테이너ID
docker rm 2ab83ef570fe
docker container ls -a
docker ps -a
docker ps -qa | clip

@REM 도커이미지 삭제
@REM docker rmi $(docker images -q)   linux 용
docker image ls | clip
docker rmi 도커이미지ID
docker rmi caa9184772a4
docker image ls
docker images -q | clip



@REM 도커이미지 삭제
@REM 도커데스크탑 에서 도커컨테이너 삭제, 이게 상당히 편하다


모든 도커컨테이너 삭제
@REM docker rm -f $(docker ps -qa)
echo y | docker container prune

모든 도커이미지 삭제
echo y | docker image prune -a

모든 도커컨테이너/도커이미지 삭제
echo y | docker container prune
echo y | docker image prune -a

@REM 익숙해지면 docker-compose 또는 k8s 써보자
