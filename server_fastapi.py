# from app.routes import index, auth
import inspect
import os
from contextlib import asynccontextmanager

import clipboard
import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from pydantic import BaseModel
from starlette.middleware.exceptions import ExceptionMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from pkg_park4139_for_linux import FastapiUtil, MySqlUtil, DebuggingUtil, FileSystemUtil, StateManagementUtil, UvicornUtil, SecurityUtil, BusinessLogicUtil, MemberUtil
from pkg_routers import router_coding_test_management, router_main, router_nav_items, router_book, router_user, router_developer_special, router_cloud, router_excel_merge, router_customer_service, router_commutation_management, router_login, router_join, router_test_try_1

templates = Jinja2Templates(directory=r"pkg_web/templates")

# 개발/운영 모드
StateManagementUtil.is_op_mode = False  # False 이면 dev 모드, 주석하면 op 모드


# 설정데이터를 설정파일에 저장
# FastAPI에서는 환경변수 설정 BaseSettings를 활용, built in pydantic
# config.env, 에 설정 저장 config.env도 파일인데 보안에 안전한가?
# 설정 파일의 내용은 Settings 클래스의 필드에 맞게 작성되어야 합니다.
# class Settings(BaseSettings):
#     database_uri: str
#     sqlalchemy_echo: bool = True
#     sqlalchemy_track_modifications: bool = True
#     secret_key: str  # SESSION? 웹 세션?, DB 세션? 을 위한 시크릿 키?,  random bytes 시크릿 키 비밀번호로 app.secret_key 변수에 저장, 잘 보관해라 이 비밀번호를, 함부로 배포해서는 않되니 방법을 모색할것.
#     config_file: str
#
#     class Config:
#         env_file = ".env"  # 환경 변수 파일명 설정
#
# settings = Settings(
#     _env_file="config.env",  # 환경 변수 파일 경로 설정
#     _env_file_encoding="utf-8"  # 환경 변수 파일 인코딩 설정
# )
# Settings 클래스에 secret_key 필드만 포함되어 있습니다.
# secret_key는 .env 파일이나 환경 변수를 통해 설정할 수 있도록 되어 있습니다.
# config.env 파일을 생성하고, secret_key 값을 해당 파일에 작성해야 합니다.
# 설정데이터를 환경변수에 저장
# ?


# 영한 버전 설정
# en.yaml/ko.yaml


@asynccontextmanager
async def lifespan(app: FastAPI):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")
    # 앱 시작 후 1번만 실행(app 객체 생성 뒤) , @app.on_event("startup") deprecated, @app.on_event("startup") 대체품

    # 모드설정
    if StateManagementUtil.is_op_mode:
        mode = "op"
        DebuggingUtil.print_magenta(f"INFO:{StateManagementUtil.INDENTATION_PROMISED}{os.path.basename(__file__)}를 {mode}모드 로 구동 중입니다")
    else:
        mode = "dev"
        DebuggingUtil.print_ment_red(f"INFO:{StateManagementUtil.INDENTATION_PROMISED}{os.path.basename(__file__)}를 {mode}모드 로 구동 중입니다")

    # 데이터베이스
    # SQLALCHEMY_TRACK_MODIFICATIONS
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLAlchemy가 데이터베이스의 변경 사항을 추적하는 기능을 활성화 또는 비활성화
    # 대규모 애플리케이션에서는 권장되지 않습니다. SQLALCHEMY_TRACK_MODIFICATIONS = False 로 두는 것이 좋다
    try:
        if not StateManagementUtil.is_op_mode:
            MySqlUtil.Base.metadata.drop_all(bind=MySqlUtil.engine)  # 개발 중에 drop 필요한 경우가 있음
            DebuggingUtil.print_magenta(rf'''INFO:{StateManagementUtil.INDENTATION_PROMISED}데이터베이스 드롭 성공''')
        MySqlUtil.Base.metadata.create_all(bind=MySqlUtil.engine)  # 데이터베이스에, Base 클래스에 정의된 모든 테이블을 생성, 옵션코드, class Item(Base): 다음에 호출되어야 동작한다
        DebuggingUtil.print_magenta(rf'''INFO:{StateManagementUtil.INDENTATION_PROMISED}데이터베이스 테이블 생성 성공''')
        if not StateManagementUtil.is_op_mode:
            # 테스트 계정 생성 자동화
            member_data = {
                'id': "`",
                'pw': "`",
                'name': "아이유",
                'phone_no': "",
                'address': "",
                'e_mail': "",
                'birthday': "",
                'date_joined': BusinessLogicUtil.get_time_as_('%Y_%m_%d_%H_%M_%S'),
                'date_canceled': ''
            }
            MemberUtil.insert_member(member=member_data, db=MySqlUtil.get_session_local())
            DebuggingUtil.print_magenta(rf'''INFO:{StateManagementUtil.INDENTATION_PROMISED}데이터베이스 테스트 계정 자동생성 성공''')
    except:
        DebuggingUtil.print_ment_fail(rf'''INFO:{StateManagementUtil.INDENTATION_PROMISED}예약된 데이터베이스 작업을 수행할 수 없었습니다.''')

    # 서버 인사
    if not StateManagementUtil.is_op_mode:
        DebuggingUtil.print_magenta(rf'INFO:{StateManagementUtil.INDENTATION_PROMISED}MySqlUtil.Settings.uri   : {MySqlUtil.Settings.uri}')
        DebuggingUtil.print_magenta(rf'INFO:{StateManagementUtil.INDENTATION_PROMISED}UvicornUtil.Settings.url : {UvicornUtil.Settings.url}')
        DebuggingUtil.print_magenta(rf"INFO:{StateManagementUtil.INDENTATION_PROMISED}✧*｡٩(ˊᗜˋ*)و✧*｡")

    # swagger 실행 자동화
    # FileSystemUtil.explorer(fr"{UvicornUtil.Settings.protocol_type}://{UvicornUtil.Settings.host}:{UvicornUtil.Settings.port}/docs")
    # FileSystemUtil.explorer(fr"{UvicornUtil.Settings.protocol_type}://{UvicornUtil.Settings.host}:{UvicornUtil.Settings.port}/redoc")
    # FileSystemUtil.explorer(fr"{UvicornUtil.Settings.protocol_type}://{UvicornUtil.Settings.host}:{UvicornUtil.Settings.port}")

    # 더미 데이터 객체 생성 자동화
    # FileSystemUtil.explorer(fr"{UvicornUtil.Settings.protocol_type}://{UvicornUtil.Settings.host}:{UvicornUtil.Settings.port}/make-dummyies")
    # FastapiUtil.test_client_post_request() # swagger 로 해도 되지만, test 자동화 용도

    # 클라이언트 테스트 자동화
    # FastapiUtil.test_client_post_request()  # swagger 로 해도 되지만, test 자동화 용도로 고민 중

    # 콘솔 타이틀 변경 테스트
    # lines = subprocess.check_output(rf'start cmd /k title NETWORK TEST CONSOLE', shell=True).decode('utf-8').split("\n")

    # 클라이언트 테스트 자동화
    # lines = subprocess.check_output(rf'start cmd /k title CLIENT TEST CONSOLE ', shell=True).decode('utf-8').split("\n")
    # for i in range(0,10,+1):
    #     os.system(rf'explorer "{url_base}/api/via-db/items/{i}"')

    # 머신러닝 모델 더미 생성
    # def fake_answer_to_everything_ml_model(x: float):
    #     return x * 42
    #
    # # Load the ML model
    # ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model

    yield  # 이게 lifespan의 동작트리거 기준이된다!! 이거 전후로 startup/shutdown 동작한다.

    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")
    print(f"INFO:{StateManagementUtil.INDENTATION_PROMISED}애플리케이션 종료를 진행합니다")

    # 백업도 작성대기

    # # Clean up the ML models and release the resources
    # ml_models.clear()


app = FastAPI(lifespan=lifespan, swagger_ui_parameters={"tryItOutEnabled": True})
# app.config.from_object(config) # config.py 를 사용해서 SETTING
# app.config.from_envvar('APP_CONFIG_FILE')  # 환경변수 APP_CONFIG_FILE 에 저장된 파일주소 가져와서 설정

# handler = Mangum(app)  #  AWS serverless platform 쓸 때 써야한다던 것 같다. function 단위로 쪼개는 역활
# app.mount("/pkg_web", StaticFiles(directory="pkg_web"), name="pkg_web")
app.mount("/static", StaticFiles(directory="pkg_web/static"), name="static")  # html 에서 /static 오로 찾게되는 것 같음.
app.mount("/pkg_cloud", StaticFiles(directory="pkg_cloud"), name="pkg_cloud")

# app.encoding = 'utf-8'
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.INFO)


# 미들웨어
# UvicornUtil.init_ip_address_allowed(app) # nginx 가 앞단이므로 nginx 에서 설정하는 것이 효율적일듯
# UvicornUtil.init_domain_address_allowed(app) # nginx 가 앞단이므로 nginx 에서 설정하는 것이 효율적일듯
if not StateManagementUtil.is_op_mode:
    FastapiUtil.init_cors_policy(app)  # nginx 가 앞단이므로 nginx 에서 설정하는 되어 있으므로 dev 에서 테스트 시에만 필요


# fastapi 기본 예외처리 핸들러
# FastAPI는 기본적으로 예외 처리를 자동으로 처리하고 오류 응답을 생성합니다. 하지만 커스텀 핸들러를 추가하여, 예외를 직접 처리할 수 있음
@app.exception_handler(RequestValidationError)
async def reqeust_validation_exception_handler(request: Request, exc):  # exc : Exception
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")
    DebuggingUtil.print_magenta(rf'''request.url : {request.url}''')
    # 이거 고민되는데 api 라면 json 으로 respon 하는게 좋겠고, 웹이라면 http 로 respon 하는게 맞을 것 같은데 이를 알아낼 수 있으면 좋겠다. 우선은 json 으로 respon 하자
    if "/web" in request.url:
        # return HTMLResponse(content=f'''<script>alert("{ment_error}");window.history.go(-1);</script>''')
        return HTMLResponse(content=f'''<script>alert("{exc.detail}");window.history.go(-1);</script>''')
    else:
        # json 으로 처리
        context = {
            "request": request,
            "exc_errors": exc.errors(),
            "exc_body": exc.body,
            "exe_detail": exc.detail,
        }
        return JSONResponse(content=context)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc):  # exc : Exception
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")
    DebuggingUtil.print_magenta(rf'''request.url : {request.url}''')
    # 이거 고민되는데 api 라면 json 으로 respon 하는게 좋겠고, 웹이라면 http 로 respon 하는게 맞을 것 같은데 이를 알아낼 수 있으면 좋겠다. 우선은 json 으로 respon 하자
    if "/web" in str(request.url):
        # html 파일로 처리
        # context = {
        #     "request": request,
        #     "msg": msg,
        #     'status_code': status_code,
        #     "exc_errors": exc.errors(),
        #     "exc_body": exc.body,
        #     "window_location_href": default_redirection_page,
        # }
        # return templates.TemplateResponse("/errors/main.html", context=context, status_code=status_code)

        # js alert 로 처리
        # window.history.go(-1);// 전 페이지로 이동
        # //window.history.go(-2);// 전전 페이지로 이동
        # //window.history.go(1);// 다음 페이지로 이동
        # //window.history.go(2);// 다다음 페이지로 이동
        # return HTMLResponse(content=f'''<script>alert("exec.detail : {exc.detail}");window.history.go(-1);</script>''')
        return HTMLResponse(content=f'''<script>alert("{exc.detail}");window.history.go(-1);</script>''')
    else:
        # json 으로 처리
        context = {
            "request": request,
            "exc_errors": exc.errors(),
            "exc_body": exc.body,
            "exe_detail": exc.detail,
        }
        return JSONResponse(content=context)



app.add_middleware(ExceptionMiddleware)
# 커스텀 예외처리 핸들러, Exception 추가 작업 처리를 기대
# async def custom_exception_handler(request: Request, exc: Any) -> JSONResponse:
#     # custom exception handling logic
#     return JSONResponse(
#         status_code=500,
#         content={"message": "Custom exception handler 작동"}
#     )
# exception_handlers: Dict[Type[Exception], Coroutine[Any, Any, JSONResponse]] = {
#     Exception: custom_exception_handler
# }
# app.exception_handlers = exception_handlers


app.add_middleware(
    SessionMiddleware,
    secret_key=SecurityUtil.get_random_bytes(),  # 난수생성기로 세션시크릿 생성 # 세션이 동적으로 생성이 되게 하려고 했는데 그러면, 서버 재시작시 세션데이터가 손실, 동일서버를 다중서버로 운영 시 시크릿 키가 서로 다르면 문제가 됨. 고로 같아야함.
    max_age=3600,  # 세션 수명 3600 초(1시간)
)


@app.middleware("http")
async def preprocess_after_request(request, call_next):
    # 매 라우팅 전에 동작하는 함수 # 일종의 aop 같이 처리? # request 감지하고 트리거로서 가로채기를 하는 느낌이다
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")

    await FastapiUtil.preprocess_after_request(request)
    response = await call_next(request)
    return response


@app.middleware("http")
async def preprocess_before_response_return(request, call_next):
    # 매 라우팅 후에 동작하는 함수
    # function_name = inspect.currentframe().f_code.co_name
    # DebuggingUtil.commentize(f"{function_name}()")
    response = await call_next(request)
    await FastapiUtil.preprocess_before_response_return(request, response)
    return response


# 라우팅 동작 설계 (잠정)
# https://park4139.store/api/
# https://park4139.store/web/
# https://pjh4139.store/p=


# 파비콘 라우팅 처리
# @app.get('/favicon.ico', include_in_schema=False)
# async def get_favicon():
#     #     # function_name = inspect.currentframe().f_code.co_name
#     #        DebuggingUtil.commentize(f"{function_name}()")
#     #     # return PlainTextResponse('')
#     #     # return Response(content=b'', media_type='image/x-icon')
#     #     # raise HTTPException(status_code=404)
#     #     # raise HTTPException(status_code=500)
#     pass  # favicon 요청에 대한 콘솔에 출력.


# 라우터 설정
@app.get("/", tags=["API 테스트"])  # tags 파라미터는 FastAPI 자동문서화에 사용되는 데이터, 엔드포인트를 그룹화하는 데 사용되는 기능, # tags 를 동일하게 입력하면 하나의 api 그룹으로 묶을 수 있다
async def check_api_health(request: Request):
    DebuggingUtil.print_magenta(f"{inspect.currentframe().f_code.co_name}()")

    if StateManagementUtil.is_op_mode:
        return {"success": f"fastapi 서버로서 {os.path.basename(__file__)}를 구동 중 입니다"}
    else:
        # 의도적 웹페이지로 리다이렉팅, 테스트용
        return RedirectResponse(url="/web/member")
@app.get("/filter/urls", tags=["API 테스트"])
async def collect_urls(request: Request):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")
    urls = []
    for index, route in enumerate(app.routes):
        if hasattr(route, "path"):
            # href = f"{request.base_url}{prefix_promised}{route.path}"
            href = f"{str(request.base_url)[0:-1]}{route.path}"
            urls.append(href)
    return {"urls": urls}


@app.get("/pw_hashed/{pw_plain}", tags=["API 테스트"])
async def get_pw_hashed(pw_plain: str):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")

    from passlib.context import CryptContext
    pw_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    pw_hashed = pw_context.hash(pw_plain)

    # 테스트용 코드
    clipboard.copy(pw_hashed)
    return {"pw_hashed": pw_hashed}

app.include_router(router_user.router, prefix="/api", tags=["USER API (DB JSON)"])
app.include_router(router_book.router, prefix="/api", tags=["BOOK API (DB JSON)"])
app.include_router(router_nav_items.router, prefix="/api", tags=["nav-items API (DB JSON)"])
app.include_router(router_main.router, prefix="/web", tags=["회원관리 메인 웹 (MySql)"])
app.include_router(router_join.router, prefix="/web", tags=["회원관리 가입 웹 (MySql)"])
app.include_router(router_login.router, prefix="/web", tags=["회원관리 로그인 웹 (MySql)"])
app.include_router(router_commutation_management.router, prefix="/web", tags=["근태관리 웹 (MySql)"])
app.include_router(router_customer_service.router, prefix="/web", tags=["CS 관리 웹 (MySql)"])
app.include_router(router_excel_merge.router, prefix="/web", tags=["엑셀파일 병합 웹 (Server Local Directory)"])
app.include_router(router_cloud.router, prefix="/web", tags=["파일공유 웹 (Server Local Directory)"])  # 백업
app.include_router(router_developer_special.router, prefix="/web", tags=["개발자 웹 (Not Defined)"])
app.include_router(router_coding_test_management.router, prefix="/coding-test", tags=["코딩 테스트 관리 API (MySql)"])
app.include_router(router_test_try_1.router, prefix="/test", tags=["x test try 1"])
# app.include_router(router_test_try_2.router, prefix="/test", tags=["x test try 2"])
# app.include_router(router_test_try_3.router, prefix="/test", tags=["x test try 3"])
# app.include_router(router_developer_special.router, prefix="/web", tags=["백오피스 웹"])
# app.include_router(router_item.router, prefix="/api", tags=["상품관리 API"])
# app.include_router(router_todo.router, prefix="/api", tags=["할일관리 API(mysql.test_db.todos 에 저장), 미완성"])
# app.include_router(router_member.router, prefix="/api", tags=["회원관리 API(maria.test_db.members 에 저장), 미완성"])
# app.include_router(router_user.router, prefix="/api", tags=["회원관리 API(mysql.test_db.users 에 저장), 미완성"])
# app.include_router(router_test.router, prefix="/test", tags=["JWT/OAuth2 test4 (MySql)"])

# "if name == "main":" 코드는
# 이 파일이 직접 실행되는 경우만 이 코드 블록은 실행됩니다.
# 이 파일을 import하여 사용할 때는 해당 코드 블록이 실행되지 않습니다.
# 이 파일을 uvicorn으로 실행하면 해당 코드 블록이 실행되지 않습니다. 이는 # dev 에서만 동작되는 것으로 사용할 수 있습니다.
if __name__ == "__main__":
    uvicorn.run(app=f"{FileSystemUtil.get_target_as_n(__file__)}:app", host=UvicornUtil.Settings.host, port=UvicornUtil.Settings.port)
