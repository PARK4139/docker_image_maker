# 2023 12 07 17 07 apply %%%FOO%%% via dev tool auto increament
# -*- coding: utf-8 -*-
__author__ = 'PARK4139 : Jung Hoon Park'

import json
import os
import random
import sys
import traceback
from uuid import uuid4

from fastapi import APIRouter

from pkg_park4139_for_linux import DebuggingUtil, BusinessLogicUtil, FastapiUtil, SecurityUtil
from pkg_park4139_for_linux import StateManagementUtil

router = APIRouter()

USERS_JSON = StateManagementUtil.USERS_JSON


@router.put("/user-dummys/reset")
def put_user_dummys_reset():
    try:
        # FileSystemUtil.explorer(fr"{settings.protocol_type[0]}://{settings.host[0]}:{settings.port[0]}/make-dummy")
        USERS_JSON = StateManagementUtil.USERS_JSON
        dummy_cnt = 100
        dummy_data = []
        for _ in range(dummy_cnt):
            dummy_sample = {
                'id': uuid4().hex + BusinessLogicUtil.get_time_as_('%Y%m%d%H%M%S%f') + SecurityUtil.get_random_alphabet(),
                'pw': random.randint(00000, 99999),
                'name': random.choice(['김지영', '이민준', '박서연', '최영희', '정민재', '한지수', '서예진', '윤승우', '신하늘', '오준호', '류지현', '임동혁', '송지우', '홍민지', '강성민', '권수진', '신동욱', '최선영', '이지원', '김민재', '정서영', '박준형', '황예린', '강민호', '신지민', '이서연', '한승민', '조윤서', '김동현', '양미경']),
                'date_join': random.choice(['202401270047888999', '202401270047888999']),
                'date_logout_last': random.choice(['202401270047888999', '202401270047888999']),
                'address_house': random.choice(
                    ["서울특별시 강남구 역삼동 123-45", "경기도 성남시 분당구 정자동 678-90", "부산광역시 해운대구 우동 12-34", "인천광역시 남구 주안동 56-78", "대구광역시 수성구 만촌동 901-23", "광주광역시 서구 화정동 45-67", "대전광역시 유성구 도룡동 89-01", "울산광역시 남구 삼산동 234-56", "세종특별자치시 도움2로 78", "경기도 고양시 일산동구 백석동 34-56", "강원도 춘천시 소양동 78-90", "충청북도 청주시 상당구 용암동 123-45", "충청남도 천안시 동남구 신방동 67-89", "전라북도 전주시 완산구 효자동 90-12", "전라남도 목포시 상동 34-56", "경상북도 포항시 북구 흥해읍 78-90",
                     "경상남도 창원시 의창구 봉림동 123-45", "제주특별자치도 제주시 이도이동 56-78", "서울특별시 종로구 종로1가 90", "경기도 수원시 팔달구 인계동 12", "부산광역시 동래구 명장동 34", "인천광역시 부평구 부평동 56", "대구광역시 중구 동인동 78", "광주광역시 남구 봉선동 90", "대전광역시 서구 월평동 12", "울산광역시 중구 성남동 34", "세종특별자치시 조치원읍 56", "경기도 안산시 상록구 본오동 78", "강원도 원주시 일산동 90"]),
                'address_e_mail': random.choice(
                    ["example1@gmail.com", "example2@yahoo.com", "example3@hotmail.com", "example4@naver.com", "example5@daum.net", "example6@kakao.com", "example7@outlook.com", "example8@icloud.com", "example9@nate.com", "example10@hanmail.net", "example11@google.com", "example12@yahoo.co.kr", "example13@hotmail.co.kr", "example14@naver.com", "example15@daum.net", "example16@kakao.com",
                     "example17@outlook.com", "example18@icloud.com", "example19@nate.com", "example20@hanmail.net", "example21@gmail.com", "example22@yahoo.com", "example23@hotmail.com", "example24@naver.com", "example25@daum.net", "example26@kakao.com", "example27@outlook.com", "example28@icloud.com", "example29@nate.com", "example30@hanmail.net"]),
                'number_phone': random.choice(
                    ["010-1234-5678", "02-9876-5432", "031-111-2222", "051-333-4444", "032-555-6666", "053-777-8888", "064-999-0000", "042-111-2222", "062-333-4444", "051-555-6666", "053-777-8888", "064-999-0000", "010-1234-5678", "02-9876-5432", "031-111-2222", "051-333-4444", "032-555-6666", "053-777-8888", "064-999-0000", "042-111-2222", "062-333-4444", "051-555-6666", "053-777-8888",
                     "064-999-0000", "010-1234-5678", "02-9876-5432", "031-111-2222", "051-333-4444", "032-555-6666", "053-777-8888", "064-999-0000"]),
            }
            dummy_data.append(dummy_sample)
        with open(USERS_JSON, "w", encoding="utf-8") as file:
            json.dump(dummy_data, file, ensure_ascii=False)
        DebuggingUtil.print_magenta(f"더미를 {dummy_cnt} 개로 리셋하였습니다")
        return dummy_data
    except:
        traceback.print_exc(file=sys.stdout)
        return {"detail": f"에러가 발생했습니다"}


@router.post("/user-dummys")
def post_user_dummys():
    try:
        USERS_JSON = StateManagementUtil.USERS_JSON
        with open(USERS_JSON, encoding="utf-8") as file:
            existing_data = json.load(file)
        dummy_data = existing_data
        dummy_cnt = random.randint(1, 100)

        for _ in range(dummy_cnt):
            dummy_sample = {
                'id': uuid4().hex + BusinessLogicUtil.get_time_as_('%Y%m%d%H%M%S%f') + SecurityUtil.get_random_alphabet(),
                'pw': random.randint(00000, 99999),

                'name': random.choice(['김지영', '이민준', '박서연', '최영희', '정민재', '한지수', '서예진', '윤승우', '신하늘', '오준호', '류지현', '임동혁', '송지우', '홍민지', '강성민', '권수진', '신동욱', '최선영', '이지원', '김민재', '정서영', '박준형', '황예린', '강민호', '신지민', '이서연', '한승민', '조윤서', '김동현', '양미경']),
                'date_join': random.choice(['202401270047888999', '202401270047888999']),
                'date_logout_last': random.choice(['202401270047888999', '202401270047888999']),
                'address_house': random.choice(
                    ["서울특별시 강남구 역삼동 123-45", "경기도 성남시 분당구 정자동 678-90", "부산광역시 해운대구 우동 12-34", "인천광역시 남구 주안동 56-78", "대구광역시 수성구 만촌동 901-23", "광주광역시 서구 화정동 45-67", "대전광역시 유성구 도룡동 89-01", "울산광역시 남구 삼산동 234-56", "세종특별자치시 도움2로 78", "경기도 고양시 일산동구 백석동 34-56", "강원도 춘천시 소양동 78-90", "충청북도 청주시 상당구 용암동 123-45", "충청남도 천안시 동남구 신방동 67-89", "전라북도 전주시 완산구 효자동 90-12", "전라남도 목포시 상동 34-56", "경상북도 포항시 북구 흥해읍 78-90",
                     "경상남도 창원시 의창구 봉림동 123-45", "제주특별자치도 제주시 이도이동 56-78", "서울특별시 종로구 종로1가 90", "경기도 수원시 팔달구 인계동 12", "부산광역시 동래구 명장동 34", "인천광역시 부평구 부평동 56", "대구광역시 중구 동인동 78", "광주광역시 남구 봉선동 90", "대전광역시 서구 월평동 12", "울산광역시 중구 성남동 34", "세종특별자치시 조치원읍 56", "경기도 안산시 상록구 본오동 78", "강원도 원주시 일산동 90"]),
                'address_e_mail': random.choice(
                    ["example1@gmail.com", "example2@yahoo.com", "example3@hotmail.com", "example4@naver.com", "example5@daum.net", "example6@kakao.com", "example7@outlook.com", "example8@icloud.com", "example9@nate.com", "example10@hanmail.net", "example11@google.com", "example12@yahoo.co.kr", "example13@hotmail.co.kr", "example14@naver.com", "example15@daum.net", "example16@kakao.com",
                     "example17@outlook.com", "example18@icloud.com", "example19@nate.com", "example20@hanmail.net", "example21@gmail.com", "example22@yahoo.com", "example23@hotmail.com", "example24@naver.com", "example25@daum.net", "example26@kakao.com", "example27@outlook.com", "example28@icloud.com", "example29@nate.com", "example30@hanmail.net"]),
                'number_phone': random.choice(
                    ["010-1234-5678", "02-9876-5432", "031-111-2222", "051-333-4444", "032-555-6666", "053-777-8888", "064-999-0000", "042-111-2222", "062-333-4444", "051-555-6666", "053-777-8888", "064-999-0000", "010-1234-5678", "02-9876-5432", "031-111-2222", "051-333-4444", "032-555-6666", "053-777-8888", "064-999-0000", "042-111-2222", "062-333-4444", "051-555-6666", "053-777-8888",
                     "064-999-0000", "010-1234-5678", "02-9876-5432", "031-111-2222", "051-333-4444", "032-555-6666", "053-777-8888", "064-999-0000"]),
            }
            dummy_data.append(dummy_sample)

        # USERS_JSON 에 데이터 저장
        with open(USERS_JSON, "w", encoding="utf-8") as file:
            json.dump(dummy_data, file, ensure_ascii=False)

        DebuggingUtil.print_magenta(f"더미를 추가로 {dummy_cnt} 개 생성하였습니다 총 {len(dummy_data)}개의 데이터가 {os.path.basename(USERS_JSON)}에 저장되어 있습니다")
        return dummy_data
    except:
        traceback.print_exc(file=sys.stdout)
        return {"detail": f"에러가 발생했습니다"}


@router.get("/user-random")
async def get_user_random():
    try:
        USERS = FastapiUtil.init_and_update_json_file(USERS_JSON)
        if len(USERS) > 0:
            user_choiced = USERS[random.randint(0, len(USERS))]
            # BusinessLogicUtil.print_json_via_jq_pkg(json_list=user_choiced)
            DebuggingUtil.print_magenta(f"{USERS_JSON}에서 랜덤으로 user를 가져왔습니다")
            return user_choiced
        else:
            DebuggingUtil.print_magenta(rf"{USERS_JSON}에 users가 없습니다")
            return {"detail": f"{USERS_JSON}에 users가 없습니다"}
    except:
        traceback.print_exc(file=sys.stdout)
        return {"detail": f"에러가 발생했습니다"}


@router.get("/users")
async def get_users():
    USERS = FastapiUtil.init_and_update_json_file(USERS_JSON)
    # 예쁘게 json 출력
    # # BusinessLogicUtil.print_json_via_jq_pkg(json_file=USERS_JSON)

    # 일렬로 json 출력
    [print(sample) for sample in USERS]
    # return {"users": USERS}
    return USERS


@router.get("/user/{index}")
async def get_user_by_index(index: int):
    try:
        USERS = FastapiUtil.init_and_update_json_file(USERS_JSON)
        if index < len(USERS):
            # 예쁘게 json 출력
            # # BusinessLogicUtil.print_json_via_jq_pkg(json_str=USERS[index])

            # 일렬로 json 출력
            DebuggingUtil.print_ment_light_black(USERS[index])

            return USERS[index]
        DebuggingUtil.print_ment_fail(f"user  인덱스 {index}이 범위({len(USERS)}) 밖에 있습니다.")
        return {"detail": f"user  인덱스 {index}가 범위를 벗어났습니다 ({len(USERS)})."}
    except:
        traceback.print_exc(file=sys.stdout)
        return {"detail": f"에러가 발생했습니다"}


@router.post("/user")
async def post_user(user: FastapiUtil.User):
    try:
        USERS_JSON = StateManagementUtil.USERS_JSON
        with open(USERS_JSON, encoding="utf-8") as file:
            existing_data = json.load(file)
        user_data = {
            'id': user.id,
            'pw': user.pw,
            'name': user.pw,
            'date_join': user.date_join,
            'date_logout_last': user.date_logout_last,
            'address_house': user.address_house,
            'address_e_mail': user.address_e_mail,
            'number_phone': user.number_phone,
        }
        existing_data.append(user_data)
        # USERS_JSON 에 데이터 저장
        with open(USERS_JSON, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False)
        DebuggingUtil.print_magenta(f"{user_data} 를 {os.path.basename(USERS_JSON)}에 저장")
        return user_data
    except:
        traceback.print_exc(file=sys.stdout)
        return {"detail": f"에러가 발생했습니다"}


@router.get("/user")
async def get_user_by_id(id: str):
    try:
        USERS = FastapiUtil.init_and_update_json_file(USERS_JSON)
        for user in USERS:
            if user['id'] == id:
                # 예쁘게 json 출력
                # # BusinessLogicUtil.print_json_via_jq_pkg(json_str=user)

                # 일렬로 json 출력
                DebuggingUtil.print_ment_light_black(user)

                return user
        DebuggingUtil.print_ment_fail(f"({len(USERS)}).")
        return {"detail": f"아이디가 {id}인 User 이 없습니다"}
    except:
        traceback.print_exc(file=sys.stdout)

        return {"detail": f"에러가 발생했습니다"}


@router.put("/user")
async def put_user_by_id(user: FastapiUtil.User):
    try:
        USERS = FastapiUtil.init_and_update_json_file(USERS_JSON)
        for i, user_ in enumerate(USERS):
            if user_["id"] == user.id:
                USERS[i] = user.model_dump()  # 위에서 코드는 id 도 재초기화
                # USERS[i] = membe
                USERS[i]["id"] = user.id  # 기존 id 로 초기화
                with open(USERS_JSON, "w", encoding="utf-8") as file:
                    json.dump(USERS, file, indent=4, ensure_ascii=False)
                DebuggingUtil.print_ment_light_black(rf'user_ : {user_}')
                DebuggingUtil.print_ment_light_yellow(f"아이디 {user.id} 인 user 이 성공적으로 업데이트되었습니다")
                return {"message": f"아이디 {user.id} 인 user 이 성공적으로 업데이트되었습니다"}
        DebuggingUtil.print_ment_fail(f"데이터베이스에서 아이디 {user.id} 인 user 이 찾을 수 없습니다.")
        return {"detail": f"데이터베이스에서 아이디 {user.id} 인 user 을 찾을 수 없습니다"}
    except:
        traceback.print_exc(file=sys.stdout)

        return {"detail": f"에러가 발생했습니다"}


@router.delete("/user")
async def delete_user_by_id(id: str):
    try:
        USERS = FastapiUtil.init_and_update_json_file(USERS_JSON)
        for i, user in enumerate(USERS):
            if user["id"] == id:
                del USERS[i]
                # USERS.remove(user)
                with open(USERS_JSON, "w", encoding="utf-8") as file:
                    json.dump(USERS, file, indent=4, ensure_ascii=False)
                DebuggingUtil.print_ment_light_black(rf'user : {user}')
                DebuggingUtil.print_ment_red(f"아이디 {id} 인 user 이 성공적으로 삭제되었습니다.")
                return {"message": f"아이디 {id} 인 user 이 성공적으로 삭제되었습니다."}
        DebuggingUtil.print_ment_fail(f"데이터베이스에서 아이디 {id} 인 user 이 찾을 수 없습니다.")
        return {"detail": f"데이터베이스에서 아이디 {id} 인 user 이 찾을 수 없습니다."}
    except:
        traceback.print_exc(file=sys.stdout)

        return {"detail": f"에러가 발생했습니다"}


@router.delete("/users")
async def delete_users():
    try:
        # FileSystemUtil.explorer(fr"{settings.protocol_type[0]}://{settings.host[0]}:{settings.port[0]}/make-dummy")
        dummy_data = []
        # USERS_JSON 에 데이터 저장
        with open(USERS_JSON, "w", encoding="utf-8") as file:
            json.dump(dummy_data, file, ensure_ascii=False)

        DebuggingUtil.print_magenta(f"더미를 0 개로 리셋하였습니다")
        return dummy_data
    except:
        traceback.print_exc(file=sys.stdout)

        return {"detail": f"에러가 발생했습니다"}
