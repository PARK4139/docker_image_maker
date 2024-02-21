# 2023 12 07 17 07 apply %%%FOO%%% via dev tool auto increament
# -*- coding: utf-8 -*-
__author__ = 'PARK4139 : Jung Hoon Park'

import inspect
import random
from uuid import uuid4

from fastapi import APIRouter

from pkg_park4139_for_linux import DebuggingUtil, BusinessLogicUtil, FastapiUtil, StateManagementUtil, SecurityUtil

router = APIRouter()


@router.get("/더미멤버들생성")  # todo 더미데이터 구조 수정해야 한다.
def get_dummies():
    todos = StateManagementUtil.todos  # 리스트에 저장, 런타임 중에만 저장이 유지됨, 앱종료 시 데이터 삭제
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")
    print("애플리케이션 시작 시 실행되어야 하는 초기화 작업을 수행합니다.")
    # todos: [todo] 에 저장
    # dummy_cnt = random.randint(1, 100)
    dummy_cnt = 100
    for _ in range(dummy_cnt):
        todo_dummy = {
            # 수정해야한다. 여기 내용들
            'id': uuid4().hex + BusinessLogicUtil.get_time_as_('%Y%m%d%H%M%S%f') + SecurityUtil.get_random_alphabet(),
            'pw': SecurityUtil.get_random_int(),  # 암호화 모듈 필요, get_random_int() 는 아직 미완성.
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
        todos.append(todo_dummy)
    [print(sample) for sample in todos]
    DebuggingUtil.print_ment_success(f"더미를 추가로 {dummy_cnt} 개 생성하였습니다 총 {len(todos)}개의 데이터가 todos 리스트에 저장되어 있습니다")
    return todos


@router.get("/todos")
def get_todos():
    todos = StateManagementUtil.todos  # 리스트에 저장, 런타임 중에만 저장이 유지됨, 앱종료 시 데이터 삭제
    return todos


@router.get("/todo")
def get_todos(id: str):
    todos = StateManagementUtil.todos  # 리스트에 저장, 런타임 중에만 저장이 유지됨, 앱종료 시 데이터 삭제
    for todo_ in todos:
        if todo_['id'] == id:
            print(rf'todo_ : {todo_}')
            return {"message": "Todo got successfully"}
    return {"message": "Todo not found"}


@router.post("/todo")
def create_todo(todo: FastapiUtil.TodoItem):
    todos = StateManagementUtil.todos  # 리스트에 저장, 런타임 중에만 저장이 유지됨, 앱종료 시 데이터 삭제
    todo_ = todo.model_dump()
    todo_['id'] = uuid4().hex + BusinessLogicUtil.get_time_as_('%Y%m%d%H%M%S%f') + SecurityUtil.get_random_alphabet()
    print(rf"todo_['id'] : {todo_['id']}")
    todos.append(todo_)
    return {"message": "Todo posted successfully"}


@router.put("/todo")
def update_todo(id: str, todo: FastapiUtil.TodoItem):
    todos = StateManagementUtil.todos  # 리스트에 저장, 런타임 중에만 저장이 유지됨, 앱종료 시 데이터 삭제
    for todo_ in todos:
        if todo_['id'] == id:
            todo_['title'] = todo.title
            todo_['completed'] = todo.completed
            return {"message": "Todo updated successfully"}
    return {"message": "Todo not found"}


@router.delete("/todo")
def delete_todo(id: str):
    todos = StateManagementUtil.todos  # 리스트에 저장, 런타임 중에만 저장이 유지됨, 앱종료 시 데이터 삭제
    for todo_ in todos:
        if todo_['id'] == id:
            # todo_.remove(todo_)
            del todo_
            return {"message": "Todo deleted successfully"}
    return {"message": "Todo not found"}
