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
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from pkg_park4139_for_linux import DebuggingUtil, BusinessLogicUtil, FastapiUtil
from pkg_park4139_for_linux import StateManagementUtil

router = APIRouter()

BOOKS_JSON = StateManagementUtil.BOOKS_JSON


@router.get("/books-dummy-with-overwrite")
def make_books_dummy_with_overwrite():
    try:
        BOOKS_JSON = StateManagementUtil.BOOKS_JSON
        dummy_cnt = 100
        genres = ["러브코메디", "러브픽션", "러브액션"]
        names = ["내 청춘러브 코메디는 잘못되어 있어", "너에게 닿기를"]
        dummy_data = []
        for _ in range(dummy_cnt):
            book_dummy = {
                'id': uuid4().hex,
                'name': random.choice(names),
                'genre': random.choice(genres),
                'price': random.randint(1000, 10000),
            }
            dummy_data.append(book_dummy)

        # BOOKS_JSON 에 데이터 저장
        with open(BOOKS_JSON, "w", encoding="utf-8") as file:
            json.dump(dummy_data, file, ensure_ascii=False)

        DebuggingUtil.print_magenta(f"더미를 {dummy_cnt} 개로 리셋하였습니다")
        return {"message": f"더미를 {dummy_cnt} 개로 리셋하였습니다"}
    except:
        traceback.print_exc(file=sys.stdout)
        return {"detail": f"에러가 발생했습니다"}



@router.get("/books-dummy-without-overwrite")
def make_books_dummy_without_overwrite():
    try:
        # FileSystemUtil.explorer(fr"{settings.protocol_type[0]}://{settings.host[0]}:{settings.port[0]}/make-dummyies")
        BOOKS_JSON = StateManagementUtil.BOOKS_JSON

        # 기존의 BOOKS_JSON 데이터 가져오기
        with open(BOOKS_JSON, encoding="utf-8") as file:
            existing_data = json.load(file)

        dummy_data = existing_data
        # dummy_cnt = 100
        dummy_cnt = random.randint(1, 100)
        genres = ["러브코메디", "러브픽션", "러브액션"]
        names = ["내 청춘러브 코메디는 잘못되어 있어", "너에게 닿기를"]
        for _ in range(dummy_cnt):
            book_dummy = {
                'id': uuid4().hex,
                'name': random.choice(names),
                'genre': random.choice(genres),
                'price': random.randint(1000, 10000),
            }
            dummy_data.append(book_dummy)

        # BOOKS_JSON 에 데이터 저장
        with open(BOOKS_JSON, "w", encoding="utf-8") as file:
            json.dump(dummy_data, file, ensure_ascii=False)

        DebuggingUtil.print_magenta(f"더미를 추가로 {dummy_cnt} 개 생성하였습니다 총 {len(dummy_data)}개의 데이터가 {os.path.basename(BOOKS_JSON)}에 저장되어 있습니다")
        return {"message": f"더미를 추가로 {dummy_cnt} 개 생성하였습니다 총 {len(dummy_data)}개의 데이터가 {os.path.basename(BOOKS_JSON)}에 저장되어 있습니다"}
    except:
        traceback.print_exc(file=sys.stdout)
        return {"detail": f"에러가 발생했습니다"}


@router.get("/books")
async def list_books():
    try:
        BOOKS = FastapiUtil.init_and_update_json_file(BOOKS_JSON)
        # BusinessLogicUtil.print_json_via_jq_pkg(json_file=BOOKS_JSON)
        return {"books": BOOKS}
    except:
        traceback.print_exc(file=sys.stdout)
        return {"detail": f"에러가 발생했습니다"}


@router.get("/book-by-index/{index}")
async def book_by_index(index: int):
    try:
        BOOKS = FastapiUtil.init_and_update_json_file(BOOKS_JSON)
        if index < len(BOOKS):
            # BusinessLogicUtil.print_json_via_jq_pkg(json_str=BOOKS[index])
            return BOOKS[index]
        DebuggingUtil.print_ment_fail(f"book  인덱스 {index}이 범위({len(BOOKS)}) 밖에 있습니다.")
        # raise HTTPException(status_code=404, detail=f"Book index {index} out of range ({len(BOOKS)}).")
    except:
        traceback.print_exc(file=sys.stdout)
        return {"detail": f"에러가 발생했습니다"}

@router.get("/book")  # 골라야한다면 이게 나는 좋은데
async def book_by_id(id: str):
    try:
        BOOKS = FastapiUtil.init_and_update_json_file(BOOKS_JSON)
        for book in BOOKS:
            # if book.id == id:
            if book['id'] == id:
                # BusinessLogicUtil.print_json_via_jq_pkg(json_str=book)
                return book
        # raise HTTPException(status_code=404, detail=f"Book ID {id} not found in database.")
        DebuggingUtil.print_ment_fail(f"({len(BOOKS)})개의 등록된 books 중, id 가 {id}인 Book 이 없습니다.")
    except:
        traceback.print_exc(file=sys.stdout)
        return {"detail": f"에러가 발생했습니다"}


@router.get("/book")  # 이건 내 스타일이 아닌데...이게 보편적인지 확인해보고 싶다..원래 rest 스타일 준수하면 get 쓰면 안되는 것 아닌가? 써도 되나
async def get_book(id: str):
    try:
        BOOKS = FastapiUtil.init_and_update_json_file(BOOKS_JSON)
        for book in BOOKS:
            # if book.id == id:
            if book['id'] == id:
                # BusinessLogicUtil.print_json_via_jq_pkg(json_str=book)
                return book
        # raise HTTPException(status_code=404, detail=f"Book ID {id} not found in database.")
        DebuggingUtil.print_ment_fail(f"({len(BOOKS)})개의 등록된 books 중, id 가 {id}인 Book 이 없습니다.")
    except:
        traceback.print_exc(file=sys.stdout)
        return {"detail": f"에러가 발생했습니다"}

@router.post("/book")
async def add_book(book: FastapiUtil.Book):
    try:
        BOOKS = FastapiUtil.init_and_update_json_file(BOOKS_JSON)
        book.id = uuid4().hex  # id 를 hex 로 생성하여 할당
        json_book = jsonable_encoder(book)
        BOOKS.append(json_book)
        with open(BOOKS_JSON, "w", encoding="utf-8") as file:
            json.dump(BOOKS, file, ensure_ascii=False)
            # BusinessLogicUtil.print_json_via_jq_pkg(json_str=json_book)
        DebuggingUtil.print_magenta(f"book 이 성공적으로 생성되었습니다.")
        return {"id": F"{book.id} 가 {BOOKS_JSON} 에 저장되었습니다"}
    except:
        traceback.print_exc(file=sys.stdout)
        return {"detail": f"에러가 발생했습니다"}


@router.post("/book")  # 일단 1개만 success
async def create_book(book: FastapiUtil.Book):
    try:
        BOOKS = FastapiUtil.init_and_update_json_file(BOOKS_JSON)
        # 여기서 모두 업로드 하면 될 것 같은데
        # BOOKS.append(book) # fail
        BOOKS.append(book.model_dump())  # success
        with open(BOOKS_JSON, "w", encoding="utf-8") as file:
            json.dump(BOOKS, file, indent=4, ensure_ascii=False)
        DebuggingUtil.print_ment_light_white(rf'book : {book}')
        DebuggingUtil.print_magenta(f"book 이 성공적으로 생성되었습니다.")
        return {"message": "book 이 성공적으로 생성되었습니다."}
    except:
        traceback.print_exc(file=sys.stdout)
        return {"detail": f"에러가 발생했습니다"}


@router.put("/book")
async def update_book(id: str, updated_book: FastapiUtil.Book):
    try:
        BOOKS = FastapiUtil.init_and_update_json_file(BOOKS_JSON)
        for i, book in enumerate(BOOKS):
            if book["id"] == id:
                BOOKS[i] = updated_book.model_dump()  # 위에서 코드는 id 도 업데이트 시켜버린다.
                # BOOKS[i] = updated_book
                BOOKS[i]["id"] = id  # 기존 id 로 초기화
                with open(BOOKS_JSON, "w", encoding="utf-8") as file:
                    json.dump(BOOKS, file, indent=4, ensure_ascii=False)
                DebuggingUtil.print_ment_light_white(rf'book : {book}')
                DebuggingUtil.print_ment_light_yellow(f"아이디 {id} 인 book 이 성공적으로 업데이트되었습니다")
                return {"message": f"아이디 {id} 인 book 이 성공적으로 업데이트되었습니다"}
        # DebuggingUtil.print_ment_fail(f"데이터베이스에서 아이디 {id} 인 book 이 찾을 수 없습니다.")
    except:
        traceback.print_exc(file=sys.stdout)
        return {"detail": f"에러가 발생했습니다"}


@router.delete("/book")
async def delete_book(id: str):
    try:
        BOOKS = FastapiUtil.init_and_update_json_file(BOOKS_JSON)
        for i, book in enumerate(BOOKS):
            # if book.id== id:
            # print(rf'book["id"] : {book["id"]} id : {id}')
            if book["id"] == id:
                del BOOKS[i]
                # BOOKS.remove(book)
                with open(BOOKS_JSON, "w", encoding="utf-8") as file:
                    json.dump(BOOKS, file, indent=4, ensure_ascii=False)
                DebuggingUtil.print_ment_light_white(rf'book : {book}')
                DebuggingUtil.print_ment_red(f"아이디 {id} 인 book 이 성공적으로 삭제되었습니다.")
                return {"message": f"아이디 {id} 인 book 이 성공적으로 삭제되었습니다."}
        DebuggingUtil.print_ment_fail(f"데이터베이스에서 아이디 {id} 인 book 이 찾을 수 없습니다.")
    except:
        traceback.print_exc(file=sys.stdout)
        return {"detail": f"에러가 발생했습니다"}


@router.get("/book-random")
async def get_book_randomed():
    try:
        BOOKS = FastapiUtil.init_and_update_json_file(BOOKS_JSON)
        if len(BOOKS) > 0:
            book_choiced = random.choice(BOOKS)
            # BusinessLogicUtil.print_json_via_jq_pkg(json_list=book_choiced)
            return book_choiced
        else:
            DebuggingUtil.print_ment_fail(rf"{BOOKS_JSON}에 books가 없습니다")
            raise HTTPException(status_code=404, detail=f"{BOOKS_JSON}에 books가 없습니다")
    except:
        traceback.print_exc(file=sys.stdout)
        return {"detail": f"에러가 발생했습니다"}
