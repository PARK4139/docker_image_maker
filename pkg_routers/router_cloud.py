import inspect
import os
import shutil
import uuid
from tempfile import NamedTemporaryFile
from typing import List, IO

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
default_redirection_page_without_prefix = '/our-cloud'
default_redirection_page = f'/{prefix_promised}{default_redirection_page_without_prefix}'


@router.get("/our-cloud")
async def get_our_cloud(request: Request):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")
    FastapiUtil.jinja_data.prefix_promised = prefix_promised

    if 'id' in request.session and request.session['id'] != '':
        # 로그인 한 경우
        context = {"request": request, "jinja_data": FastapiUtil.jinja_data}
        return templates.TemplateResponse("/our_cloud.html", context=context)
    else:
        # 로그인 하지 않은 경우
        return RedirectResponse('/member')


@router.post("/our-cloud")
async def post_our_cloud(request: Request):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")
    FastapiUtil.jinja_data.prefix_promised = prefix_promised

    if 'id' in request.session and request.session['id'] != '':
        # 로그인 한 경우
        context = {"request": request, "jinja_data": FastapiUtil.jinja_data}
        return templates.TemplateResponse("/our_cloud.html", context=context)
    else:
        # 로그인 하지 않은 경우
        return RedirectResponse('/member')


@router.post("/upload-files")
async def post_upload_files(files: List[UploadFile]):
    function_name = inspect.currentframe().f_code.co_name
    DebuggingUtil.commentize(f"{function_name}()")

    # pkg_cloud 비우기
    # FileSystemUtil.truncate_tree(StateManagementUtil.DIRECTORY_CLOUD)

    # 클라이언트에서 보낸파일들 서버의 지정된 디렉토리에 저장
    UPLOAD_DIR = StateManagementUtil.DIRECTORY_CLOUD
    for file in files:
        content = await file.read()
        # filename = f"{str(uuid.uuid4())}.jpg"  # uuid로 유니크한 파일명으로 변경
        DebuggingUtil.print_magenta(rf'''file.filename : {file.filename}''')
        if file.filename.strip()=="":
            return HTMLResponse(content=f'''<script>alert("선택된 파일이 없습니다");window.location.href='our-cloud';</script>''')
        with open(os.path.join(UPLOAD_DIR, file.filename), "wb") as fp:
            fp.write(content)
            return HTMLResponse(content=f'''<script>alert("파일이 업로드 되었습니다");window.location.href='our-cloud';</script>''')
    # return {"filenames": [file.filename for file in files]}
    # file 이라는 이름으로 해당 파일 객체를 받으므로,
    # 클라이언트단(html)에서는 file/files이라는 키값(아마도 name 태그를 의미하는 듯) 설정하지 않으면 422 Unprocessable Entity 에러

    return RedirectResponse('our-cloud')


@router.get("/our-cloud/download/{file_nx}")
async def get_out_cloud_download_file_nx(file_nx):
    targetFile = rf"{StateManagementUtil.DIRECTORY_CLOUD}\{file_nx}"
    DebuggingUtil.print_magenta(f"targetFile:{StateManagementUtil.INDENTATION_PROMISED}{targetFile}")
    return FileResponse(path = targetFile, filename=file_nx ) # media_type- 미디어 유형을 제공. 설정하지 않으면 파일 이름이나 경로를 사용하여 미디어 유형을 추론합니다.