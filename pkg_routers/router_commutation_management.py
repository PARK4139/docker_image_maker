import inspect

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pkg_park4139_for_linux import DebuggingUtil, MySqlUtil, BusinessLogicUtil, FastapiUtil, MemberUtil, CommutationManagementUtil

templates = Jinja2Templates(directory=r"pkg_web/templates")

router = APIRouter()
router.mount("/static", StaticFiles(directory="pkg_web/static"), name="static") # 적용되는지 테스트 필요함.

prefix_promised = "web"  # /web 는 다른 파일에 작성된 부분이다. 라우터를 다른 파일로 분리했기 때문에 이 부분은 유지보수하며 알아내기가 까다롭다 # 하드코딩
default_redirection_page_without_prefix = '/developer/tests/routing'
# default_redirection_page_without_prefix = '/member/login'
default_redirection_page = f'/{prefix_promised}{default_redirection_page_without_prefix}'

@router.post('/go-to-office')
def post_go_to_office(request: Request):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")

    # 오늘날짜로 출근한적 있는지 조회
    # 금일 출근처리한 사람은 출근처리할 수 없습니다.


    # 변수에 저장
    server_time = BusinessLogicUtil.get_time_as_('%Y %m %d %H %M %S')
    HH = server_time.split(' ')[3]
    mm = server_time.split(' ')[4]
    ss = server_time.split(' ')[5]
    name = request.session['id']

    # members = MySqlUtil.get_session_local().query(MemberUtil.Member).filter_by(id=request.session['id'], name=request.session['name']).limit(10).all() # success
    members = MySqlUtil.get_session_local().query(MemberUtil.Member).filter_by(id=request.session['id']).limit(10).all()
    print(len(members))
    if len(members) == 1:
        for member in members:

            # 객체에 바인딩
            member_data = {
                'id': request.session['id'],
                'name': name,
                'phone_no': member.phone_no,
                'time_to_go_to_office': '-',
                'time_to_leave_office': server_time
            }

            # 데이터베이스에 저장
            CommutationManagementUtil.insert_commutation_management(commutation_management=member_data, db=MySqlUtil.get_session_local())
    return HTMLResponse(content=f'''<script>alert("{name} 님 {HH}시 {mm}분 {ss}초 출근처리 되었습니다");window.location.href='member';</script>''')


@router.post('/leave-office')
def post_leave_office(request: Request):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")

    # 오늘날짜로 출근한적 있는지 조회
    # 금일 출근처리하지 않은 사람은 퇴근처리할 수 없습니다.


    # 변수에 저장
    server_time = BusinessLogicUtil.get_time_as_('%Y %m %d %H %M %S')
    HH = server_time.split(' ')[3]
    mm = server_time.split(' ')[4]
    ss = server_time.split(' ')[5]
    name = request.session['id']
    # members = MySqlUtil.get_session_local().query(MemberUtil.Member).filter_by(id=request.session['id'], name=request.session['name']).limit(4).all()
    members = MySqlUtil.get_session_local().query(MemberUtil.Member).filter_by(id=request.session['id']).limit(4).all()
    print(len(members))
    if (len(members) == 1):
        for member in members:

            # 객체에 바인딩
            member_data = {
                'id': request.session['id'],
                'name': name,
                'phone_no': member.phone_no,
                'time_to_go_to_office': '-',
                'time_to_leave_office': server_time
            }

            # 데이터베이스에 저장
            CommutationManagementUtil.insert_commutation_management(commutation_management=member_data, db=MySqlUtil.get_session_local())

    return HTMLResponse(content=f'''<script>alert("{name} 님 {HH}시 {mm}분 {ss}초 퇴근처리 되었습니다");window.location.href='member';</script>''')
