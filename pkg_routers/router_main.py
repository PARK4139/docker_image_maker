import inspect

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pkg_park4139_for_linux import DebuggingUtil, FastapiUtil, StateManagementUtil

templates = Jinja2Templates(directory=r"pkg_web/templates")

router = APIRouter()
router.mount("/static", StaticFiles(directory="pkg_web/static"), name="static")

prefix_promised = "web"  # /web 는 다른 파일에 작성된 부분이다. 라우터를 다른 파일로 분리했기 때문에 이 부분은 유지보수하며 알아내기가 까다롭다 # 하드코딩
# default_redirection_page_without_prefix = '/developer/tests/routing'
default_redirection_page_without_prefix = '/member'
default_redirection_page = f'/{prefix_promised}{default_redirection_page_without_prefix}'


# security = HTTPBasic()


@router.get("/member")
async def route_get_member(request: Request):
    # async def route_get_member(request: Request, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")

    # 파라미터 제어
    # DebuggingUtil.print_magenta(rf'''credentials.username : {credentials.username}''')
    # DebuggingUtil.print_magenta(rf'''credentials.password : {credentials.password}''')

    FastapiUtil.jinja_data.prefix_promised = prefix_promised

    # 로그인 자동화, 개발 모드에서만 동작
    if not StateManagementUtil.is_op_mode:
        request.session['id'] = '`'  # 서버시작 시, 테스트 계정 아이디 1로 생성 자동화 그래서 id 는 1 로 둠

    # 포트폴리오용 코드
    request.session['id'] = '`'  # 서버시작 시, 테스트 계정 아이디 1로 생성 자동화 그래서 id 는 1 로 둠
    if not 'login_cnt' in request.session:
        request.session['login_cnt'] = "0"
    request.session['login_cnt'] = f"{int(request.session['login_cnt'])+1}"


    if 'id' in request.session and request.session['id'] != '':
        # session 기간 내에 로그인 한 경우
        from fastapi import Response

        context = {"request": request, "jinja_data": FastapiUtil.jinja_data}
        return templates.TemplateResponse("/member/main.html", context=context)
    else:
        # session 기간 내에 로그인 하지 않은 경우
        context = {"request": request, "jinja_data": FastapiUtil.jinja_data}
        return templates.TemplateResponse("/member/login.html", context=context)


@router.post("/member")
async def route_post_member(request: Request):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")

    FastapiUtil.jinja_data.prefix_promised = prefix_promised

    # foo.html 에서 전송된 form 데이터를 변수에 저장 
    form_data = await request.form()
    for field in form_data:
        print(f"Field: {field}, Value: {form_data[field]}")

    if 'id' in request.session and request.session['id'] != '':
        # session 기간 내에 로그인 한 경우
        context = {"request": request, "jinja_data": FastapiUtil.jinja_data}
        return templates.TemplateResponse("/member/main.html", context=context)
    else:
        # session 기간 내에 로그인 하지 않은 경우
        context = {"request": request, "jinja_data": FastapiUtil.jinja_data}
        return templates.TemplateResponse("/member/login.html", context=context)
