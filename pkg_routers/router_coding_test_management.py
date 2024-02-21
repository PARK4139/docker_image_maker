import inspect
import os
from datetime import timedelta
from typing import Annotated
from typing import Optional

import clipboard
from fastapi import APIRouter, UploadFile, HTTPException, File
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette import status

from pkg_park4139_for_linux import DebuggingUtil, SecurityUtil, StateManagementUtil, JwtUtil, MySqlUtil, FileSystemUtil, BusinessLogicUtil

templates = Jinja2Templates(directory=r"pkg_web/templates")

router = APIRouter()
router.mount("/static", StaticFiles(directory="pkg_web/static"), name="static")

prefix_promised = "web"  # /web 는 다른 파일에 작성된 부분이다. 라우터를 다른 파일로 분리했기 때문에 이 부분은 유지보수하며 알아내기가 까다롭다 # 하드코딩
# default_redirection_page_without_prefix = '/developer/tests/routing'
default_redirection_page_without_prefix = '/register'
default_redirection_page = f'/{prefix_promised}{default_redirection_page_without_prefix}'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="coding-test/jwt")
pw_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "IInrs6KU3n9pSsk5-5aUdKIjxsCQ51JdC3tzuihoKJw"  # python -c import secrets; print(secrets.token_urlsafe(32))' 해서 OS 환경변수에 저장
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# .env 파일을 공부를 해야한다. OS 환경변수에 직접 저장하는게 아닌 파일형태로 저장하는 것 처럼 보인다.
# 유의할 것은 .env 을 github에 저장되지 않도록 .gitignore 에 .env 를 등록
# 당연한 이야기 이지만 secret_key를 절대로 공개하지 않아야 한다.
# secret_key 정기적 변경
# CSRF 공격을 방지하기 위해 CSRF 공격 대비
# SQL injection 공격 대비


# api_key_header = APIKeyHeader(name="Token")
class data_register(BaseModel):
    name: str
    email: str
    # username: str
    # pw: str


class data_auth(BaseModel):
    token: str


class User(BaseModel):
    # username: str
    # full_name: Optional[str] = None
    # disabled: Optional[bool] = None
    name: Optional[str] = None
    token: Optional[str] = None
    email: Optional[str] = None


class UserInDB(User):
    pw_hashed: str


def verify_pw(pw_plain, pw_hashed):
    """return boolean"""
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")
    return pw_context.verify(pw_plain, pw_hashed)


def get_pw_hashed(pw_plain):
    """사용자를 평문 비밀번호를 jwt 로 만들기 전에 pw_plain을 pw_hashed 로 전처리 할때 사용하는 함수"""
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")
    return pw_context.hash(pw_plain)


def get_current_user_as_class(rs, form_data_username: str):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")
    if form_data_username in rs:
        current_user_dict = rs[form_data_username]
        return UserInDB(**current_user_dict)


def authenticate_user(form_data_username: str, form_data_password: str):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")

    # # jwt 생성
    # jwt = SecurityUtil.get_jwt(data=dict(user_as_dict[form_data_username]), secret_key=SECRET_KEY, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    # # jwt = SecurityUtil.get_jwt(data=form_data_username, secret_key=SECRET_KEY, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    # # DB에 JWT 유무 판단
    # rs = JwtUtil.get_jwts_by_token(db=MySqlUtil.get_session_local(), token=jwt)
    # [print(sample) for sample in rs]
    # print(rf'rs : {rs}')
    # print(rf'type(rs) : {type(rs)}')
    # print(rf'len(rs) : {len(rs)}')
    # if len(rs) != 1:
    #     return {"detail": f"{function_name}() 에서 유효하지 않은 토큰으로 판정되었습니다"}

    rs = JwtUtil.get_jwts(db=MySqlUtil.get_session_local())
    user = get_current_user_as_class(rs, form_data_username)
    DebuggingUtil.print_magenta(rf'user : {user}')
    DebuggingUtil.print_magenta(rf'type(user) : {type(user)}')

    if not user:
        DebuggingUtil.print_ment_fail(rf'''인증실패(DB 에 없는 경우)''')
        return False  # DB 에 없는 경우
    if not verify_pw(pw_plain=form_data_password, pw_hashed=user.pw_hashed):
        DebuggingUtil.print_ment_fail(rf'''인증실패(pw 가 다른 경우)''')
        return False  # pw 가 다른 경우
    DebuggingUtil.print_ment_success(rf'''인증성공''')
    return user  # DB 에 있고 pw 가 같은 경우


@router.post("/jwt")
async def post_jwt(form_data: OAuth2PasswordRequestForm = Depends()):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")

    # 파라미터 제어
    DebuggingUtil.print_magenta(rf'''form_data.username : {form_data.username}''')
    DebuggingUtil.print_magenta(rf'''form_data.password : {form_data.password}''')

    # api 사용자 입력 바인딩
    _jwt = form_data.username

    # _jwt 유효성 디버깅
    DebuggingUtil.print_magenta(rf'''_jwt : {_jwt}''')
    SecurityUtil.decode_jwt_token(_jwt)

    # 유저 인증 로직
    # jwt 인증
    duplication_chk = []
    rs = JwtUtil.get_jwts(db=MySqlUtil.get_session_local())
    DebuggingUtil.print_magenta(rf'rs : {rs}')
    DebuggingUtil.print_magenta(rf'len(rs) : {len(rs)}')

    for row in rs:
        if _jwt == row.token:
            duplication_chk.append(_jwt)

    DebuggingUtil.print_magenta(rf'duplication_chk : {duplication_chk}')
    DebuggingUtil.print_magenta(rf'type(duplication_chk) : {type(duplication_chk)}')
    DebuggingUtil.print_magenta(rf'len(duplication_chk) : {len(duplication_chk)}')

    if len(duplication_chk) != 1:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # detail="Could not validate credentials",
            detail=f"{function_name}() 에서 의도하지 않은 중복 검출 판정이 이루어졌습니다. 다시 시도해 주세요",
            headers={"WWW-Authenticate": "Bearer"},
        )
        DebuggingUtil.print_ment_fail(rf'''인증실패(DB 에 없는 경우)''')
        raise credentials_exception

    # return jwt # success
    return {"access_token": _jwt, "token_type": "bearer"}  # success


@router.post("/register")
async def post_register(data: data_register):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")

    # JWT 생성
    data = {
        # "username": data.username,
        "username": data.name,
        # "pw_hashed": get_pw_hashed(pw_plain=data.pw),
        "pw_hashed": get_pw_hashed(pw_plain=data.email),
    }
    _jwt = SecurityUtil.get_jwt(data=dict(data), secret_key=SECRET_KEY, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    # JWT 중복확인
    rs = JwtUtil.get_jwts_by_token(db=MySqlUtil.get_session_local(), token=_jwt)
    if len(rs) != 0:
        return {"detail": f"{function_name}() 에서 의도하지 않은 중복 검출 판정이 이루어졌습니다. 다시 시도해 주세요"}

    # JWT 저장
    jwt_data = {
        'token': _jwt,
    }
    JwtUtil.insert_jwt_encoded(db=MySqlUtil.get_session_local(), jwt_data=jwt_data)

    # 개발 편의용 코드
    clipboard.copy(_jwt)

    return {"access_token": _jwt, "token_type": "bearer"}


# @router.post("/input-param")
# async def post_input_param(data: data_auth):
#     function_name = inspect.currentframe().f_code.co_name
#     DebuggingUtil.commentize(f"{function_name}()")
#
#     # api 사용자 입력, 바인딩
#     _jwt = data.token
#
#     # _jwt 유효성 디버깅
#     DebuggingUtil.print_magenta(rf'''_jwt : {_jwt}''')
#     SecurityUtil.decode_jwt_token(_jwt)
#
#     # _jwt 중복확인
#     rs = JwtUtil.get_jwts_by_token(db=MySqlUtil.get_session_local(), token=_jwt)
#     for item in rs:
#         _jwt = item.token
#         DebuggingUtil.print_magenta(rf'''item.token : {item.token}''')
#     if len(rs) != 1:
#         return {"detail": f"{function_name}() 에서 유효하지 않은 토큰으로 판정되었습니다"}
#
#     # _jwt 만료 시간 확인
#     payload = jwt.decode(_jwt, SECRET_KEY, algorithms=["HS256"])
#     if "exp" in payload:
#         expiration_time = payload["exp"]
#         DebuggingUtil.print_magenta(rf'''expiration_time : {expiration_time}''')
#         # 만료되었는지 확인
#         # 현재 시간을 UTC로 가져옵니다. KST 랑 비교해보고 아니면 KST 로 가져와야함.
#         import time
#
#         current_time = int(time.time())
#         DebuggingUtil.print_magenta(rf'''current_time : {current_time}''')
#         exp_time = payload["exp"]
#         DebuggingUtil.print_magenta(rf'''exp_time : {exp_time}''')
#         # 만료 시간과 현재 시간을 비교합니다.
#         if current_time > exp_time:
#             return {"detail": f"{function_name}() 에서 토큰 유효기간 만료로 판정되었습니다"}
#         else:
#             DebuggingUtil.print_magenta("토큰이 유효합니다.")
#
#     # 랜덤연산식 영문
#     param = BusinessLogicUtil.get_random_math_expression_english_input_for_code_test()
#
#     # 에러처리
#     # try:
#     #     # ... 데이터 처리 로직 추가 ...
#     #
#     # except JWTException as e:
#     #     logger.error(f"JWT 토큰 검증 실패: {e}")
#     #     raise HTTPException(status_code=401, detail=str(e))
#     #
#     # except RequestValidationError as e:
#     #     logger.error(f"요청 데이터 유효성 오류: {e}")
#     #     raise e
#     #
#     # except Exception as e:
#     #     logger.error(f"예상치 못한 오류 발생: {e}")
#     #     raise HTTPException(status_code=500, detail="Internal server error")
#
#     return {"param": param}


@router.get("/input-param")
async def get_input_param(jwt_: Annotated[str, Depends(oauth2_scheme)]):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")

    # _jwt 유효성 디버깅
    DebuggingUtil.print_magenta(rf'''jwt_ : {jwt_}''')
    SecurityUtil.decode_jwt_token(jwt_)

    # 랜덤연산식 영문
    param = BusinessLogicUtil.get_random_math_expression_english_input_for_code_test()
    return {"param": param}


@router.get("/solution")
async def get_solution(jwt_: Annotated[str, Depends(oauth2_scheme)]):
    # async def get_solution():
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")

    # _jwt 유효성 디버깅
    DebuggingUtil.print_magenta(rf'''jwt_ : {jwt_}''')
    SecurityUtil.decode_jwt_token(jwt_)

    # get_input_param() requests 모듈로 post request.
    # url = "http://127.0.0.1:8080/coding-test/input-param"  # 동일한 엔드포인트로 요청을 보내는 경우
    # headers = {
    #     "accept": "application/json",
    #     "Content-Type": "application/json",
    #     'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InN0cmluZyIsInB3X2hhc2hlZCI6IiQyYiQxMiQ0NGltUU1zVzFwUk9Ma2x6WVIybmYuakVOVlZFSHFVSEZZb2JYckREa1psODQuRlRqM1ZSRyIsImV4cCI6MTcwODQ3OTkxNX0.5QBV3PGmitjVa5Fp4Zxd7fVf3GqHKCwLcNRnLIToosY'
    # }
    # response = requests.get(url, headers=headers)
    # test_token = response.json()
    # [DebuggingUtil.print_magenta(sample) for sample in test_token ]
    # DebuggingUtil.print_magenta(rf'test_token : {test_token}')
    # DebuggingUtil.print_magenta(rf'type(test_token) : {type(test_token)}')
    # DebuggingUtil.print_magenta(rf'len(test_token) : {len(test_token)}')

    # 랜덤연산식 영문
    test_token = BusinessLogicUtil.get_random_math_expression_english_input_for_code_test()
    test_token = BusinessLogicUtil.convert_math_expression_english_to_math_expression_math(test_token)
    solution = await BusinessLogicUtil.get_operation_result_of_parser_for_code_test(test_token)
    DebuggingUtil.print_magenta(rf'''solution : {solution}''')
    return {"solution": solution}


@router.post("/submit")
async def post_submit(file: UploadFile, jwt_: Annotated[str, Depends(oauth2_scheme)]):
# async def post_submit(jwt_: Annotated[str, Depends(oauth2_scheme)], file: UploadFile = File(...)):
    # async def post_submit(file: binary, jwt_: Annotated[str, Depends(oauth2_scheme)]):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")

    # _jwt 유효성 디버깅
    DebuggingUtil.print_magenta(rf'''jwt_ : {jwt_}''')
    SecurityUtil.decode_jwt_token(jwt_)

    # 파일 저장
    directory_coding_test_result = StateManagementUtil.DIRECTORY_CODING_TEST_RESULT
    files_bytes = 0
    files_name = []

    content = await file.read()
    DebuggingUtil.print_magenta(rf'''file.filename : {file.filename}''')
    if file.filename.strip() == "":
        return {"result_msg": "선택된 파일이 없습니다."}

    file_path = rf'{directory_coding_test_result}/{file.filename}'

    FileSystemUtil.make_leaf_file(file_path)
    with open(file_path, "wb") as fp:
        fp.write(content)
    files_bytes += os.path.getsize(file_path)
    files_name.append(file.filename)

    return {
        "result_msg": "파일이 성공적으로 제출되었습니다.",
        "files_name": files_name,
        "files_bytes": files_bytes
    }
