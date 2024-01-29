import inspect
import os
from typing import Union

import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException

from pkg_park4139 import ColoramaColorUtil, DebuggingUtil, FileSystemUtil, FastapiServerUtil, StateManagementUtil

NAV_ITEMS_JSON = StateManagementUtil.NAV_ITEMS_JSON
NAV_ITEMS = FastapiServerUtil.init_and_update_json_file(NAV_ITEMS_JSON)

app = FastAPI()


@app.get("/")
async def return_success():
    # DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
    DebuggingUtil.print_ment_via_colorama(f"{inspect.currentframe().f_code.co_name}() 호출되었습니다", colorama_color=ColoramaColorUtil.LIGHTWHITE_EX)
    return {"success": f"fastapi 서버로서 {os.path.basename(__file__)}를 구동 중 입니다"}

@app.get("/nav-items")
def get_nav_items():
    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
    [print(sample) for sample in NAV_ITEMS]
    return NAV_ITEMS

@app.get("/nav-items/{index}")
def get_nav_items_by_index(index: Union[int, None]):
    try:
        return NAV_ITEMS[index]
    except:
        DebuggingUtil.print_ment_fail(f"({len(NAV_ITEMS)})개의 등록된 nav_items 중, index 가 {index}인 nav_item 이 없습니다.")
        raise HTTPException(status_code=404, detail=f"({len(NAV_ITEMS)})개의 등록된 nav_items 중, index 가 {index}인 nav_item 이 없습니다.")


if __name__ == "__main__":
    # :: ASGI SERVER RUN SETTING
    # DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}")
    print()
    print()
    DebuggingUtil.commentize("fastapi 서버가 uvicorn 에 의해 로컬테스트 모드로 시작되었습니다")

    # 스웨거 자동실행
    # FileSystemUtil.explorer(fr"{FastapiServerUtil.Settings.protocol_type[0]}://{FastapiServerUtil.Settings.host[0]}:{FastapiServerUtil.Settings.port[0]}/docs")
    # FileSystemUtil.explorer(fr"{FastapiServerUtil.Settings.protocol_type[0]}://{FastapiServerUtil.Settings.host[0]}:{FastapiServerUtil.Settings.port[0]}/redoc")
    # FileSystemUtil.explorer(fr"{FastapiServerUtil.Settings.protocol_type[0]}://{FastapiServerUtil.Settings.host[0]}:{FastapiServerUtil.Settings.port[0]}")

    # 더미 데이터 객체 생성
    # FileSystemUtil.explorer(fr"{FastapiServerUtil.Settings.protocol_type[0]}://{FastapiServerUtil.Settings.host[0]}:{FastapiServerUtil.Settings.port[0]}/make-dummyies")

    uvicorn.run(
        app=f"{FileSystemUtil.get_target_as_n(__file__)}:app",
        host=FastapiServerUtil.Settings.host[0],  # class 를 사용하면 tuple 로 오며, str(tuple) 이렇게 사용할 수 없고, tuple[0] 으로 가져와야 하네. js 의 destructon 문법처럼 py의 unpacking 을 사용하는 방법이 있으나 변수 새로 생성해야함.
        port=FastapiServerUtil.Settings.port[0],
        # reload=True,  # 이 설정 너무 의존하지는 말자. pkg 변경 되면 rerun 다시 해줘야한다
        # log_level="info",
        # log_level="debug",
    )
