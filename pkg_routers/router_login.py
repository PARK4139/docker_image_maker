import inspect

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from pkg_park4139_for_linux import DebuggingUtil, BusinessLogicUtil, MemberUtil, SecurityUtil

templates = Jinja2Templates(directory=r"pkg_web/templates")

router = APIRouter()
router.mount("/static", StaticFiles(directory="pkg_web/static"), name="static")

prefix_promised = "web"  # /web 는 다른 파일에 작성된 부분이다. 라우터를 다른 파일로 분리했기 때문에 이 부분은 유지보수하며 알아내기가 까다롭다 # 하드코딩
default_redirection_page_without_prefix = '/developer/tests/routing'
# default_redirection_page_without_prefix = '/member/login'
default_redirection_page = f'/{prefix_promised}{default_redirection_page_without_prefix}'


@router.get('/member/login')
def get_member_login(request: Request):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")

    # session 에 id 확인
    if 'id' in request.session and request.session['id'] != '':
        return RedirectResponse('/member')
    else:
        context = {"request": request}
        return templates.TemplateResponse('/member/login.html', context=context)


@router.post('/member/login1')
async def post_member_login1(request: Request):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")


    # 로그인 한 사람은 로그인화면에 진입 할 수 없습니다.

    # 포트폴리오 확인 시 로그인 자동화 설정 일부분
    request.session['main_page_request_cnt'] = "0"

    # html 파일의 form 으로 부터 전송된 데이터 form_data 에 저장
    form_data = await request.form()
    print(rf'form_data["id"] : {form_data["id"]}')
    print(rf'form_data["pw"] : {form_data["pw"]}')

    # sql injection 간단히 확인
    if not SecurityUtil.is_sql_injection_safe_simply(data=form_data["id"]):  # 그럼 아이디에 sql 키워드와 동일한건 못넣는 거네
        return HTMLResponse(content=f'''<script>alert("SQL 인젝션");window.location.href='/{prefix_promised}/member';</script>''')
    if form_data["id"].strip() == "":
        return HTMLResponse(content=f'''<script>alert("아이디가 입력되지 않았습니다");window.location.href='/{prefix_promised}/member';</script>''')
    if form_data["pw"].strip() == "":
        return HTMLResponse(content=f'''<script>alert("패스워드가 입력되지 않았습니다");window.location.href='/{prefix_promised}/member';</script>''')
    if form_data["id"].strip() == "" or form_data["pw"].strip() == "":
        return HTMLResponse(content=f'''<script>alert("패스워드 또는 아이디가 입력되지 않았습니다");window.location.href='/{prefix_promised}/member';</script>''')
    if MemberUtil.is_member_joined(id=form_data['id'], pw=form_data['pw'], request=request):
        # 세션에 세션내 에서 유지할 데이터 저장, 로그인 상태유지를 찾아보니까 보통은 id 나 e-mail 로 한다고 한다, 다음에는 e-mail로 하자.
        request.session['id'] = form_data['id']
        request.session['login_time'] = BusinessLogicUtil.get_time_as_('%Y_%m_%d_%H_%M_%S')
        request.session['name'] = MemberUtil.get_member_name_joined(id=form_data['id'], pw=form_data['pw'], request=request)
        return HTMLResponse(content=f'''<script>alert("로그인 되었습니다");window.location.href='/{prefix_promised}/member';</script>''')
    else:
        return HTMLResponse(content=f'''<script>alert("패스워드 또는 아이디가 틀렸습니다.");window.location.href='/{prefix_promised}/member';</script>''')


@router.post('/logout')
def post_logout(request: Request):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")

    # 세션에서 id 제거
    request.session.pop('id', None)

    # 세션 내 모든 값 삭제
    # request.session.clear()
    return RedirectResponse(f'/{prefix_promised}/member')
