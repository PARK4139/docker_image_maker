import inspect
import os
import shutil
import uuid
from tempfile import NamedTemporaryFile
from typing import List, IO, Union

from fastapi import APIRouter
from fastapi import File, UploadFile
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse, FileResponse, StreamingResponse, Response, HTMLResponse

from pkg_park4139_for_linux import DebuggingUtil, FastapiUtil, BusinessLogicUtil, StateManagementUtil, TestUtil, FileSystemUtil, UvicornUtil
templates = Jinja2Templates(directory=r"pkg_web/templates")

router = APIRouter()

prefix_promised = "web"  # /web 는 다른 파일에 작성된 부분이다. 라우터를 다른 파일로 분리했기 때문에 이 부분은 유지보수하며 알아내기가 까다롭다 # 하드코딩
default_redirection_page_without_prefix = '/developer-special'
default_redirection_page = f'/{prefix_promised}{default_redirection_page_without_prefix}'


@router.get("/developer-special")
async def get_developer_special(request: Request):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")
    FastapiUtil.jinja_data.prefix_promised = prefix_promised

    # 등록된 주소 출력
    # for route in router.routes:
    #     print(route.path)

    if 'id' in request.session and request.session['id'] != '':
        # 로그인 한 경우
        context = {"request": request, "jinja_data": FastapiUtil.jinja_data}
        return templates.TemplateResponse("/developer_special.html", context=context)
    else:
        # 로그인 하지 않은 경우
        context = {"request": request, "jinja_data": FastapiUtil.jinja_data}
        return RedirectResponse('/member')


@router.post("/developer-special")
async def post_developer_special(request: Request):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")
    FastapiUtil.jinja_data.prefix_promised = prefix_promised

    if 'id' in request.session and request.session['id'] != '':

        # 디렉토리를 재생성. 주의, 하위파일은 모두 삭제됨, 복구불가
        DIR_PATH = StateManagementUtil.DIRECTORY_XLS_TO_MERGE
        FileSystemUtil.truncate_tree(DIR_PATH)

        # 디렉토리를 재생성. 주의, 하위파일은 모두 삭제됨, 복구불가
        DIR_PATH = StateManagementUtil.DIRECTORY_XLS_MERGED
        FileSystemUtil.truncate_tree(DIR_PATH)

        # 로그인 한 경우
        context = {"request": request, "jinja_data": FastapiUtil.jinja_data}
        return templates.TemplateResponse("/developer_special.html", context=context)
    else:
        # 로그인 하지 않은 경우
        return RedirectResponse('/member')


@router.post("/developer-special/upload-files")
async def post_upload_files(files: List[UploadFile]):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")

    # pkg_special 비우기
    # FileSystemUtil.truncate_tree(StateManagementUtil.DIRECTORY_CLOUD)

    # 클라이언트에서 보낸파일들 서버의 지정된 디렉토리에 저장
    UPLOAD_DIR = StateManagementUtil.DIRECTORY_PKG_CLOUD
    for file in files:
        content = await file.read()
        # filename = f"{str(uuid.uuid4())}.jpg"  # uuid로 유니크한 파일명으로 변경
        DebuggingUtil.print_magenta(rf'''file.filename : {file.filename}''')
        if file.filename.strip()=="":
            return HTMLResponse(content=f'''<script>alert("선택된 파일이 없습니다");window.location.href='developer-special';</script>''')
        with open(os.path.join(UPLOAD_DIR, file.filename), "wb") as fp:
            fp.write(content)

    # return {"filenames": [file.filename for file in files]}
    # file 이라는 이름으로 해당 파일 객체를 받으므로,
    # 클라이언트단(html)에서는 file/files이라는 키값(아마도 name 태그를 의미하는 듯) 설정하지 않으면 422 Unprocessable Entity 에러

    return RedirectResponse('developer-special')




# 사진 다운로드
# @app.get("/downloadFiles/")
# async def download_photo(photo_id: int, db: Session = Depends(get_db)):
# function_name = inspect.currentframe().f_code.co_name
# DebuggingUtil.commentize(f"{function_name}()")
#     find_photo: Photo = db.query(Photo).filter_by(photo_id=photo_id).first()
#     return FileResponse(find_photo.src)


# 파일 전송 샘플
# @router.get("/developer_special/")
# def download_developer_special():
#     file_name_downloaded = FileSystemUtil.get_target_as_nx(StateManagementUtil.MERGED_EXCEL_FILE)
#     return FileResponse(StateManagementUtil.MERGED_EXCEL_FILE, filename=file_name_downloaded)




# 파일 확장자 유효성 확인 기능
def check_allowed_file_or_not(filename, request: Request):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")

    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'toml'}  # 파일 업로드 가능 확장자 SETTING




# 테스트페이지
@router.route('/test-native-query')
def test_native_query_and_render(request: Request):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")

    # print(" __________________________________________________________________________________________________________________________________ NATIVE_QUERY UPDATE SETTING s")
    # # row        = None
    # # connection = None
    # db = pymysql.connect(
    #     host        =config_db['host'],
    #     user        =config_db['user'],
    #     password    =config_db['password'],
    #     database    =config_db['database'],
    #     charset='utf8'
    #     cursorclass = pymysql.cursors.DictCursor
    # )
    # cursor = db.cursor()
    # values_to_bind = [
    #     {'CUSTOMER_NAME': '_박_정_훈_11_', 'MASSAGE': '주문서변경요청','DATE_REQUESTED': str(get_time_as_style("0"))},
    # ]
    # sql ='''
    #     UPDATE REQUEST_TB
    #     SET CUSTOMER_NAME = %(CUSTOMER_NAME)s ,
    #         MASSAGE = %(MASSAGE)s ,
    #         DATE_REQUESTED = %(DATE_REQUESTED)s
    #     WHERE ID_REQUEST = 11
    #     ;
    # '''
    # cursor.executemany(sql, values_to_bind)
    # db.commit()
    # pause()


    # print(" __________________________________________________________________________________________________________________________________ ORM INSERT SETTING s")
    # engine = create_engine(db_url)
    # Base = declarative_base()
    #
    # class REQUEST_TB(Base):
    #     __tablename__ = "REQUEST_TB"
    #     ID_REQUEST = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True, autoincrement=True)
    #     CUSTOMER_NAME = sqlalchemy.Column(sqlalchemy.VARCHAR(length=13))
    #     MASSAGE = sqlalchemy.Column(sqlalchemy.VARCHAR(length=100))
    #     DATE_REQUESTED = sqlalchemy.Column(sqlalchemy.VARCHAR(length=100))
    #     USE_YN = sqlalchemy.Column(sqlalchemy.VARCHAR(length=2))
    #
    # Session = sqlalchemy.orm.sessionmaker()
    # Session.configure(bind=engine)
    # session = Session()
    # session.add(REQUEST_TB(CUSTOMER_NAME="_박_정_훈_y_", MASSAGE="주문서변경요청", DATE_REQUESTED=BusinessLogicUtil.get_time_as_('%Y_%m_%d_%H_%M_%S'), USE_YN="Y"))
    # session.commit()
    # session.close()


    return ''


@router.get("/종아해요/{who}")  # without 쿼리스트링
def 종아한대요(who):
    return {"message": f"종아해요 {who}을(를) 요"}


@router.get("/파라미터-로-쿼리스트링-설정")  # with 쿼리스트링 설정,  @router.get("/종아해요/{who}") -> @router.get("/종아해요/")
def love1(q):
    return {"message": f"{q}"}


@router.get("/파라미터-타입힌팅-으로-쿼리스트링-벨리데이션-설정")  # with query
def love3(q: str):
    return {"message": f"{q}"}


@router.get("/파라미터-타입힌팅-as-Union-으로-쿼리스트링-벨리데이션-nullable-설정")  # with query
def get_item(q: Union[str, None] = None):  # 쿼리스트링 q 를 nullable 하도록 설정
    return {"message": f"{q}"}


@router.get("/알겠음/items/{item_id}")  # fastapi 기본예제
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@router.get("/items/{item_id}")  # 몇 번 테스트해보니 이제 어떻게 만들었는지 이해감.
def read_item(item_id: int, q: Union[str, None] = None, p: Union[int, None] = None):
    return {"item_id": item_id, "q": q, "p": p}

# @router.get("/api/items/{id}")
# def read_item(id: int, q: Optional[str] = None):
#     return {"id": id, "q": q}

# @router.put("/api/items/{id}")
# async def update_item(id: int, item: Item):
#     result = {"id": id, **item.dict()}


# @router.delete("/api/items/{id}")
# def delete_item(id: int):
#     return {"deleted": id}




# class REQUEST_TB(Base):
#     __tablename__ = "REQUEST_TB"
#     # __table_args__ = {'mysql_collate': 'utf8_general_ci'}  # encoding 안되면 비슷하게 방법을 알아보자  mysql 용 코드로 보인다.
#     ID_REQUEST = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True, autoincrement=True)
#     CUSTOMER_NAME = sqlalchemy.Column(sqlalchemy.VARCHAR(length=13))
#     MASSAGE = sqlalchemy.Column(sqlalchemy.VARCHAR(length=100))
#     DATE_REQUESTED = sqlalchemy.Column(sqlalchemy.VARCHAR(length=100))
#     USE_YN = sqlalchemy.Column(sqlalchemy.VARCHAR(length=2))
#
#     def __init__(self, ID_REQUEST, CUSTOMER_NAME, MASSAGE, DATE_REQUESTED, USE_YN):
#         self.ID_REQUEST = ID_REQUEST
#         self.CUSTOMER_NAME = CUSTOMER_NAME
#         self.MASSAGE = MASSAGE
#         self.DATE_REQUESTED = DATE_REQUESTED
#         self.USE_YN = USE_YN
#
#     def add_new_records(ID_REQUEST, CUSTOMER_NAME, MASSAGE, DATE_REQUESTED, USE_YN):
#         new_records = REQUEST_TB(ID_REQUEST=ID_REQUEST, CUSTOMER_NAME=CUSTOMER_NAME, MASSAGE=MASSAGE, DATE_REQUESTED=DATE_REQUESTED, USE_YN=USE_YN)
#         session.add(new_records)
#         session.commit()
#
#     @staticmethod
#     def select_records_all():
#         records = session.query(REQUEST_TB).all()
#         records_as_str = ''
#         for Record in records:
#             tmp = '{{delimeter}}' + str(Record.ID_REQUEST) + '{{delimeter}}' + Record.CUSTOMER_NAME + '{{delimeter}}' + Record.MASSAGE + '{{delimeter}}' + Record.DATE_REQUESTED + '{{delimeter}}' + Record.USE_YN + ' \n'
#             records_as_str += tmp
#         print(records_as_str)
#
#     def select_records_by_id_Request(ID_REQUEST):
#         return session.query(REQUEST_TB).filter_by(ID_REQUEST=ID_REQUEST).order_by(REQUEST_TB.ID_REQUEST.desc()).all()
#
#     def select_records_by_id_request(ID_REQUEST):
#         return session.query(REQUEST_TB).filter_by_(ID_REQUEST=ID_REQUEST).first()
#
#     # def select_records_by_id_Request(ID_REQUEST, CUSTOMER_NAME):
#     #     return session.query(REQUEST_TB).filter(and_(REQUEST_TB.ID_REQUEST == item['ID_REQUEST'],
#     #                                                  REQUEST_TB.sequence_id == item['sequence_id'])).all()
#
#     def select_records_by_RowNumber(RowNumber):
#         records = session.query(REQUEST_TB).get(RowNumber)
#         records_as_str = ''
#         for Record in records:
#             tmp = '{{delimeter}}' + str(Record.ID_REQUEST) + '{{delimeter}}' + Record.CUSTOMER_NAME + '{{delimeter}}' + Record.MASSAGE + '{{delimeter}}' + Record.DATE_REQUESTED + '{{delimeter}}' + Record.USE_YN + ' \n'
#             records_as_str += tmp
#             print(records_as_str)
#         return records_as_str
#
#     def select_records_by_CUSTOMER_NAME_via_like(CUSTOMER_NAME='_박_정_훈_'):
#         records = session.query(REQUEST_TB).filter(REQUEST_TB.CUSTOMER_NAME.like('%' + CUSTOMER_NAME + '%'))
#         records_as_str = ''
#         for Record in records:
#             tmp = '{{delimeter}}' + str(Record.ID_REQUEST) + '{{delimeter}}' + Record.CUSTOMER_NAME + '{{delimeter}}' + Record.MASSAGE + '{{delimeter}}' + Record.DATE_REQUESTED + '{{delimeter}}' + Record.USE_YN + ' \n'
#             records_as_str += tmp
#             print(records_as_str)
#         return records_as_str
#
#     def select_records_where_CUSTOMER_NAME_is_not_(CUSTOMER_NAME='_박_정_훈_'):
#         records = session.query(REQUEST_TB).first(REQUEST_TB.CUSTOMER_NAME != CUSTOMER_NAME)
#         records_as_str = ''
#         for record in records:
#             tmp = '{{delimeter}}' + str(record.ID_REQUEST) + '{{delimeter}}' + record.CUSTOMER_NAME + '{{delimeter}}' + record.MASSAGE + '{{delimeter}}' + record.DATE_REQUESTED + '{{delimeter}}' + record.USE_YN + ' \n'
#             records_as_str += tmp
#             print(records_as_str)
#         return records_as_str
#
#     def select_records_by_Status(isActive):  # ,이건 뭐지?
#         records = session.query(REQUEST_TB).filter_by_(active=isActive)
#         records_as_str = ''
#         for Record in records:
#             tmp = '{{delimeter}}' + str(Record.ID_REQUEST) + '{{delimeter}}' + Record.CUSTOMER_NAME + '{{delimeter}}' + Record.MASSAGE + '{{delimeter}}' + Record.DATE_REQUESTED + '{{delimeter}}' + Record.USE_YN + ' \n'
#             records_as_str += tmp
#             print(records_as_str)
#         return records_as_str
#
#     def update_record_status(ID_REQUEST, isActive):  # isActive 이건 뭐지?  use_yn 개념 같아 보인다.
#         records = session.query(REQUEST_TB).get(ID_REQUEST)
#         records.active = isActive
#         session.commit()
#
#     def update_record_of_MASSAGE_by_ID_REQUEST(ID_REQUEST, MASSAGE):
#         session.query(REQUEST_TB).filter(REQUEST_TB.ID_REQUEST == ID_REQUEST).first().MASSAGE = MASSAGE
#         session.commit()
#
#     def delete_records_by_ID_REQUEST(ID_REQUEST):
#         session.query(REQUEST_TB).filter(REQUEST_TB.ID_REQUEST == ID_REQUEST).delete()
#         session.commit()
#
#     def delete_records_by_CUSTOMER_NAME(CUSTOMER_NAME='_박_정_훈_'):
#         session.query(REQUEST_TB).filter(REQUEST_TB.CUSTOMER_NAME == CUSTOMER_NAME).delete()
#         session.commit()


# success
# result = MySqlUtil.get_session_local().query(MemberUtil.Member).filter(MemberUtil.Member.id == id).first() # success , 그러나 타입힌팅 에러가...
# 테스트
# result = select(ItemsUtil.Item).where(ItemsUtil.Item.id.in_(["id1","id2"]))
# result = session.query(MySqlUtil.members).filter_by(id=id, pw=pw).first()
# result = session.query(MySqlUtil.members).filter_by(id=id).order_by(members.id.desc()).all()
# result = session.query(MySqlUtil.members).filter(members.name.ilike("%_박_정_훈_%").all_())
# result = MySqlUtil.get_session_local().query(MemberUtil.Member).filter_by(id=id, pw=pw).limit(2)



# orders
# boards
# lists