import inspect

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pkg_park4139_for_linux import DebuggingUtil, MySqlUtil, BusinessLogicUtil, FastapiUtil, MemberUtil

templates = Jinja2Templates(directory=r"pkg_web/templates")

router = APIRouter()
router.mount("/static", StaticFiles(directory="pkg_web/static"), name="static")

prefix_promised = "web"  # /web 는 다른 파일에 작성된 부분이다. 라우터를 다른 파일로 분리했기 때문에 이 부분은 유지보수하며 알아내기가 까다롭다 # 하드코딩
default_redirection_page_without_prefix = '/developer/tests/routing'
# default_redirection_page_without_prefix = '/member/login'
default_redirection_page = f'/{prefix_promised}{default_redirection_page_without_prefix}'


@router.get('/member/join')
def get_member_join(request: Request):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")
    context = {"request": request, "jinja_data": FastapiUtil.jinja_data}
    return templates.TemplateResponse("member/join.html", context=context)


@router.post('/member/join1')
def post_member_join1(request: Request):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")

    # 가입 양식 더미 데이터 바인딩 자동화
    FastapiUtil.jinja_data.prefix_promised = prefix_promised
    # FastapiUtil.jinja_data.random_str = SecurityUtil.get_random_id(length_limit=30)
    # FastapiUtil.jinja_data.name = SecurityUtil.get_random_name()
    # FastapiUtil.jinja_data.id = SecurityUtil.get_random_id(20)
    # FastapiUtil.jinja_data.pw = 1
    # FastapiUtil.jinja_data.pw2 = SecurityUtil.get_random_pw(30)
    # FastapiUtil.jinja_data.birthday = SecurityUtil.get_random_date()  # 이건 드롭다운 버튼으로 선택하도록
    # FastapiUtil.jinja_data.phone_no = SecurityUtil.get_random_phone_number()
    # FastapiUtil.jinja_data.address = SecurityUtil.get_random_address()
    # FastapiUtil.jinja_data.e_mail = SecurityUtil.get_random_e_mail()
    # FastapiUtil.jinja_data.age = SecurityUtil.get_random_user_trial_input_case()
    # FastapiUtil.jinja_data.date_joined = SecurityUtil.get_random_user_trial_input_case()
    # FastapiUtil.jinja_data.date_canceled = SecurityUtil.get_random_user_trial_input_case()
    # FastapiUtil.jinja_data.fax_no = SecurityUtil.get_random_user_trial_input_case()
    # FastapiUtil.jinja_data.business_registration_no = SecurityUtil.get_random_user_trial_input_case()
    # FastapiUtil.jinja_data.company_name = SecurityUtil.get_random_user_trial_input_case()
    # FastapiUtil.jinja_data.department = SecurityUtil.get_random_user_trial_input_case()
    # FastapiUtil.jinja_data.position = SecurityUtil.get_random_user_trial_input_case()
    # FastapiUtil.jinja_data.company_address = SecurityUtil.get_random_user_trial_input_case()
    context = {"request": request, "jinja_data": FastapiUtil.jinja_data}
    return templates.TemplateResponse("member/join.html", context=context)


@router.post('/member/join2')  # response_class=HTMLResponse 앞으로는 작성하지 말자 return 쪽에 HTMLResponse 적는게 가독성이 좋다고 생각한다.
async def post_member_join2(request: Request):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")

    # 의도된대로 JoinForm 를 파라미터 타입힌팅을 하여 fastapi 유효성검사 success
    # 그러나 에러 핸들러에서 유효성검사 결과 처리를 해야함.
    # 그냥 이 엔드포인트 내에서 유효성검사 결과 처리하는 것이 유지보수에 좋을 것 같은데..
    # 유지보수를 위해 이 엔드포인트 내에서 유효성검사 결과 처리하도록 JoinForm 파라미터 타입힌팅을 삭제 하엿다
    # 덧붙여 fastapi 의 유효성검사는 함수가 호출되기 전에 이뤄지는 것으로 생각된다.
    # 함수 내부의 코드는, 유효성 검사를 통과한 다음 수행되는 코드이다.

    # form_data 에 html form post 요청 내용 저장
    form_data = await request.form()
    for field in form_data:
        print(f"Field: {field} : {form_data[field]}")

    # 객체에 바인딩
    member_data = {
        # 순서 중요.
        'name': form_data['name'],
        'id': form_data['id'],
        'phone_no': form_data['phone_no'],
        'e_mail': form_data['e_mail'],
        'pw': form_data['pw'],
        'address': form_data['address'],
        'birthday': form_data['birthday'],
        'date_joined': BusinessLogicUtil.get_time_as_('%Y_%m_%d_%H_%M_%S'),
    }

    # 데이터 공통전처리
    # member_data 딕셔너리를 돌면서 모든 value 에 .strip() 처리를 하는 코드
    for key, value in member_data.items():
        member_data[key] = value.strip()


    # 필수요소를 공백으로 한경우
    neccessary_data_blank = ""
    for key, value in member_data.items():
        if value == '':
            print(rf'''key : {key},  value : {value}''')
            neccessary_data_blank = key
            break
    print(rf'''neccessary_data_blank : {neccessary_data_blank}''')
    neccessary_data_blank = BusinessLogicUtil.get_kor_from_eng(english_word=neccessary_data_blank)  # f-string을 이용을 하더라도 함수는 넣지말자, 동작하지 않을 수 있다.
    DebuggingUtil.print_magenta(rf'''neccessary_data_blank : {neccessary_data_blank}''')
    if not neccessary_data_blank == "":
        return HTMLResponse(content=f'''
        <script>
            alert("{neccessary_data_blank}는 필수요소입니다.\\n공백으로 회원가입을 할 수 없습니다.");
            window.location.href='/{prefix_promised}/member/join'
        </script>
        ''')

    # 비밀번호와 비밀번호 확인
    if member_data['pw'] != form_data['pw2']:
        return HTMLResponse(content=f'''
        <script>
            alert("비밀번호가 일치하지 않습니다.\\n비밀번호를 일치하게 입력해주세요.");
            window.location.href='/{prefix_promised}/member/join'
        </script>
        ''')

    # 가입된 아이디인지 확인
    if MemberUtil.is_member_joined_by_id(id=member_data['id'], request=request):
        return HTMLResponse(content=f'''
       <script>
           alert("이미가입된 아이디입니다.\\n다른 아이디로 회원가입을 시도해주세요.");
           window.location.href='/{prefix_promised}/member/join'
       </script>
       ''')

    # member_data 벨리데이션
    MemberUtil.validate_member(member_data)

    # 회원가입
    MemberUtil.insert_member(member=member_data, db=MySqlUtil.get_session_local())

    return HTMLResponse(content=f'''
    <script>
        alert("회원가입 되었습니다");
        window.location.href='/{prefix_promised}/member' 
    </script>
    ''')
