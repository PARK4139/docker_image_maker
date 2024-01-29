@REM @echo off
chcp 65001

@Rem 윈도우즈에서는 docker desktop 을 실행시켜야 한다. 그렇지 않으면 error during connect: This error may indicate that the docker daemon is not running.: Post~~~ 에러 나온다
@Rem 자꾸 에러떠서 docker desktop 재설치를 했다.
@Rem 깃 허브로 docker 로그인
docker login -u park4139
도커허브인증토큰
@Rem docker desktop 재실행
explorer "C:\ProgramData\Microsoft\Windows\Start Menu\Docker Desktop.lnk"

@REM 도커이미지 빌드
docker build -t server_alpine_image -f server_alpine.Dockerfile . || wsl -e sh -c "echo -e '\033[0;31m도커이미지 빌드 실패\033[0m';" && timeout 600 > nul
docker image ls

@REM 도커컨테이너 실행 via interactive mode
@REM docker run -it server_alpine_image /bin/bash
docker run -it --name server_alpine_container -p 5000:5000 server_alpine_image:latest
docker run -d --name server_alpine_container -p 5000:5000 server_alpine_image:latest
@REM -d : Detached 모드(백그라운드 모드)


@REM # 실행된 도커컨테이너 에 명령 via interactive mode
ls
@REM # 현재 머신에 설치가능한 python3 최신 버전 확인
apk policy python3
python --version
python3 --version
pip --version
git --version
pip3 --version
docker --version
aws --version
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

@REM 도커컨테이너 확인(실행중인)
docker ps

@REM 도커컨테이너 확인(모든)
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

@REM  도커이미지 빌드 프로젝트 PUSH (to 깃허브)
set commit_ment=fastapi 서버 도커파일 local test 완료
set commit_ment=alpine linux 로 컨버팅 중인 커스텀 패키지
git add *
git commit -m "%commit_ment%"
git push -u origin main
git status | find "working tree clean"


@REM  도커이미지 PUSH (to 도커허브)
docker logs -f 도커컨테이너ID
@REM 도커이미지 PUSH 전 태그명 변경
docker tag server_alpine_image park4139/server_alpine_image
@REM 도커이미지 PUSH
docker push park4139/server_alpine_image


@REM 참고자료 도커 공식 유튜브채널 영상 https://www.youtube.com/watch?v=iqqDU2crIEQ
@REM docker-compose up -d



@REM 알파인리눅스 컨테이너 내에서 fastapi 서버 컨테이너를 실행해보자.
@REM service docker start

@REM 도커이미지 PULL
@REM docker pull park4139/server_alpine_image:latest
docker pull park4139/server_fastapi_image:latest
docker images
docker logout


@REM 도커이미지 PULL 한것 실행
docker run --name server_fastapi_container -p 8080:80 park4139/server_fastapi_image:latest


docker-compose up -d
@REM 참고자료 도커 공식 유튜브채널 영상 https://www.youtube.com/watch?v=iqqDU2crIEQ



@REM 익숙해지면 docker-compose 또는 k8s 써보자


우분투 제어
    '너가 있으니 나도 있다' by 남아프리카 부족 언어
    whoami # 리눅스아이디 아는 법, root 슈퍼관리자ID, 계정만들기
    apt-get update # 패키지인덱스 업데이트
    apt-get upgrade # 함부로 하면 안됨.
    apt-get install 우분투패키지명
    apt-get remove 우분투패키지명
    apt-get --purge remove 우분투패키지명 # --purge 설정파일도 삭제
    https://www.youtube.com/watch?v=890m7fWHWH4  # 우분투 20.04 에 docker 설치
리눅스명령어 실행 (as 백그라운드 프로세스)
    echo "test" &

리눅스파일 제어
    cp -rf * 새SRC폴더명
    chmod -R 777 directory # 모든권한부여 with walking
    chmod -R 400 directory # 모든권한설정 with walking(directory의 소유자 읽기만 허용)
    rm -rf * # 리눅스파일 삭제 (모든파일삭제)
    ls -l

리눅스파일 소프트링크 확인 # 윈도우의 바로가기의 주소와 동등
    ls -al
    ln -s foo_1.txt foo_2.txt

리눅스프로세스 제어 # 리눅스에는 휴지통이 없다.
    ps aux | grep 프로세스명
    kill -9 프로세스ID
    ctrl c # 프로세스 종료

echo ${USER}
sudo usermod -aG docker ${USER}





service docker status




@REM 익숙해지면 docker-compose 또는 k8s 써보자

