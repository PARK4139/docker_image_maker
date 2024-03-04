import inspect
import traceback
from datetime import datetime

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from pkg_park4139_for_linux import DebuggingUtil, MySqlUtil, BusinessLogicUtil, FastapiUtil, CustomerServiceBoardUtil, CommutationManagementUtil, MemberUtil, TestUtil

templates = Jinja2Templates(directory=r"pkg_web/templates")

router = APIRouter()
router.mount("/static", StaticFiles(directory="pkg_web/static"), name="static")  # 적용되는지 테스트 필요함.

prefix_promised = "web"  # /web 는 다른 파일에 작성된 부분이다. 라우터를 다른 파일로 분리했기 때문에 이 부분은 유지보수하며 알아내기가 까다롭다 # 하드코딩
default_redirection_page_without_prefix = '/member'
redirection_url = f'/{prefix_promised}{default_redirection_page_without_prefix}'




# @router.post('/customer-service-board/{detail_id}', response_class=HTMLResponse) # html 에서 a_tag 로 get 요청을 했을 때, 엔드포인트 내부가 완전히 동일하기 때문에 다음과 같이 처리함.
@router.post('/customer-service-board')
# async def post_customer_service_board(request: Request, p: int = 1): # p 필요한 경우.
async def post_customer_service_board(request: Request):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")
    try:
        # session 기간 내에 로그인 한 경우
        if 'id' in request.session and request.session['id'] != '':
            # jinja_data 업데이트
            FastapiUtil.jinja_data.prefix_promised = prefix_promised
            FastapiUtil.jinja_data.redirection_url = prefix_promised
            server_time = BusinessLogicUtil.get_time_as_('%Y %m %d %H %M %S')
            HH = server_time.split(' ')[3]
            mm = server_time.split(' ')[4]
            ss = server_time.split(' ')[5]
            FastapiUtil.jinja_data.server_time = server_time

            # form_data 에 저장, html 에서 post한 데이터
            form_data = await request.form()
            for field in form_data:
                print(f"Field: {field}, Value: {form_data[field]}")

            # jinja_data 업데이트
            posts = CustomerServiceBoardUtil.get_customer_service_boards(db=MySqlUtil.get_session_local())
            FastapiUtil.jinja_data.posts = posts

            if "detail_id" in form_data:
                rows_data = CustomerServiceBoardUtil.get_customer_service_board(id=int(form_data['detail_id']))
                for row in rows_data:
                    FastapiUtil.jinja_data.detail_id = form_data['detail_id']
                    FastapiUtil.jinja_data.writer = row.writer
                    FastapiUtil.jinja_data.title = row.title
                    FastapiUtil.jinja_data.contents = row.contents
                    FastapiUtil.jinja_data.date_reg = row.date_reg
                    FastapiUtil.jinja_data.del_yn = row.del_yn
                    DebuggingUtil.print_magenta(rf'''row.writer : {row.writer}''')
                    DebuggingUtil.print_magenta(rf'''row.title : {row.title}''')
                    DebuggingUtil.print_magenta(rf'''row.contents : {row.contents}''')
                    DebuggingUtil.print_magenta(rf'''row.date_reg : {row.date_reg}''')
                    DebuggingUtil.print_magenta(rf'''row.del_yn : {row.del_yn}''')

            context = {"request": request, "jinja_data": FastapiUtil.jinja_data}
            return templates.TemplateResponse("/customer_service_board.html", context=context)
            # return templates.TemplateResponse("/excel_merge.html", context=context)
        else:
            # session 기간 내에 로그인 하지 않은 경우
            context = {"request": request, "jinja_data": FastapiUtil.jinja_data}
            # return templates.TemplateResponse("/customer_service_board.html", context=context)
            # return templates.TemplateResponse("/excel_merge.html", context=context)
            return RedirectResponse(redirection_url)
    except:
        DebuggingUtil.print_ment_fail(f"{function_name}(), fail, \n {traceback.format_exc()}")
        # 400 에러 처리를 하고. 400 에러 핸들러에서 redirection 처리를 하는게 어떤가?
        return RedirectResponse(redirection_url)


# @router.get('/customer-service-board/{detail_id}', response_class=HTMLResponse)
# async def get_customer_service_board_detail(request: Request, detail_id: int = 1):
#     function_name = inspect.currentframe().f_code.co_name
#     DebuggingUtil.commentize(f"{function_name}()")
#     try:
#         # session 기간 내에 로그인 한 경우
#         if 'id' in request.session and request.session['id'] != '':
#
#             # jinja_data 업데이트
#             FastapiUtil.jinja_data.prefix_promised = prefix_promised
#             FastapiUtil.jinja_data.redirection_url = prefix_promised
#             server_time = BusinessLogicUtil.get_time_as_('%Y %m %d %H %M %S')
#             HH = server_time.split(' ')[3]
#             mm = server_time.split(' ')[4]
#             ss = server_time.split(' ')[5]
#             FastapiUtil.jinja_data.server_time = server_time
#
#             # form_data 에 저장, html 에서 post한 데이터
#             form_data = await request.form()
#             for field in form_data:
#                 print(f"Field: {field}, Value: {form_data[field]}")
#
#             # jinja_data 업데이트
#             posts = CustomerServiceBoardUtil.get_customer_service_boards(db=MySqlUtil.get_session_local())
#             FastapiUtil.jinja_data.posts =  posts
#
#             if detail_id != None:
#                 rows_data = CustomerServiceBoardUtil.get_customer_service_board(id=int(detail_id))
#                 for row in rows_data:
#                     FastapiUtil.jinja_data.detail_id = detail_id
#                     FastapiUtil.jinja_data.writer = row.writer
#                     FastapiUtil.jinja_data.title = row.title
#                     FastapiUtil.jinja_data.contents = row.contents
#                     FastapiUtil.jinja_data.date_reg = row.date_reg
#                     FastapiUtil.jinja_data.del_yn = row.del_yn
#                     DebuggingUtil.print_magenta(rf'''row.writer : {row.writer}''')
#                     DebuggingUtil.print_magenta(rf'''row.title : {row.title}''')
#                     DebuggingUtil.print_magenta(rf'''row.contents : {row.contents}''')
#                     DebuggingUtil.print_magenta(rf'''row.date_reg : {row.date_reg}''')
#                     DebuggingUtil.print_magenta(rf'''row.del_yn : {row.del_yn}''')
#
#             context = {"request": request, "jinja_data": FastapiUtil.jinja_data}
#             return templates.TemplateResponse("/customer_service_board.html", context=context)
#             # return templates.TemplateResponse("/excel_merge.html", context=context)
#         else:
#             # session 기간 내에 로그인 하지 않은 경우
#             context = {"request": request, "jinja_data": FastapiUtil.jinja_data}
#             # return templates.TemplateResponse("/customer_service_board.html", context=context)
#             # return templates.TemplateResponse("/excel_merge.html", context=context)
#             return RedirectResponse(redirection_url)
#     except:
#         DebuggingUtil.print_ment_fail(f"{function_name}(), fail, \n {traceback.format_exc()}")
#         # 400 에러 처리를 하고. 400 에러 핸들러에서 redirection 처리를 하는게 어떤가?
#         return RedirectResponse(redirection_url)


@router.post('/customer-service-board2')
async def post_customer_service_board2(request: Request):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")
    try:

        # form_data 에 저장, foo.html 에서 post한 데이터
        form_data = await request.form()
        for field in form_data:
            print(f"Field: {field}, Value: {form_data[field]}")
            if form_data[field].strip() == "":
                return HTMLResponse(content=f'''<script>alert("필수항목({BusinessLogicUtil.get_kor_from_eng(field)})은 공백일 수 없습니다");window.history.go(-1);</script>''')


        # session id 가 로그인해도 되는 아이디인지 확인, 2개 아니고 1개 인지도
        customer_service_board_rows = MySqlUtil.get_session_local().query(MemberUtil.Member).filter_by(id=request.session['id']).limit(2).all()
        if len(customer_service_board_rows) == 1:
            # 데이터베이스에 저장
            customer_service_board_row_data = {
                'writer': form_data["writer"],
                'title': form_data["title"],
                'contents': form_data["contents"],
                'date_reg': BusinessLogicUtil.get_time_as_('%Y-%m-%d %H:%M:%S'),
                'del_yn': 'y',
            }
            CustomerServiceBoardUtil.insert_customer_service_board(customer_service_board=customer_service_board_row_data, db=MySqlUtil.get_session_local())

        # 이전페이지로 리다이렉트
        referer = request.headers.get("referer")
        if referer:
            return RedirectResponse(referer)
        else:
            return RedirectResponse(redirection_url)
    except:
        DebuggingUtil.print_ment_fail(f"{function_name}(), fail, \n {traceback.format_exc()}")
        # 400 에러 처리를 하고. 400 에러 핸들러에서 redirection 처리를 하는게 어떤가?
        return RedirectResponse(redirection_url)
