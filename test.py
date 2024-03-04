__author__ = 'PARK4139 : Jung Hoon Park'

# as 는 별칭을 설정하는 키워드
import inspect
import os
import random
import re
# -*- coding: utf-8 -*-  # python 3.x 하위버전 호환을 위한코드
import sys
import traceback
from io import BytesIO, StringIO

import pandas as pd
import plotly.figure_factory as ff
from PySide6.QtWidgets import QApplication
from bs4 import ResultSet, BeautifulSoup

from pkg_park4139_for_linux import TestUtil, DebuggingUtil, BusinessLogicUtil, StateManagementUtil, MySqlUtil, FinanceStockTickerUtil, FileSystemUtil, StockInfoUtil, SeleniumUtil


class TestUtilReplica:
    is_first_test_lap = True
    test_results = []

    @staticmethod
    # 이해한 게 문제가 있는지 상속에 대한 실험은 꼭 진행해보도록 하자.
    # 하지만 부모 class 로 만든 인스턴스에 영향이 없도록(값의 공유가 되지 않도록) 사용하는 것이 기본적인 방법으로
    # 심도있게 예측해야할 상황은 field 가 공유되도록 해야 될때 이다.
    # 예시로 Account 번호를 DB에 넣는 객체는 singletone으로 유지.
    # Parent().name    parent.name   Child().name   child.name
    def pause():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        DebuggingUtil.commentize(f"__________________________________________________{inspect.currentframe().f_code.co_name}")
        BusinessLogicUtil.print_today_time_info()
        os.system('pause >nul')

    @staticmethod
    def measure_seconds_performance(function):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        """시간성능 측정 데코레이터 코드"""

        # def wrapper(*args, **kwargs):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")

        def wrapper(**kwargs):  # **kwargs, keyword argument, dictionary 로 parameter 를 받음. named parameter / positional parameter 를 받을 사용가능?
            DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
            # def wrapper(*args):# *args, arguments, tuple 로 parameter 를 받음.
            DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
            # def wrapper():
            DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
            test_cycle_max_limit = 5
            if TestUtil.is_first_test_lap:
                ment = rf"총 {test_cycle_max_limit}번의 시간성능측정 테스트를 시도합니다"
                TestUtil.is_first_test_lap = False
                DebuggingUtil.print_ment_light_yellow(ment)
            seconds_performance_test_results = TestUtil.test_results
            import time
            time_s = time.time()
            # function(*args, **kwargs)
            function(**kwargs)
            # function(*args)
            # function()
            time_e = time.time()
            mesured_seconds = time_e - time_s
            DebuggingUtil.print_ment_yellow(f"{StateManagementUtil.UNDERLINE_PROMISED}시간성능측정 결과")
            seconds_performance_test_results.append(f"{round(mesured_seconds, 2)}sec")
            DebuggingUtil.print_ment_yellow(rf'seconds_performance_test_results : {seconds_performance_test_results}')
            # DebuggingUtil.print_ment_yellow(rf'type(seconds_performance_test_results) : {type(seconds_performance_test_results)}')
            DebuggingUtil.print_ment_yellow(rf'len(seconds_performance_test_results) : {len(seconds_performance_test_results)}')
            if len(seconds_performance_test_results) == test_cycle_max_limit:
                DebuggingUtil.print_ment_yellow("시간성능측정이 완료 되었습니다")
                DebuggingUtil.print_ment_yellow(f"{StateManagementUtil.UNDERLINE_PROMISED}TEST END")
                TestUtil.pause()

        return wrapper

    @staticmethod
    def measure_milliseconds_performance(function):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        """시간성능 측정 코드"""

        def wrapper(*args, **kwargs):
            DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
            # def wrapper(*args):# *args, arguments, tuple 로 parameter 를 받음.
            DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
            # def wrapper():
            DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
            DebuggingUtil.commentize(f"__________________________________________________{inspect.currentframe().f_code.co_name}")
            test_cycle_max_limit = 5
            milliseconds_performance_test_result = []
            import time
            time_s = time.time()
            # function(*args, **kwargs)
            function(**kwargs)
            # function(*args)
            # function()
            time_e = time.time()
            mesured_seconds = time_e - time_s
            DebuggingUtil.commentize(rf"시간성능측정 결과")
            milliseconds_performance_test_result.append(round(mesured_seconds * 1000, 5))
            print(rf'milliseconds_performance_test_result : {milliseconds_performance_test_result}')
            print(rf'type(milliseconds_performance_test_result) : {type(milliseconds_performance_test_result)}')
            print(rf'len(milliseconds_performance_test_result) : {len(milliseconds_performance_test_result)}')
            if len(milliseconds_performance_test_result) == test_cycle_max_limit:
                DebuggingUtil.print_magenta("시간성능측정이 완료 되었습니다")
                TestUtil.pause()

        return wrapper


# LOGGER SET UP
# logger = logging.getLogger('park4139_test_logger')
# hdlr = logging.FileHandler('park4139_logger.log')
# hdlr.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
# logger.addHandler(hdlr)
# logger.setLevel(logging.INFO)


# DebuggingUtil.commentize() 메소드 테스트 결과, 1개 파일을 만들어 실행하는 데까지 무려 11초 정도로 측정됨, ffmpeg 작업 속도로 문제
# 의도적으로 mp3 파일을 미리 만들어, ffmpeg 로 두 파일 합성작업 시간을 줄일수 있으므로, 성능 최적화 기대,
# 따라서, 코드에서 사용되는 모든 텍스트를 추출하여 DebuggingUtil.commentize 하도록 하여, 최적화시도해보자
# 번외로 리스트의 파라미터를 몇개까지 가능하지 테스트 해보고 싶긴한데, 망가져도 되는 컴퓨터로 시도해보자


def decorate_test_status_printing_code(function):
    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")

    def wrapper():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        DebuggingUtil.commentize(rf"test status")
        function()

    return wrapper


qss = """
    # QWidget {
    #     color: #FFFFFF;
    #     background: #333333;
    #     height: 32px;
    # }
    # QLabel {
    #     color: #FFFFFF;
    #     background: #333333;
    #     font-size: 16px;
    #     padding: 5px 5px;
    # }
    # QToolButton {
    #     background: #333333;
    #     border: none;
    # }
    # QToolButton:hover{
    #     background: #444444;
    # }
"""

# 테스트 루프 카운트 최대치 설정
test_loop_limit = 3


@TestUtil.measure_seconds_performance_nth
def crawl_geo_info():
    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
    driver = None
    try:
        driver = SeleniumUtil.get_driver_for_selenium()
        target_url = 'https://www.google.com/search?q=현재위치'
        DebuggingUtil.print_magenta(rf'''target_url : {target_url}''')
        driver.get(target_url)
        page_src = driver.page_source
        soup = BeautifulSoup(page_src, "lxml")
        results: any
        # results = soup.find_all("body")
        results: ResultSet = soup.find_all("span", class_="BBwThe")  # 지역정보 한글주소
        # results: ResultSet = soup.find_all("span", class_="fMYBhe") # 지역정보 영어주소
        results: str = results[0].text
        results_about_geo = results
        DebuggingUtil.print_magenta(ment='지역정보  웹크롤링 완료')
        DebuggingUtil.print_magenta(f'''results_about_geo :\n{results_about_geo}''')
    finally:
        # driver.close()
        driver.quit()


@TestUtil.measure_seconds_performance_nth
def crawl_naver_weather():
    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
    # 테이블이 존재하는 html url 에서 table 의 데이터를 가져올때 유용한 함수 pd.read_html()
    # df = pd.read_html('http://m.infostock.co.kr/sector/sector_detail.asp?code=64&theme=2%uCC28%uC804%uC9C0&mode=w')[1]  # 막혀있음, 토큰이 필요한 듯, 이 방식으로는 안됨, selenium 으로는 시도해볼만 하다고 생각함.
    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
    driver = None
    try:
        driver = SeleniumUtil.get_driver_for_selenium()
        target_url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=동안구+관양동+날씨'
        DebuggingUtil.print_magenta(rf'''target_url : {target_url}''')
        driver.get(target_url)
        page_src = driver.page_source
        soup = BeautifulSoup(page_src, "lxml")
        results: ResultSet = soup.find_all("div", class_="status_wrap")
        results: str = results[0].text
        # 데이터 클렌징
        results: str = results.replace("오늘의 날씨", "오늘의날씨")
        results: str = results.replace(" 낮아요", "낮아요")
        results: str = results.replace(" 높아요", "높아요")
        results: str = results.replace(" 체감", "체감온도")
        results_refactored = results.split(" ")
        results_refactored: [str] = [x for x in results_refactored if x.strip(" ") and x.strip("") and x.strip("\"") and x.strip("\'") and x.strip("\'\'")]  # 불필요 리스트 요소 제거 ( "" , "\"", " " ...)
        results_refactored: [str] = [x for x in results_refactored if x.strip("현재")]  # 리스트 요소 "오늘의"
        # 리스트 내 특정문자와 동일한 요소의 바로 뒷 요소를 가져와 딕셔너리에 저장 # 데이터의 key, value 형태가 존재하면서 순번이 key 다음 value 형태로 잘 나오는 경우 사용.
        keys_predicted = ['온도', '체감온도', '습도', '서풍', '동풍', '남풍', '북풍', '북서풍', '미세먼지', '초미세먼지', '자외선', '일출', '오늘의날씨']
        results_: dict = {}
        for i in range(len(results_refactored) - 1):
            for key_predicted in keys_predicted:
                if results_refactored[i] == key_predicted:
                    key = results_refactored[i]
                    value = results_refactored[i + 1]
                    results_[key] = value
        results_refactored = results_
        results: str = "\n".join([f"{key}: {value}" for key, value in results_refactored.items()])  # dict to str (개행을 시킨)
        results_about_naver_weather = results
        DebuggingUtil.print_magenta(ment='동안구 관양동 날씨 웹크롤링 완료')
        DebuggingUtil.print_magenta(f'''results_about_naver_weather :\n{results_about_naver_weather}''')

    finally:
        # driver.close()
        driver.quit()

    # df = df[3:]  # 상위 3개의 행 제거
    # DebuggingUtil.print_magenta(rf'''df : {df}''')


@TestUtil.measure_seconds_performance_nth
def crawl_pm_ranking():
    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
    driver = None
    try:
        driver = SeleniumUtil.get_driver_for_selenium()
        target_url = f'https://www.dustrank.com/air/air_dong_detail.php?addcode=41173103'
        DebuggingUtil.print_magenta(rf'''target_url : {target_url}''')
        driver.get(target_url)
        page_src = driver.page_source
        soup = BeautifulSoup(page_src, "lxml")
        # results = soup.find_all(href=re.compile("magnet"), id='link1') # <a class="sister" href="http://example.com/magnet" id="link1">Elsie</a>
        results = soup.find_all("table", class_="datatable")  # <table class="datatable">foo!</div>
        soup = BeautifulSoup(str(results), "lxml")
        results = soup.find_all("table")[-1]
        soup = BeautifulSoup(str(results), "lxml")
        results = soup.find_all("table")[-1].text
        results = results.split("\n")  # 리스트
        results = [x for x in results if x.strip()]
        results = [x for x in results if x.strip(",")]  # 리스트 요소 "," 제거
        # results = [x + '\n' for x in results] #리스트 요소마다 \n prefix 로서 추가
        head_1 = results[1]
        head_2 = results[2]
        # body = results[3]+'\n'*10
        # body = re.split(r"[,!?]", results[3]) #, !, ? 이면 쪼개기
        # pattern = r'\d{2}-\d{2}-\d{2} \d{2}:\d{2}[가-힣]+\(\d+\)[가-힣]+\(\d+\)'
        pattern = r'(\d{2}-\d{2}-\d{2} \d{2}:\d{2})([가-힣]+\(\d+\))([가-힣]+\(\d+\))'  # 정규식을 () 로 부분 부분 묶으면 tuple 형태로 수집할 수 있다.
        body = re.findall(pattern, results[3])
        body = list(body)  # tuple to list
        body = [list(item) for item in body]  # LIST 내 ITEM 이 TUPLE 일 때 ITEM 을 LIST 로 변환 #의도대로 잘 변했으~

        # 리스트 요소를 3개 단위로 개행하여 str 에 저장
        body_ = ""
        for i in range(0, len(body), 1):
            body_ = body_ + body[i][0] + body[i][1] + body[i][2] + "\n"
        body = body_
        # body = "\n".join(body) # list to str
        results = f"{head_1}\t{head_2}\n{body}"

        results_about_pm_ranking = results

        DebuggingUtil.print_magenta(ment='미세먼지 초미세먼지 웹크롤링 완료')
        DebuggingUtil.print_magenta(f'''results_about_pm_ranking :\n{results_about_pm_ranking}''')

    finally:
        # driver.close()
        driver.quit()


@TestUtil.measure_seconds_performance_nth
def crawl_korean_ultrafine_dust():
    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
    driver = None
    try:
        # # '전국초미세먼지'(bs4 way)
        target_url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&qvt=0&query=전국초미세먼지'
        DebuggingUtil.print_magenta(rf'''target_url : {target_url}''')
        driver = SeleniumUtil.get_driver_for_selenium()
        driver.get(target_url)
        page_src = driver.page_source
        soup = BeautifulSoup(page_src, "lxml")
        results: any
        # results = soup.find_all("body")
        results: ResultSet = soup.find_all("div", class_="detail_box")
        results: str = results[0].text
        results: str = results.replace("지역별 초미세먼지 정보", "")
        results: str = results.replace("관측지점 현재 오전예보 오후예보", "")
        results: str = results.replace("", "")
        results___: [str] = results.split(" ")
        results___: [str] = [x for x in results___ if x.strip(" ") and x.strip("") and x.strip("\"") and x.strip("\'") and x.strip("\'\'")]  # 불필요 리스트 요소 제거 ( "" , "\"", " " ...)

        # 리스트 요소를 4개 단위로 개행하여 str 에 저장
        results_: str = ""
        for i in range(0, len(results___), 4):
            if i == len(results___):
                pass
            results_ = f"{results_}\t{results___[i]}\t{results___[i + 1]}\t{results___[i + 2]}\t{results___[i + 3]}\n"
        results___ = results_
        results_about_nationwide_ultrafine_dust = results___

        DebuggingUtil.print_magenta(ment='초미세먼지 웹크롤링 완료')
        DebuggingUtil.print_magenta(f'''results_about_nationwide_ultrafine_dust :\n{results_about_nationwide_ultrafine_dust}''')

    finally:
        # driver.close()
        driver.quit()


@TestUtil.measure_seconds_performance_nth
def test_core_etc():
    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
    try:
        # cmd = rf'python "{test_target_file}"' # SUCCESS # 가상환경이 아닌 로컬환경에서 실행이 됨.
        # cmd = rf'start cmd /k "{test_helping_bat_file}" {test_target_file}'  # SUCCESS # 가상환경에서 실행 # 새 cmd.exe 창에서 열린다
        # cmd = rf'start /b cmd /c "{test_helping_bat_file}" {test_target_file}' # FAIL  # 가상환경에서 실행되나 콘솔에 아무것도 출력되지 않음
        # cmd = rf'call "{test_helping_bat_file}" {test_target_file}'  # FAIL  # 가상환경에서 실행되나 콘솔에 사용자 입력만 출력됨
        # cmd = rf'"{test_helping_bat_file}" {test_target_file}' # FAIL  # 가상환경에서 실행되나  콘솔에 사용자 입력만 출력됨
        # cmd = rf'call cmd /c "{test_helping_bat_file}" {test_target_file}'  # FAIL  # 가상환경에서 실행되나 콘솔에 사용자 입력만 출력됨
        # cmd = rf'start cmd /c "{test_helping_bat_file}" {test_target_file}'  # SUCCESS # 가상환경에서 실행 # 새 cmd.exe 창에서 열린다 #이걸로 선정함
        # park4139.get_cmd_output(cmd)

        # DebuggingUtil.print_magenta(f"test")
        # print(f"test")

        # Park4139.ask_to_google(question)
        # Park4139.ask_to_bard(question)
        # Park4139.ask_to_wrtn(question)

        # Park4139.speak_alt("테스트")

        # app = QApplication()
        # Park4139.get_comprehensive_weather_information_from_web()
        # app.exec()

        # __________________________________________________________________________________________________________________________________ TESTED SECTION 2
        # dialog =  pkg_park4139_for_linux.CustomDialog(contents="테스트를 시작할까요?", buttons=["시작하기", "시작하지 않기"])
        # dialog.exec()
        # dialog.show()

        # global dialog
        # dialog = pkg_park4139_for_linux.CustomDialog(contents="다운로드하고 싶은 URL을 제출해주세요?", buttons=["제출", "제출하지 않기"], is_input_text_box=True)
        # dialog.show()
        # text_of_clicked_btn = dialog.text_of_clicked_btn
        # DebuggingUtil.commentize("text_of_clicked_btn")
        # DebuggingUtil.print_magenta(text_of_clicked_btn)
        # if text_of_clicked_btn == "제출":
        #     Park4139.download_from_youtube_to_webm(dialog.box_for_editing_input_text.text())

        # # CustomDialog 를 쓰레드 안에서 띄우기
        # import sys
        # import time
        # from PySide6.QtCore import QThread, Signal
        # from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QDialog
        # app = QApplication(sys.argv)
        # class CustomDialogThread(QThread):
        #     show_dialog_signal = Signal()
        #     def run(self):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        #         self.show_dialog_signal.emit()
        # def show_dialog():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        #     from pkg_park4139_for_linux import CustomDialog
        #     dialog = CustomDialog(contents="테스트를 시작할까요?", buttons=["시작하기", "시작하지 않기"])
        #     # dialog.exec()
        #     dialog.show()
        # thread = CustomDialogThread()
        # thread.show_dialog_signal.connect(show_dialog)
        # thread.start()
        # sys.exit(app.exec())
        # __________________________________________________________________________________________________________________________________ TESTED SECTION 2

        # __________________________________________________________________________________________________________________________________  UP (TESTED SUCCESS)
        app = QApplication()
        app.exec()
        # __________________________________________________________________________________________________________________________________ BELOW (NOT TESTED YET)

        # 사용에 유의해야 한다.
        # 값이 공유가 되니 유의해야 한다. 오히려 이점을 활용해서 공유객체를 사용할 수 있지 않을까?

        # 얕은 복사 실험 # 이것도 얕은 복사네요.
        # li = [1, 2]
        # ls_copied = li
        # ls_copied[0] = 2
        # print(ls_copied) # [2, 2]
        # print(ls) # [2, 2]? or [1, 2]?

        # 얕은 복사 실험
        # li = [1, 2]
        # ls_copied = copy.copy(li)
        # ls_copied[0] = 2
        # print(ls_copied) # [2, 2]
        # print(ls) # [2, 2]? or [1, 2]?

        # 깊은 복사 실험
        # li_deepcopied=copy.deepcopy(li) # 오히려 딥카피의 경우가 사용하는데 자유로운 생각이 든다.

        # 셀레니움 새로운 문법
        # https://selenium-python.readthedocs.io/locating-elements.html
        # find_element(By.ID, "id")
        # find_element(By.NAME, "name")
        # find_element(By.XPATH, "xpath")
        # find_element(By.LINK_TEXT, "link text")
        # find_element(By.PARTIAL_LINK_TEXT, "partial link text")
        # find_element(By.TAG_NAME, "tag name")
        # find_element(By.CLASS_NAME, "class name")
        # find_element(By.CSS_SELECTOR, "css selector")

        # foo = ",".join(key for key in park4139.keyboards).split(",")# DICTIONARY TO STR AS CSV STYLE
        # print(foo)

        # foo = [keyValue for keyValue in park4139.keyboards]
        # print(foo)

        # for key, value in park4139.keyboards.items():
        #     print(key, value)
        # for key, value in park4139.keyboards.items():
        #     print(key)
        # for key, value in park4139.keyboards.items():
        #     print(value)

        # 파이썬 리스트 특정요소를 특정문자를 기준으로 두 요소로 분리해서 그 특정요소 리스트 자리에 그대로 삽입하는 코드   ['1','온도많음','2'] -> ['1','온도','많음','2']
        # certain_text: str = '온도'
        # results_ = []
        # for item in results:
        #     if certain_text in item:
        #         words = item.split(certain_text)
        #         results_.append(certain_text)
        #         results_.extend(words)
        #     else:
        #         results_.append(item)
        # results: [str] = results_
        # print(context=f"{results}")

        # 파이썬 리스트의 요소홀수가 key 요소짝수가 value 로서 dict 에 넣기
        # results_: dict = {}
        # for i in range(0, len(results) - 1, 2):
        #     if i == len(results) - 1:
        #         pass
        #     else:
        #         results_[results[i]] = results[i + 1]
        # results: dict = results_

        # results = soup.select(copied_html_selector)
        # for index, element in enumerate(results, 1):
        #     # print("{} 번째 text: {}".format(index, element.text))
        #     continue
        # element_str = element.text.strip().replace('현재 온도', '')
        # print(element_str)

        # soup.prettify()
        # print(str(soup))
        # print(str(soup.prettify()))

        # for index, element in enumerate(elements, 1):
        #     # print("{} 번째 text: {}".format(index, element.text))
        #     continue

        # # 여러개 체크박스 체크 예제
        # for i in pyautogui.locateAllOnScreen("checkbox.png"):
        #     pyautogui.click(i, duration=0.25)

        # 화면에서 특정범위를 제한하여 이동할때
        # img_capture = pyautogui.locateOnScreen("Run_icon.png", region=(1800, 0, 1920, 100))
        # img_capture = pyautogui.locateOnScreen("Run_icon.png", confidence=0.7)  # 인식이 잘안될때   유사도 70%  으로 설정
        # pyautogui.moveTo(img_capture)

        # 공들여 만든 느린 코드..
        sample = []
        # [print(sample) for sample in samples]  # 리스트를 한줄코드로 출력
        # sample = [x for x in sample if not x==None]  # from [None] to []
        # sample = [x if x is not None else "_" for x in sample]  # from [None] to ["_"]
        # sample = [x for x in sample if x.strip()]  # from [""] to []
        sample = [x if x is not None else "" for x in sample]  # from [None] to [""]
        sample = "".join(sample)  # from ["a", "b", "c"] to "abc"
        # abspaths을 mtimes 에 맞춰서 내림차순 정렬(파일변경일이 현시점에 가까운 시간인 것부터 처리하기 위함)
        # abspaths_and_mtimes = _get_processed_abspaths_and_mtimes(abspaths, mtimes)# 쓰레드 5개로 분산처리해도 5분 걸림...
        # abspaths_and_mtimes = Park4139List.get_list_added_elements_alternatively(abspaths, mtimes)  # from [1, 2, 3] + [ x, y, z] to [1, x, 2, y, 3, z]
        # abspaths_and_mtimes = Park4139List.get_nested_list_grouped_by_each_two_elements_in_list(abspaths_and_mtimes)  # from ["a", "b", "c", "d"] to [["a","b"], ["c","d"]]
        # abspaths_and_mtimes = Park4139List.get_nested_list_sorted_by_column_index(nested_list=abspaths_and_mtimes, column_index=1, decending_order=True)
        # abspaths_and_mtimes = Park4139List.get_list_seperated_by_each_elements_in_nested_list(abspaths_and_mtimes)  # from [["a","b"], ["c","d"]] to ["a", "b", "c", "d"]
        # abspaths_and_mtimes = Park4139List.get_list_each_two_elements_joined(abspaths_and_mtimes)  # from ["a", "b", "c", "d"] to ["ab", "cd"]
        # samples = [f"{key}: {value}" for key, value in samples.items()]  # from dict to ["key: value\n"]
        # samples = get_list_added_elements_alternatively(dirnames, tree_levels)  # from [][] to []
        # abspaths_and_mtimes = get_list_each_two_elements_joined(abspaths_and_mtimes)  # from ["a", "b", "c", "d"] to ["ab", "cd"]
        # samples = get_list_grouped_by_each_two_elements_in_list(samples)
        # samples = get_nested_list_sorted_by_column_index(nested_list=samples, column_index=1, decending_order=True)  # tree depth를 의미하는 column_index=1 에 대한 내림차순 정렬
        # samples = get_nested_list_removed_row_that_have_nth_element_dulplicated_by_column_index(nested_list=samples, column_index=0)  # from [[]] to [[]] # from [[1 2]] to [[1, 2]] # from [ [str str] [str str] ]  to  [ [str, str], [str, str]]
        # samples = np.array([dirnames, tree_levels]) # 두 리스트를 ndarry 로 합하기
        # samples = np.transpose(samples)  # 행과 열을 교체, from ndarry to ndarry
        # samples = dirnames + tree_levels  # 두 리스트를 [] 로 합하기 # from [][] to []
        # samples = [dirnames + tree_levels]  # 두 리스트를 [[]] 로 합하기 # from [][] to [[][]]
        # samples = [[row[i] for row in samples] for i in range(len(samples[0]))] # 행과 열을 교체 # from [[]] to [[]]
        # samples = get_nested_list_converted_from_ndarray(ndarray = samples)  # from ndarray to [[]]
        # samples: [str] = sorted(samples, key=lambda sample: sample[1], reverse=True)  # 비중첩 list 의 특정 열의 내림차순 정렬
        # samples = np.transpose(samples) # 행과 열을 교체 # to ndarry
        # samples = samples[np.argsort(-samples[:, 0].astype(int))] # 2차원배열 첫 번째 열을 기준으로 내림차순으로 정렬 # to ndarry
        # samples = list(set(samples))  # list to list 중복제거(orderless way)
        # tree_levels_and_abspaths_and_mtimes = get_list_added_elements_alternatively(abspaths_and_mtimes, abspaths)  # from [1, 2, 3] + [ x, y, z] to [1,x,2,y,3,z]

        # ndarray 핸들링
        # tree_levels_and_abspaths_and_mtimes = np.array([tree_levels, abspaths, mtimes])
        # tree_levels_and_abspaths_and_mtimes = np.transpose(tree_levels_and_abspaths_and_mtimes)

        # 오늘의 에러
        # 결론 : TypeError: 'int' object is not subscriptable 나타나면, 내가 int 를 슬라이싱하고 있나 확인해보자. int 는 슬라이싱하면 안된다.
        # TypeError: 'int' object is not subscriptable
        # 오늘만난 에러는 해당 오류는 정수형 객체가 인덱싱을 지원하지 않기 때문에 발생하는 오류입니다. 이 오류는 보통 정수형 변수를 대신하여 리스트나 튜플과 같은 인덱싱이 가능한 객체를 사용해야 할 때 발생합니다.
        # 예를 들어, 다음과 같은 상황에서 해당 오류가 발생할 수 있습니다
        # 문제코드
        # for index, item in enumerate(samples): # enumerate 로 리스트의 원소를 2개씩 출력
        #     print(rf'item[index] : {str(item[index])}')
        #     print(rf'item[index+1] : {str(item[index+1])}')

        # 해설
        # samples : [int] 였는데
        # item 은 int 였을 것이며.
        # int 를 [] 인덱스로 찾으려고 하니 문제가 발생한 것이다.

        # 해결코드 ( 의도된 방향으로 고치면 )
        # for index, item in enumerate(samples): # enumerate 로 리스트의 원소를 2개씩 출력
        #     print(rf'samples[index] : {str(samples[index])}')
        #     print(rf'samples[index+1] : {str(samples[index+1])}')

        # samples = sorted(samples, reverse=True) # 내림차순 정렬
        # 파이썬 요소가 5만 개의 문자열 리스트를 요소에 대해서 중복제거를 하는 가장 빠른 방법을 알아보고 싶긴한데. 나중에 실험비교 해보자

        # 파이썬 문자열 핸들링 성능 향상 아이디어 > 문자열 짧은 문자로 나오게 암호화 시키는 방법 > 문자열을 압축하는 기술 > Lempel-Ziv-Welch (LZW) 알고리즘 > 짧은 문자열로 암호화 시켜준다 > 짧은 문자열 이면 파이선 검색속도가 빨라지지 않을까?
        # db.toml 에는 특수문자가 들어갈 수 없다. > 특수문자가 있는 문자열을 특수문자가 없는 문자열로 압축 알고리즘 > Huffman 알고리즘 > 원래의 문자열을 알아야 하기 때문에 패스
        # 압축될 데이터들 특성 분석해서 LZW 압축을 효율적으로 할 수 있는 딕셔너리 적용 > 압축률 증가 > 사용될 57000 개 파일들의 경로명의 특성 분석 > 프로젝트 패키지명을 딕셔너리 첫번째 요소로 사용, \ 로 파일들의 경로 쪼개서 중복이 있는 요소들만 딕셔너리에 추가

        # LZM 용 딕셔너리 제작 함수
        # 아이디어 1. dirname abspath 의 len 를 tree depth 별로 정렬 > 중복제거 > 딕셔너리 저장 > 문자열 압축률 50프로 이상 가능 할 것으로 생각됨 (딕셔너리는 depression 시 필요하므로 잘 저장해 둬야한다) > 데이터분석해서 하드코딩으로 딕셔너리 작성.
        # 아이디어 2. 파일명은 문자열 데이터 중복 분석 알고리즘 적용 >

        # 진행상황
        #     아이디어 1. 의 중복제거 까지 완료

        # samples = [
        #     r"C:\Users\123\Desktop\services\archive_py\py_pkg_ver_.log",
        #     r"C:\Users\123\Desktop\services\archive_py\poetry.lock",
        #     r"C:\Users\123\Desktop\services\archive_py\pkg_yt_dlp\yt-dlp.sh",
        #     r"C:\Users\123\Desktop\services\archive_py\pkg_yt_dlp\yt-dlp.cmd",
        #     r"C:\Users\123\Desktop\services\archive_py\pkg_yt_dlp\yt_dlp\utils\_legacy.py",
        #     r"C:\Users\123\Desktop\services\archive_py\pkg_yt_dlp\yt_dlp\utils\_deprecated.py",
        #     r"C:\Users\123\Desktop\services\archive_py\pkg_yt_dlp\yt_dlp\postprocessor\xattrpp.py",
        #     r"C:\Users\123\Desktop\services\archive_py\pkg_yt_dlp\yt_dlp\postprocessor\sponsorblock.py",
        #     r"C:\Users\123\Desktop\services\archive_py\pkg_yt_dlp\yt_dlp\postprocessor\__pycache__\xattrpp.cpython-311.pyc",
        #     r"C:\Users\123\Desktop\services\archive_py\pkg_yt_dlp\yt_dlp\postprocessor\__pycache__\sponsorblock.cpython-312.pyc",
        #     r"C:\Users\123\Desktop\services\archive_py\pkg_yt_dlp\yt_dlp\postprocessor\__pycache__\sponsorblock.cpython-311.pyc",
        #     r"C:\Users\123\Desktop\services\archive_py\pkg_yt_dlp\yt_dlp\networking\__pycache__\websocket.cpython-311.pyc",
        #     r"C:\Users\123\Desktop\services\archive_py\pkg_yt_dlp\yt_dlp\networking\__pycache__\exceptions.cpython-312.pyc",
        #     r"C:\Users\123\Desktop\services\archive_py\pkg_yt_dlp\yt_dlp\networking\__pycache__\exceptions.cpython-311.pyc",
        # ]
        # samples = samples

        # current_directory_state = [f"{key}" for key, value in current_directory_state.items()]  # from dict to ["key\n"]

        # current_target_files = current_directory_state
        # current_target_files = current_directory_state[0:]
        # current_target_files = current_directory_state[0:9999]  # 샘플 10000개 테스트
        # current_target_files = current_directory_state[0:4999]  # 샘플 5000개 테스트
        # current_target_files = current_directory_state[0:999]  # 샘플 1000개 테스트
        # current_target_files = current_directory_state[0:99]  # 샘플 100개 테스트
        # current_target_files = current_directory_state[0:9]  # 샘플 10개 테스트

        # 세 리스트의 핸들링
        # abspaths = [sample for sample in current_target_files]  # 파일절대경로 목록
        # mtimes = [os.path.getmtime(sample) for sample in current_target_files]  # 파일생성일자 목록
        # 이 경우는 list comprehension을 사용해셔 가독성이 좋았지만. 50000개의 파일을 무려 2번이나 돌아야 하는게 흠이다.
        # 1번만 돌도록 성능개량, 하으...그래도 3초 넘개 걸림. 공부한 쓰레드 적용해보자!

        # def get_files_cnt_of_directory(directory):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        #     """
        #     사용법
        #     file_count = get_files_cnt_of_directory(directory_abspath)
        #     """
        #     # try:
        #     #     files_count = 0
        #     #     for _, _, files in os.walk(directory):
        #     #         files_count += len(files)
        #     #     return int(files_count)
        #     # except:
        #     #     pass
        #
        #     # try:
        #     #     cmd = 'cmd /c dir /s /b /a-d'
        #     #     result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
        #     #     file_list = result.stdout.splitlines()
        #     #     files_count = len(file_list)
        #     #     return int(files_count)
        #     # except:
        #     #     pass
        #
        #     try:
        #         cmd = f'dir /s /a /w "{directory}"'
        #         lines = Park4139.get_cmd_output(cmd=cmd)
        #         # print(lines[-3:]) # 리스트 내에서 뒤에서 3개만 출력
        #         files_count = lines[-3].split("File(s)")[0].strip()
        #         return int(files_count)
        #     except:
        #         pass

        # files_to_exclude = [
        #     Park4139.DB_TOML,
        #     Park4139.SUCCESS_LOG,
        #     Park4139.LOCAL_PKG_CACHE_FILE,
        # ]
        # current_target_files = []
        # for root, dirs, files in os.walk(directory_abspath):
        #     for file in files:
        #         file_abspath = os.path.join(root, file)  # 파일 절대 경로
        #         if file_abspath not in files_to_exclude:
        #             mtime = os.path.getmtime(file_abspath)  # 파일 생성 일자
        #             file_abspath = Park4139.get_str_replaced_special_characters(target=file_abspath, replacement="_")  # 파일 경로에서 특수문자 제거처리. toml 에 들어가지 않음.
        #             current_target_files.append([file_abspath, mtime])
        # # abspaths = [file_info[0] for file_info in current_target_files]  # file_info_list 이미 생성된 것이기때문에 이 리스트 컴프리헨션 에서는 또 돌지 않는다고 한다.
        # # mtimes = [file_info[1] for file_info in current_target_files]
        # current_target_files = Park4139List.get_nested_list_sorted_by_column_index(nested_list=current_target_files, column_index=1, decending_order=True)
        # current_target_files = Park4139List.get_list_seperated_by_each_elements_in_nested_list(current_target_files)  # from [["a","b"], ["c","d"]] to ["a", "b", "c", "d"]
        # current_target_files = Park4139List.get_list_each_two_elements_joined(current_target_files)  # from ["a", "b", "c", "d"] to ["ab", "cd"]
        # abspaths_and_mtimes = "\n".join(abspaths_and_mtimes)  # list to str
        # current_directory_state = "\n".join([f"{key}: {value}" for key, value in current_directory_state])  # list to str ([tuple] to str) (개행된 str)
        # current_directory_state = current_directory_state.split("\n")  # str to [str] (개행된 str)
        # current_directory_state = sorted(current_directory_state.items(), key=lambda item: item[1], reverse=True)  # dict to [tuple] (딕셔너리를 value(mtime)를 기준으로 내림차순으로 정렬), 날짜를 제일 현재와 가까운 날짜를 선택하는 것은 날짜의 숫자가 큰 숫자에 가깝다는 이야기이다. 그러므로  큰 수부터 작은 수의 순서로 가는 내림차순으로 정렬을 해주었다(reverse=True).
        # current_directory_state = "\n".join(current_directory_state)  # list to str ([str] to str)
        # current_directory_state = sorted(current_directory_state.items(), key=lambda item: item[0]) # dict to [tuple] (딕셔너리를 key를 기준으로 오름차순으로 정렬)

        # current_directory_state = sorted(current_directory_state.items(), key=lambda item: item[1]) # dict to [tuple] (딕셔너리를 value를 기준으로 오름차순으로 정렬)
        # current_directory_state = sorted(current_directory_state, key=lambda item: item[2])  # tuple 2차원 배열의 특정 열의 오름차순 정렬, # 람다의 쉬운 예로 볼 수 있겠다.
        # current_directory_state = {key: value for key, value in current_directory_state} # list to dict
        # dict to list (리스트 내의 파일목록의 순서를 파일변경일순으로 변경) ,  람다는 익명함수이며, return 형태도 같이 작성한다,  은 호출은 lambda_function(current_directory_state),  정의는 lambda_function(item), reuturn item[2] 이런 느낌이다
        # current_directory_state = "\n".join([f"{key}: {value}" for key, value in current_directory_state.items()])  # dict to str (개행을 시킨)
        # def _get_processed_abspaths_and_mtimes(abspaths:[str], mtimes:[str]):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        #     # 비동기 처리 설정 ( advanced  )
        #     import threading
        #     nature_numbers = [n for n in range(1, 101)]  # from 1 to 100
        #     work_quantity = len(abspaths)
        #     n = 15  # thread_cnt # interval_cnt # success
        #     n = 5  # thread_cnt # interval_cnt # low load test
        #     d = work_quantity // n  # interval_size
        #     r = work_quantity % n
        #     start_1 = 0
        #     end_1 = d - 1
        #     starts = [start_1 + (n - 1) * d for n in nature_numbers[:n]]  # 등차수열 공식
        #     ends = [end_1 + (n - 1) * d for n in nature_numbers[:n]]
        #     remained_start = ends[-1] + 1
        #     remained_end = work_quantity
        #
        #     print(rf'nature_numbers : {nature_numbers}')  # 원소의 길이의 합이 11넘어가면 1에서 3까지만 표기 ... 의로 표시 그리고 마지막에서 3번째에서 마지막에서 0번째까지 표기 cut_list_proper_for_pretty()
        #     print(rf'work_quantity : {work_quantity}')
        #     print(rf'n : {n}')
        #     print(rf'd : {d}')
        #     print(rf'r : {r}')
        #     print(rf'start_1 : {start_1}')
        #     print(rf'end_1 : {end_1}')
        #     print(rf'starts : {starts}')
        #     print(rf'ends : {ends}')
        #     print(rf'remained_start : {remained_start}')
        #     print(rf'remained_end : {remained_end}')
        #
        #     abspaths_and_mtimes____ = []
        #
        #     # 비동기 이벤트 함수 설정 ( advanced  )
        #     async def is_containing_special_characters(start_index: int, end_index: int):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        #         abspaths_and_mtimes = Park4139List.get_list_added_elements_alternatively(abspaths[start_index:end_index], mtimes[start_index:end_index])  # from [1, 2, 3] + [ x, y, z] to [1, x, 2, y, 3, z]
        #         abspaths_and_mtimes_ = Park4139List.get_nested_list_grouped_by_each_two_elements_in_list(abspaths_and_mtimes)  # from ["a", "b", "c", "d"] to [["a","b"], ["c","d"]]
        #         abspaths_and_mtimes__ = Park4139List.get_nested_list_sorted_by_column_index(nested_list=abspaths_and_mtimes_, column_index=1, decending_order=True)
        #         abspaths_and_mtimes___ = Park4139List.get_list_seperated_by_each_elements_in_nested_list(abspaths_and_mtimes__)  # from [["a","b"], ["c","d"]] to ["a", "b", "c", "d"]
        #         abspaths_and_mtimes____[start_index:end_index] = Park4139List.get_list_each_two_elements_joined(abspaths_and_mtimes___)  # from ["a", "b", "c", "d"] to ["ab", "cd"]
        #
        #     # 비동기 이벤트 루프 설정
        #     def run_async_event_loop(start_index: int, end_index: int ):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        #         loop = asyncio.new_event_loop()
        #         asyncio.set_event_loop(loop)
        #         loop.run_until_complete(is_containing_special_characters(start_index, end_index))
        #
        #     # 스레드 객체를 저장할 리스트 생성
        #     threads = []
        #
        #     # 주작업 처리용 쓰레드
        #     for n in range(0, n):
        #         start_index = starts[n]
        #         end_index = ends[n]
        #         thread = threading.Thread(target=run_async_event_loop, args=(start_index, end_index))
        #         thread.start()
        #         threads.append(thread)
        #
        #     # 남은 작업 처리용 쓰레드
        #     if remained_end <= work_quantity:
        #         start_index = remained_start
        #         end_index = remained_end
        #         thread = threading.Thread(target=run_async_event_loop, args=(start_index, end_index))
        #         thread.start()
        #         threads.append(thread)
        #     else:
        #         start_index = remained_start
        #         end_index = start_index  # end_index 를 start_index 로 하면 될 것 같은데 테스트필요하다.
        #         thread = threading.Thread(target=run_async_event_loop, args=(start_index, end_index))
        #         thread.start()
        #         threads.append(thread)
        #
        #     # 모든 스레드의 작업이 종료될 때까지 대기
        #     for thread in threads:
        #         thread.join()
        #
        #     TestUtil.pause()
        #     return abspaths_and_mtimes

        # lzw 알고리즘으로 문자열 압축부터 해야할듯... 10개 샘플 넣었는데 암호문의 길이가 1744자 나왔음....

        # 트라이 구조 유사하게 텍스트 교체 시도
        # Park4139PerformanceHandler.gen_dictionary_for_monitor_target_edited_and_bkup(directory_abspath= directory_abspath)
        # TestUtil.pause()

        # 5만줄을 쓰레드로 나누어 처리, 너무 느리다.
        # 1개의 큰 메인쓰레드를 여러개의 쓰레드로 나누어 처리한다고 보면된다
        import threading
        # 스레드로 처리할 작업량 분배 2개 쓰레드로 쪼갬
        # (스레드로 처리할 작업량) =  2 * (스레드로 처리할 작업량//2) + (스레드로 처리할 작업량%2)
        # len(lines) =  threads_cnt * (len(lines)//threads_cnt) + (len(lines)%threads_cnt)
        # 54234 =  2 * (54234//2) + (54234%2)
        # d = interval = (len(lines)//threads_cnt)
        # n = index
        sample = [i for i in range(0, 50000)]
        work_qunatity = len(sample)  # lines
        # lines = [i for i in range(0, 54233)]
        n = 10  # thread_cnt # interval_cnt
        d = work_qunatity // n
        r = work_qunatity % n
        # [시작지점_1, 시작지점_2, ...]
        # [시작지점_n, 시작지점_n]
        # [시작지점_1 + (n - 1)d, 시작지점_1 + (n - 1)d]
        # [start_1 + (n - 1)d, start_1 + (n - 1)d]
        # [start_1 + (1 - 1)d, start_1 + (2 - 1)d]
        # [0 + (1 - 1)d, 0 + (2 - 1)d]
        # starts = [a_n for a_n in range(0, n)]
        # a_n = start_1 + (n - 1) * d
        # starts = [a_n for n in range(0, n)]
        nature_numbers = [n for n in range(1, 101)]  # 수학과 프로그래밍을 연결해 사용해보자
        # start_1 = start_1 + (n - 1) * d
        # a_2 = start_1 + (n - 1) * d
        # a_3 = start_1 + (n - 1) * d
        start_1 = 0  #
        end_1 = d - 1
        starts = [start_1 + (n - 1) * d for n in nature_numbers[:n]]  # 등차수열 공식
        ends = [end_1 + (n - 1) * d for n in nature_numbers[:n]]
        remained_start = ends[-1] + 1
        remained_end = work_qunatity

        print(rf'nature_numbers : {nature_numbers}')
        print(rf'work_qunatity : {work_qunatity}')
        print(rf'n : {n}')
        print(rf'd : {d}')
        print(rf'r : {r}')
        print(rf'start_1 : {start_1}')
        print(rf'end_1 : {end_1}')
        print(rf'starts : {starts}')
        print(rf'ends : {ends}')
        print(rf'remained_start : {remained_start}')
        print(rf'remained_end : {remained_end}')

        # 표수식으로 보는 수학
        # 수식을 표로보면 이해가 잘간다
        # 숫자는 수열과 행렬로 보는게 좋다.
        # 등분 알고리즘 은 작업량이 짝수에서는 딱 떨어지는 방법이다, 홀수에서는 나머지가 발생한다.
        # 작업량 10 개를 5구간으로 나누면
        # 10 = 5 * 2         + 0
        # 10 = 5 * (10 // 5) + (10 % 5)
        #
        # 30000 =  5* 6000        + 1
        # 30000 =  5* (30000//5)  + (30000%5)
        #
        # 54234 = 5 * 10846        + 0.8
        # 54234 = 5 * (54234//5) + (54234%5)
        #
        # # 작업량 54234 개를 5구간으로 나누면
        # 1구간 0   10846 *1 = 10846
        # 2구간 0   10846 *2 = 21692
        # 3구간 0   10846 *3 = 32538
        # 4구간 0   10846 *4 = 43384
        # 5구간 0   10846 *5 = 54230
        # 나머지구간         = 54234
        #
        # 모든 구간의 인터벌은 10846 이다.
        # 나머지구간의 인터벌은 4 이다.
        #
        # 시작지점 = [1    ]
        # interval = [10846 10846 10846 10846 10846 10846]
        # 종료지점 = [10846]
        #
        # 시작지점 = [0     ]
        # interval = [10846 10846 10846 10846 10846 10846]
        # 종료지점 = [10846-1]
        #
        # 시작지점 = [start_1  a_2  a_3 a_4  a_5  ]
        # interval = [10846 10846 10846 10846 10846 10846]
        # 종료지점 = [e_1  e_2  e_3 e_4  e_5  ]

        # 등차수열의 관계식
        # start_1 = 0       = start_1 + (n - 1)d = 0   + (1 - 1)10846 = 0
        # a_2 = start_1 + d = start_1 + (n - 1)d = 0   + (2 - 1)10846 = ?
        # a_3 = a_2 + d = start_1 + (n - 1)d
        # a_4 = a_3 + d = start_1 + (n - 1)d
        # a_n = start_1 + (n - 1)d
        #
        # a_n = start_1 + (n - 1)d = ?
        #
        # 문제
        # a_5 = ?
        # a_5 = start_1 + (n - 1)d = 0 + (5 - 1)10846 = ?
        # a_54234 = ?
        # a_54234 = start_1 + (n - 1)d = 0 + (54234 - 1)10846 = ?
        #
        # a_5 = ? 가 질문이면 "=" 대신에  "= 공식 =" 으로 대체한다.
        # a_5 = 공식 = ? 를 두고 풀어본다.
        # a_54234 = ? 가 질문이면  "=" 대신에  "= 공식 =" 으로 대체한다.
        # a_54234 = start_1 + (n - 1)d = ?
        # 일반적인 문제라면 start_1, n, d 에 대해서 주어질 것이다.
        # 이 3개의 요소중 1개라도 주어지지 않는다면 이 문제는 이 방법으로 풀 수 없다.

        # # 각 스레드의 결과를 저장할 리스트
        # result_list = [None] * len(abspaths_and_mtimes)
        #
        # def process_work_divided(start_index, end_index):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        #     # 예약된 단어 맵으로 암호화
        #     for index, abspaths_and_mtime in enumerate(abspaths_and_mtimes[start_index:end_index], start=start_index):
        #         tmp = Park4139Performance.dictionary_for_monitoring_performance.items()
        #         for key, value in tmp:
        #             if key in abspaths_and_mtime:
        #                 abspaths_and_mtimes[index] = abspaths_and_mtime.replace(key, value)
        #                 # result_list[index] = abspaths_and_mtime.replace(key, value)
        #     print(f"쓰레드 {start_index}에서 {end_index}까지 작업 완료")
        #
        # threads = []  # 스레드로 처리할 작업 리스트
        #
        # # 주작업 처리용 쓰레드
        # for n in range(0, n):
        #     start_index = starts[n]
        #     end_index = ends[n]
        #     thread = threading.Thread(target=process_work_divided, args=(start_index, end_index))
        #     thread.start()
        #     threads.append(thread)
        #
        # # 남은 작업 처리용 쓰레드
        # start_index = remained_start
        # end_index = remained_end
        # thread = threading.Thread(target=process_work_divided, args=(start_index, end_index))
        # thread.start()
        # threads.append(thread)
        #
        # # 모든 스레드의 작업이 종료될 때까지 대기
        # for thread in threads:
        #     thread.join()

        # AES 암호화
        # key: bytes = b'0123456789abcdef'  # AES 키 설정 (16바이트 - 128비트)
        # plaintext: bytes = abspaths_and_mtimes.encode('utf-8')  # str to bytes  # 문자열을 UTF-8로 인코딩하여 바이트 코드로 변환
        # ciphertext = Park4139CipherUtil.aes_encrypt(key, plaintext)  # bytes to bytes
        # print(rf'ciphertext : {ciphertext}')
        # print(rf'type(ciphertext) : {type(ciphertext)}')
        # print(rf'len(ciphertext) : {len(ciphertext)}')

        # 복호화
        # decrypted_text = Park4139CipherUtil.aes_decrypt(key, ciphertext)
        # print("복호화 결과")
        # print(rf'decrypted_text.decode() : {decrypted_text.decode()}')
        # print(rf'type(decrypted_text.decode()) : {type(decrypted_text.decode())}')
        # print(rf'len(decrypted_text.decode()) : {len(decrypted_text.decode())}')

        # bytecode: bytes = b'\x48\x65\x6c\x6c\x6f'  # 예시로 바이트 코드 생성
        # string: str = bytecode.decode('utf-8')  # bytes to str

        # current_directory_state = "foo"

        # copy_path = str(input('copy_path: '))  # 복사할 폴더 위치
        # paste_path = str(input('paste_path: '))  # 저장될 폴더 위치

        # 매크로 프로그램
        # F1 녹화시작
        # F1 녹화종료
        # F1 재생
        # F1 에 다시 녹화를 시작할까요?
        #
        #
        #
        #
        # 오늘의 파이썬 에러
        # EvtSubscribeActionDeliver
        # EvtSubscribeActionDeliver
        # EvtSubscribeActionDeliver
        # EvtSubscribeActionDeliver
        # EvtSubscribeActionDeliver
        # EvtSubscribeActionDeliver
        # EvtSubscribeActionDeliver
        # EvtSubscribeActionDeliver
        # EvtSubscribeActionDeliver
        # EvtSubscribeActionDeliver
        # EvtSubscribeActionDeliver
        # EvtSubscribeActionDeliver
        # EvtSubscribeActionDeliver
        # EvtSubscribeActionDeliver
        # EvtSubscribeActionDeliver
        # EvtSubscribeActionDeliver
        # EvtSubscribeActionDeliver
        # EvtSubscribeActionDeliver
        # EvtSubscribeActionDeliver
        # 이건 뭔가. 처음 마주하는 새로운 에러이다
        # python 콘솔에 줄줄이 인쉐되어 나오는 단어다
        # 하나씩 트러블 슈팅을 하니 로컬 패키지에서 나는 에러이다
        # import 만 해도 나는 걸 보니 어디서나는지...
        # 일단 오늘 작업한 함수들만 주석해보자 못 찻겠다
        # 일단 로컬백업 수행
        # 구글링하니 windows 관련 내용 주르륵 나와
        # 확실히 이 에러가 없던 로컬백업을 열어본다
        # archive_py - 2023 12 27 23 58 02 - 복사본
        # 만약 여기서 나오면 프로젝트 문제 아니고 윈도우즈 문제...
        # 잉? archive_py - 2023 12 27 23 58 02 - 복사본 여기서 안난다.
        # 내가 프로젝트를 잘못 건드렸다는 것 같은데 어디냐
        # 뭐지 가상환경이 날아가 벼렸는데? 몇 번 다시봐도 없음.
        # freeze 시켜둔 가상환경을 설치시도하기 전에 근래 로컬백업 하나만 더보자. 와 이것도 없다.
        # 윈도우 리부팅 했는데도 나타나는 것이다.
        # IDE 문제일 수도 있으니 초기화 해보자.
        # 커밋 주기를 이번엔 길게 했는데 하아..
        # 의심사항 하나 찾음
        # # from PySide6.QtCore import Qt, QTimer, QThread, Signal, QObject, QCoreApplication
        # import 부분 주석처리 실행을 번갈아 몇번하니 사라졌다? 어쨋든 사라졌는데?
        # 문제가 있을 법한 부분은 같은 패키지가 여러개 import 되어 있던 부분이 있었다.
        # 이건 overwrite 되는 것처럼 동작하리라 생각하여 문제 없을 것이라 판단하고 귀찮아서 나중에 일괄정리하려고 둔 부분이었는데
        # import 부분 전체 백업해두고 Jetbrain IDE의 ctrl alt o 를 눌러주었다
        # 실행한번 눌러보고 오케이 되었어
        # 프로젝트 로컬백업수행완료
        # 혹시 이런게 문제가 될 수도 있어 보인다.
        #
        #
        #
        # 오늘의 파이썬 에러
        # 'test': opts.should_i_start_test_core,
        # 이게 뭔줄 아는가? yt_dlp 모듈의 파일 중 하나인데
        # should_i_start_test_core 라고 내가 리펙토링을 마구하다가 다른 패키지를 건드려
        # 문제가 된 부분이다. 유의해서 IDE 의 리펙토링을 하자
        # 이 부분은 다행히 내가 특징적으로 기억을 했기에 망정이지. 몰랐을 거다.
        #
        #
        #
        # 프로젝트 로컬 백업 버튼 만들기
        #
        # mp3 사용일자별로 정리를 해서 한번 지우자
        #
        # 다마고치 게임, 바탕화면에서 디지털몬스터 키우는 게임.
        #
        #
        #
        # 파일변경감지 아이디어
        # (이것 git으로 할 수 있잖아!)
        # 감지이벤트를 걸어 파일변경감지 시 비동기 빽업처리... 아 git 설치 안되있으면 안됨.

        # 파일명 대체 기능 (불필요한 접두/어근/접미, 삭제/추가)
        # 이름에 [subplease] 가 있다면
        # rename_without_overwrite(이름, 이름.replace([subplease],""))
        # 필요한 파일명 부여 삭제
        # rename_target_without_overwiting(current, future)
        # 이동시키지 말고 그자리에서 rename

        # 2024 PROJECT DATA PRISION
        # 내가 아는 것은 30초 이내에 찾을 수 있도록 하기 위한 프로젝트
        # 결국 보고자 하는 것은 디렉토리가 아니라 파일명을 잘 관리해서 인덱싱하면 된다고 생각한다.
        # 디렉토리명은 파일을 찾기 위한 지표정도이다.
        # 파일이 어느폴더에 있든 상관없다. 단지 이름명이 류가 되어있어 찾을 때, 정확히 호출만 되면 되는 일이다. 호출명단을 잘 관리를 하면 되는 일이다,
        # 그렇다면 실제파일을 정리할 필요가 없다, 즉 찾는시간이 적은 시스템이 필요한 것이지 정리하는시간이 필요한 게 아니다
        # 정리하는시간이 없고, 찾는시간이 빠른 시스템 이 나에게 필요한 파일색인시스템.
        # 떠오른 단점은 파일명이 변경되면 안된다.
        # 모든 파일명을 가져온다. 모든 파일명은 nick name 으로 최대한 관리한다. nick name 이 없다면 파일명을 표기한다. 파일명에서 어떤 컨텐츠인지 모른다면. 알기위해서 실행하거나 열어볼 수 밖에 없다
        # get filenames
        # organize
        # 인덱스를 파일명 유사도분류로

        # (파일명)   #hashtag name #애니 #영화
        # 파일명 부여 규칙
        # 접두사는 가장 중요한 직관적인 키워드를 넣는다.
        # 접미사는 순서에 관계없이 #애니 #영화 이런 걸 붙인다. 이 접미사는 검색 시 중요하므로 잘 보관하고 관리한다.
        # 파일명으로 가지고 파일을 검색한다.

        # 빈폴더 머지는 확실히 삭제해도 되는 빈폴더를 한 폴더에 두고 빈폴더 삭제 명령어로 처리하자

        # def prisonize_storage():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")

        # 나중에 TDD 공부를 해볼 것.
        # 파일 변화 확인 로직 필요.
        # 파일 읽어와서 전체 자리수가 바뀌면 파일 변화 한 것으로 보면 된다. 완벽하진 않아도 대부분 해소
        # git으로 관리되는 프로젝트이면 git으로도 확인 가능

        # PEP8
        # PEP8 은 파이썬 코드의 작성에 대한 표준권장규칙 정도로 나는 생각한다.
        # recommand to apply naming convention to code
        #
        # naming convention
        # 코드작성용 용어사용 규칙 정도로 나는 생각한다.
        #
        # PEP8 에 의거해서 내 코드 분석하기
        # 지켜지지 않은 부분
        # - 권장줄길이 79 : 나는 간단한 건 한줄로...웬만한건 한줄로 작성했고 최대 180 자 정도까지는 작성했다...
        # - 주석용법 : 코드자체에 대한 설명이 아닌 코드의 의도를 설명해야한다고 하는데 코드자체의 설명을 작성함.. 상당히 지켜가기 어렵다. 네이밍센스가 좋게 작성된 경우라면 지킬 수 있겠지만 다음에 다시봐도 이해가 안갈 네이밍센스로 작성된 코드라면 코드자체 설명을 주석으로 또 달 것 같다. 노력은 해야겠다.
        # - 파이썬 메소드 함수 대소문자 :
        # - 상수명 : 어떤건 소문자로 되어있는데...모두 대문자여야 함 : FILE_ABSPATH = "blah\blah\foo\foo"
        # - import 순서 : 나중에 내 import 부분 코드를 정리해봐야겠다. import 표준라이브러리모듈, import 서드파티모듈, import 로컬모듈 , 요 순서라고 하는데 몰랐다. 아 하나더 있는 규칙이, 알파벳순서 로 나열할 것. vscode 로 line sort 해야 겠다.
        # - import 는 필요한 것만 : 세부적으로 그 모듈에 특정 함수, 객체만 필요한 경우 딱 꼬집어 그것만 import 해야한다.
        # - ' 또는 " 로 일관된 사용 권장 : 지켜지기 어려울 것 같다. 그 이유는 나는 f-string 문법으로 포멧팅을 즐겨 사용하는데... string escaping을 위해서 ' 과 " 의 혼용은 필 수이다.
        # - 한줄에 여러코드를 작성 시 ; 로 구분권장 : 여러코드를 한줄로 구동하도록 시도한 적이 있는데 그 때 ; 로 구분이 되었었다는 것이 떠올랐다. 모르고 쓴 건데 이번에 알았다,
        # - ; 를 사용할 것을 권장하지 않음 : 가독성을 위해서 여러줄로 작성하고 ;를 웬만하면 쓰지 말아야겠다, 나도 공감 ; 를 쓰면 코드를 읽기 어려웠다.

        # 지켜진 부분
        # - 클래스명 : class RpaProgramWindow(QWindow):
        # - 함수, 메소드명 : def love_you():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        # - import 중 이름충돌 예상 시 as 사용 : 충돌의 소지가 있을 때 as 를 썻다. PEP8을 알고 지킨건 아니고 jetbrain IDE 의 가이드기능을 잘 따르다 보니, 잘 지켜졌다. : import blahblah as blah

        # 국내주식과 미국주식을 크롤링해서 보고 싶어졌다.
        # 몇 가지 라이브러리가 있음을 확인했고 기획하는 중이다.
        # 데이터수집장소 : 다양한 웹사이트에서 크롤링하여 데이터를 수집하기로 생각하였다, 신뢰도가 높아보이는 데이터를 수집해야 한다
        # 데이터신뢰도판단 : 네이버 금융정보 데이터신뢰도가 높다고 판단한 이유는 타블로그에서 정보를 얻었으며, 여러 이유 중 가장 큰 이유는 네이버의 공인력을 내가 믿기때문이다.)
        # 데이터수집방식 : 특정데이터는 네이버에서 직접 크롤링할 것. 웹 크롤링도 약간 늘었고, 데이터를 엑셀의 형태로 핸들링 하기 위해서 pandas 배워야 겠다. 잠깐만 기다려라 배워서 다시 오겠다.
        # import pykrx # 국내증권데이터 공유 라이브러리, 네이버금융사이트(실시간수정되는 주식데이터), 한국증권사이트 의 데이터 기반, 고신뢰성데이터 인 국내주식정보 를 볼 수 있다.  pykrx의 특징은 국내 주식만 수집이 가능한대신 yfinance보다 국내주식 시세가 정확하고 PER, PBR, 배당수익률과 같은 지표는 신뢰성이 떨어진다 - 출처: https://bigdata-doctrine.tistory.com/7 [경제와 데이터:티스토리]
        # import yfinance # 증권데이터 공유 라이브러리, 야후 파이낸스에서 크롤링한 데이터를 제공하는 라이브러리, 미국주식데이터 는 상대적으로 정확 , 국내주식데이터 의 잦은누락,   결론은 다른게 나아보인다.

        # 나의 가치는 "있어 보이는 척 말고 해본 것" 에서 온다고 믿는다.
        # 그만큼 해보려면 시간을 쏟아 부어야 한다는 주변의 어느 개발자의 말씀도 있었다
        # comprehensive input 에 대해서 집중하여 작성, 내가 이해한 만큼만 작성을 하자

        # 그동안 나는 주관이 나쁜 것이란 착각에 빠져 생각을 하는 방법을 몰랐던 것 같다.
        # 내 생각을 갖는 시간이 중요하다라는 것을 깨달았다.

        # 까먹으면 기록에서 찾는다. 이 때 그 기록은 기록 시스템으로 되어 있어야 한다.
        # 인덱싱하여 빠르게 찾아야 그 기록은 가치가 있다
        # 기록을 검색할 때에는 텍스트를 작성하게 된다, 그 텍스트는 기록에 반드시 포함되어야 한다, 이 텍스트는 기록내용에 중복 작성이 가능하다.
        # 해시태그를 활용한 기록을 하여 내가 내 기록을 찾는 검색에 있어서 노출이 활률을 높이자.

        # 그동안 텍스트를 외운 것을 이해한다고 착각한 것 같다.
        # 항상 실험하고 실험결과에서 얻은 통찰을 풀어서 생각하자.
        # 논리는 풀어서 이해해야 한다.
        # 나는 엄청 메모를 많이 하는 편이지만 이 메모에 너무 의존한 것 같다.
        # 그 의존 때문에 그 동안 깊게 생각해보는 시간을 많이 갖지 않았던 것 같다.
        # 나에겐 메모하는 시간은 줄이고 이해하기 위해 실험과 그에 의거한 통찰로 생각 해보는 시간을 더 갖도록 해야 겠다.

        # import plotly # 대표적인 인터랙티브 시각화 도구
        # print(plotly.__version__)
        # plotly 오프라인 graph 플로팅 어찌 합니까?
        # Candlestick chart를 그려낼것.
        # 주피터 노트북으로 하는 방법이 나오는데 나는 주피터 노트북 말고 pyside6 를 활용해서 ui에 띄우거나 웹에 띄우고 싶다.
        # import plotly.express as px
        # df = px.data.iris()
        # fig = px.scatter(df, x="sepal_width", y="sepal_length", color='petal_length')
        # fig.show()
        # df = px.data.stocks()
        # df

        # interface 에 관하여
        # high-level interface : 기계보다 사람에 더 가까운 인터페이스, 이 말은 CLI 보다 GUI 로 가는 이유를 설명하는 근거지 않을까 싶은데.
        # 많은 설정을 해야하는 겨우라면 나는 CLI 를 더 선호한다.

        # api 에 관하여
        # program 간 program 이다. 프로그램들 사이에 위치한 프로그램으로서 통신중계 역할을 주로 한다. api 라 부르는 것은 통신 기능이 들어있기 마련이다

        pass

    except SystemExit:  # sys.exit() 호출을 의도적으로 판단
        pass
    except:
        DebuggingUtil.trouble_shoot("%%%FOO%%%")
        traceback.print_exc(file=sys.stdout)
        TestUtil.pause()


@TestUtil.measure_seconds_performance_nth
def crawl_finance_data_via_fdr():
    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
    # __________________________________________________________________________________________________________________________________
    # import plotly.express as px
    # pip install kaleido
    import FinanceDataReader as fdr  # 주가 변화에 대한 실시간 데이터를 제공하지 않음, 나는 주가 변화에 대한 고빈도 실시간 데이터를 원하므로 다른 대안 필요.

    # 거래소상장주식코드목록 via StockListing()
    # df = fdr.StockListing(market='SSE')  # 상해
    # df = fdr.StockListing(market='SZSE')
    # df = fdr.StockListing(market='KRX-DESC') # fail
    df = fdr.StockListing(market='KRX')  # 대한민국 거래소 , KOSPI+KOSDAQ+KONEX
    # df = fdr.StockListing(market='KOSPI')
    # df = fdr.StockListing(market='NYSE')  # 뉴욕거래소 # 뉴욕주식거래소  # 뉴욕 스탁 익스체인지
    # df = fdr.StockListing(market='S&P500')
    # df = fdr.StockListing(market='NASDAQ')
    # 데이터 클렌징
    # df  = df[df["Name"] == "삼성전자"] # success
    # df  = df[df["Name"].str.contains("삼성전자")] # success
    df = df[df["ChangeCode"] == "1"]  # success, 오늘 양봉,
    # df = df[df["ChangeCode"] == "2"]  # success, 오늘 음봉
    df = df[3 <= df["ChagesRatio"]]  # success, 오늘 3프로 이상 간 것
    DebuggingUtil.print_magenta(rf'''df.columns : {df.columns}''')  # 헤더 컬럼명 제어
    # df = df[['Name', 'Code', 'ChagesRatio']]  # 컬럼들 제어
    # df = df[['Code', 'ISU_CD', 'Name', 'Market', 'Dept', 'Close', 'ChangeCode','Changes', 'ChagesRatio', 'Open', 'High', 'Low', 'Volume', 'Amount','Marcap', 'Stocks', 'MarketId']]
    df = df[['Code', 'Name', 'Market', 'ChangeCode', 'ChagesRatio', 'Open', 'High', 'Low', 'Close', 'Volume', 'Amount', 'Stocks', 'Marcap']]
    # df  = df[df["Name"].str.contains("삼성전자|하이닉스")] # success
    # df = df[df["Name"].str.contains("삼성") & df["Name"].str.contains("전자")]
    # df = df.head(1)  # 레코드들 개수 제어
    # df = df.head(10)
    # df = df.head(20)
    # df = df.head(100)
    df = df.sort_values('ChagesRatio', ascending=False)  # 레코드들 순번 제어
    # df = df.sort_values('Stocks', ascending=False) # 'Stocks': 주식의 총 개수. 발행된 주식의 총 개수. 총 상장 주식수는 해당 종목의 주식이 시장에 총 몇 주가 상장되어 있는지를 나타내며, 기업의 규모와 주식 시장에서의 유동성을 판단하는데 사용됩니다.
    # df = df.sort_values('Marcap', ascending=False) # 'Marcap': 시가총액(Market Capitalization), Marcap = stocks * 주가(close), 해당 종목의 모든 주식이 현재 시장에서 평가받는 총 가치를 의미합니다. 시가총액은 주식 시장에서 기업의 크기와 가치를 판단하는 지표.
    # df = df.sort_values('Volume', ascending=False) # 'Volume': 당일의 주식의 총수 변화량, 매수총수 + 매도총수, 활발한 거래를 나타내는 지표
    # df = df.sort_values('Amount', ascending=False) # 'Amount': 당일의 주식의 거래량 Amount = Volume * 주가(Close), 활발한 거래를 나타내는 지표
    DebuggingUtil.print_magenta(rf'''df : {df}''')
    DebuggingUtil.print_magenta(rf'''len(df) : {len(df)}''')

    fig = ff.create_table(df)
    fig.show()


# @TestUtil.measure_seconds_performance_nth
def update_ticker_xlsx():
    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
    # __________________________________________________________________________________________________________________________________
    # import FinanceDataReader as fdr
    # import pandas as pd
    # import plotly.express as px
    # # pip install kaleido
    # from PySide6.QtCore import QCoreApplication
    # from PySide6.QtWidgets import QApplication
    import FinanceDataReader as fdr  # 주가 변화에 대한 실시간 데이터를 제공하지 않음, 나는 주가 변화에 대한 고빈도 실시간 데이터를 원하므로 다른 대안 필요.
    import pandas as pd

    # 데이터 업데이트 주기가 매 프로그램 시작마다인 데이터 처리(stock ticker or stock id , stock name)
    # 데이터 업데이트가 하루 주기여도 되는 데이터만 선정, 데이터 업데이트 주기가 매 프로그램 시작마다인 현재 방식을 DB 에 데이터를 넣어 불러오는 방식으로, 데이터 업데이트 주기를 한달 주기로 변경 예정.
    # __________________________________________________________________________________________________________________________________
    # 한국주식
    # df_krx에 저장
    # 거래소상장주식코드목록 via StockListing()
    market = 'KRX'  # 대한민국 거래소 , KOSPI+KOSDAQ+KONEX
    # market='KOSDAQ'
    # market='KOSPI'
    # market='KONEX' # 코넥스
    DebuggingUtil.print_magenta(f'market : {market}')
    df = pd.DataFrame()
    try:
        df = fdr.StockListing(market=market)
    except Exception:
        print("다운로드가 멈췄음")
    # DebuggingUtil.print_magenta(f'df : \n{df}')
    # DebuggingUtil.print_magenta(rf'type(df) : {type(df)}')
    # DebuggingUtil.print_magenta(rf'len(df) : {len(df)}')
    # 데이터 클렌징
    # DebuggingUtil.print_ment_magenta(rf'''df.columns : {df.columns}''')  # 헤더 컬럼들 제어
    # df  = df[df["Name"].str.contains("삼성전자|하이닉스")]
    # df = df[df["Name"].str.contains("삼성") & df["Name"].str.contains("전자")]
    # df  = df[df["Name"] == "삼성전자"]
    # df  = df[df["Name"].str.contains("삼성전자")]
    # df = df[df["ChangeCode"] == "1"]  # 오늘 양봉,
    # df = df[df["ChangeCode"] == "2"]  # 오늘 음봉
    # df = df[3 <= df["ChagesRatio"]]  # 오늘 3프로 이상 간 것
    df = df.sort_values('Code', ascending=False)  # 레코드들 순번 제어
    df = df[['Code', 'Name', 'Market']]
    # df = df.head(1)
    # df = df.head(10)
    # df = df.head(20)
    # df = df.head(100)
    # df = df.sort_values('Stocks', ascending=False) # 'Stocks': 주식의 총 개수. 발행된 주식의 총 개수. 총 상장 주식수는 해당 종목의 주식이 시장에 총 몇 주가 상장되어 있는지를 나타내며, 기업의 규모와 주식 시장에서의 유동성을 판단하는데 사용됩니다.
    # df = df.sort_values('Marcap', ascending=False) # 'Marcap': 시가총액(Market Capitalization), Marcap = stocks * 주가(close), 해당 종목의 모든 주식이 현재 시장에서 평가받는 총 가치를 의미합니다. 시가총액은 주식 시장에서 기업의 크기와 가치를 판단하는 지표.
    # df = df.sort_values('Volume', ascending=False) # 'Volume': 당일의 주식의 총수 변화량, 매수총수 + 매도총수, 활발한 거래를 나타내는 지표
    # df = df.sort_values('Amount', ascending=False) # 'Amount': 당일의 주식의 거래량 Amount = Volume * 주가(Close), 활발한 거래를 나타내는 지표
    df_krx = df
    # DebuggingUtil.print_ment_magenta(rf'''df_krx : {df_krx}''')
    DebuggingUtil.print_magenta(rf'''len(df_krx) : {len(df_krx)}''')
    # fig = ff.create_table(df_krx)
    # fig.show()
    # __________________________________________________________________________________________________________________________________
    # 미국주식
    # df_usa에 저장
    # market='NYSE'  # 뉴욕거래소
    # market='S&P500'
    market = 'NASDAQ'
    DebuggingUtil.print_magenta(f'market : {market}')
    try:
        df = fdr.StockListing(market=market)
    except Exception:
        print("다운로드가 멈췄음")
    # 데이터 클렌징
    # DebuggingUtil.print_ment_magenta(rf'''df.columns : {df.columns}''')  # 헤더 컬럼들 제어
    # df = df[['Symbol', 'Name', 'IndustryCode', 'Industry']]
    # df  = df[~df["IndustryCode"].str.contains("63101010|63102010")] # ~ 연산자로 제외할 수 있다.
    # df  = df[df["Name"] == "NVDA"]
    # df  = df[df["Name"].str.contains("NVDA|AAPL|META|AMZN")]
    df = df.sort_values('IndustryCode', ascending=True)  # NASDAQ Industry 분류 순으로 정렬, 테마별로 보는데 유용할 것으로 기대
    df = df[['Symbol', 'Name']]
    # df = df.head(1)
    # df = df.head(10)
    # df = df.head(20)
    # df = df.head(100)
    df_usa = df
    # DebuggingUtil.print_ment_magenta(rf'''df_usa : {df_usa}''')
    DebuggingUtil.print_magenta(rf'''len(df_usa) : {len(df_usa)}''')
    # fig = ff.create_table(df_usa)
    # fig.show()
    # __________________________________________________________________________________________________________________________________
    # 미국ETF
    market = 'ETF/US'
    DebuggingUtil.print_magenta(f'market : {market}')
    df = None
    try:
        df = fdr.StockListing(market=market)
    except Exception:
        print("다운로드가 멈췄음")
    # 데이터 클렌징
    # DebuggingUtil.print_ment_magenta(rf'''df.columns : {df.columns}''')  # 헤더 컬럼들 제어
    # df = df[['Symbol', 'Name', 'IndustryCode', 'Industry']]
    # df  = df[df["Symbol"] == "TQQQ"]
    # df = df[~df["Symbol"].str.contains("IWM|LQD")]  # ~ 연산자, 비관심종목 제외 설정에 유용, 짧은 심볼을 작성 시 긴 심볼도 삭제될 수 있으니 유의해야함.
    # df  = df[df["Symbol"].str.contains("TQQQ|QQQ|META|AMZN")] # 관심종목 설정에 유용
    # df = df.sort_values('IndustryCode', ascending=True)  # NASDAQ Industry 분류 순으로 정렬, 테마별로 보는데 유용할 것으로 기대
    df = df[['Symbol', 'Name']]
    # df = df.head(1)
    # df = df.head(10)
    # df = df.head(20)
    # df = df.head(100)
    df_usa_etf = df
    # DebuggingUtil.print_magenta(f'''df_usa_etf : \n{df_usa_etf}''')
    DebuggingUtil.print_magenta(rf'''len(df_usa_etf) : {len(df_usa_etf)}''')
    df_krx = df_krx.rename(columns={"Code": "ticker", "Name": "stock_name", "Market": "market_name"})  # df 헤더명 제어
    df_usa = df_usa.rename(columns={"Symbol": "ticker", "Name": "stock_name"})
    df2 = pd.DataFrame()  # df2 에 빈 df 저장
    df2['Market'] = ['NASDAQ'] * len(df_usa)  # df2의 'Market' 열에 len(df_usa)개 만큼의 데이터가 'NASDAQ'인 레코드 저장
    df_usa = pd.concat([df_usa, df2], ignore_index=True, axis=1)  # df 가로병합 # 두 데이터프레임 병합
    df_usa.columns = ["ticker", "stock_name", "market_name"]  # df_usa 에 컬럼명 설정
    df_usa_etf = df_usa_etf.rename(columns={"Symbol": "ticker", "Name": "stock_name"})
    df3 = pd.DataFrame()
    df3['Market'] = ['US/ETF'] * len(df_usa_etf)
    df_usa_etf = pd.concat([df_usa_etf, df3], ignore_index=True, axis=1)  # df 가로병합 # 두 데이터프레임 병합
    df_usa_etf.columns = ["ticker", "stock_name", "market_name"]  # df_usa 에 컬럼명 설정
    df_concated = pd.concat([df_krx, df_usa, df_usa_etf], ignore_index=True)  # df 세로병합 # 두 데이터프레임 병합

    # function().xlsx 에 저장
    FILE_XLSX = f"{StateManagementUtil.DIRECTORY_PKG_XLSX}/{inspect.currentframe().f_code.co_name}().xlsx"
    FileSystemUtil.make_leaf_file(FILE_XLSX)
    df_concated.to_excel(FILE_XLSX)

    # df_fig.x 에 저장
    # fig.write_image("df_fig.png")
    # fig.write_image("df_fig.jpeg")
    # fig.write_image("df_fig.svg")
    # fig.write_image("df_fig.webp")
    # fig.write_image("df_fig.pdf")
    # fig.write_html("df_fig.html")

    # df 에 저장
    # FILE_XLSX = f"{StateManagementUtil.DIRECTORY_PKG_XLSX}/{inspect.currentframe().f_code.co_name}().xlsx"
    # DebuggingUtil.print_magenta(rf'''FILE_XLSX : {FILE_XLSX}''')
    # df_xlsx = pd.read_excel(FILE_XLSX)
    # DebuggingUtil.print_magenta(f'df_xlsx : \n{df_xlsx}')
    # DebuggingUtil.print_magenta(rf'type(df_xlsx) : {type(df_xlsx)}')
    # DebuggingUtil.print_magenta(rf'len(df_xlsx) : {len(df_xlsx)}')
    # df = pd.read_csv(rf"{pkg_park4139_for_linux.Park4139.PROJECT_DIRECTORY}\$cache_recycle_bin\test.xlsx")
    # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv')
    # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv')
    # df = pd.read_html(FILE_HTML)

    # fig 에 저장
    # fig = ff.create_table(df)
    # fig.show()


@TestUtil.measure_seconds_performance_nth
def update_db_finance_stock_ticker():
    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
    # __________________________________________________________________________________________________________________________________
    # import FinanceDataReader as fdr
    # import pandas as pd
    # import plotly.express as px
    # # pip install kaleido
    # from PySide6.QtCore import QCoreApplication
    # from PySide6.QtWidgets import QApplication
    import FinanceDataReader as fdr  # 주가 변화에 대한 실시간 데이터를 제공하지 않음, 나는 주가 변화에 대한 고빈도 실시간 데이터를 원하므로 다른 대안 필요.

    # 데이터 업데이트 주기가 매 프로그램 시작마다인 데이터 처리(stock ticker or stock id , stock name)
    # 데이터 업데이트가 하루 주기여도 되는 데이터만 선정, 데이터 업데이트 주기가 매 프로그램 시작마다인 현재 방식을 DB 에 데이터를 넣어 불러오는 방식으로, 데이터 업데이트 주기를 한달 주기로 변경 예정.
    # 한국주식
    # df_krx에 저장
    # 거래소상장주식코드목록 via StockListing()
    market = 'KRX'  # 대한민국 거래소 , KOSPI+KOSDAQ+KONEX
    # market='KOSDAQ'
    # market='KOSPI'
    # market='KONEX' # 코넥스
    df = fdr.StockListing(market=market)
    # 레코드들 필터링
    # DebuggingUtil.print_ment_magenta(rf'''df.columns : {df.columns}''')  # 헤더 컬럼들 제어
    # df  = df[df["Name"].str.contains("삼성전자|하이닉스")]
    # df = df[df["Name"].str.contains("삼성") & df["Name"].str.contains("전자")]
    # df  = df[df["Name"] == "삼성전자"]
    # df  = df[df["Name"].str.contains("삼성전자")]
    # df = df[df["ChangeCode"] == "1"]  # 오늘 양봉,
    # df = df[df["ChangeCode"] == "2"]  # 오늘 음봉
    # df = df[3 <= df["ChagesRatio"]]  # 오늘 3프로 이상 간 것
    df = df.sort_values('Code', ascending=False)  # 레코드들 순번 제어
    df = df[['Code', 'Name', 'Market']]
    # df = df.head(1)
    # df = df.head(10)
    # df = df.head(20)
    # df = df.head(100)
    # df = df.sort_values('Stocks', ascending=False) # 'Stocks': 주식의 총 개수. 발행된 주식의 총 개수. 총 상장 주식수는 해당 종목의 주식이 시장에 총 몇 주가 상장되어 있는지를 나타내며, 기업의 규모와 주식 시장에서의 유동성을 판단하는데 사용됩니다.
    # df = df.sort_values('Marcap', ascending=False) # 'Marcap': 시가총액(Market Capitalization), Marcap = stocks * 주가(close), 해당 종목의 모든 주식이 현재 시장에서 평가받는 총 가치를 의미합니다. 시가총액은 주식 시장에서 기업의 크기와 가치를 판단하는 지표.
    # df = df.sort_values('Volume', ascending=False) # 'Volume': 당일의 주식의 총수 변화량, 매수총수 + 매도총수, 활발한 거래를 나타내는 지표
    # df = df.sort_values('Amount', ascending=False) # 'Amount': 당일의 주식의 거래량 Amount = Volume * 주가(Close), 활발한 거래를 나타내는 지표
    df_krx = df
    # DebuggingUtil.print_ment_magenta(rf'''df_krx : {df_krx}''')
    DebuggingUtil.print_magenta(rf'''len(df_krx) : {len(df_krx)}''')
    # fig = ff.create_table(df_krx)
    # fig.show()

    # 미국주식
    # df_usa에 저장
    # market='NYSE'  # 뉴욕거래소
    # market='S&P500'
    market = 'NASDAQ'
    df = fdr.StockListing(market=market)
    # 레코드들 필터링
    # DebuggingUtil.print_ment_magenta(rf'''df.columns : {df.columns}''')  # 헤더 컬럼들 제어
    # df = df[['Symbol', 'Name', 'IndustryCode', 'Industry']]
    # df  = df[df["Name"].str.contains("NVDA|AAPL|META|AMZN")]
    # df  = df[~df["IndustryCode"].str.contains("63101010|63102010")] # ~ 연산자로 제외할 수 있다.
    # df  = df[df["Name"] == "NVDA"]
    # df  = df[df["Name"].str.contains("NVDA")]
    df = df.sort_values('IndustryCode', ascending=True)  # NASDAQ Industry 분류 순으로 정렬, 테마별로 보는데 유용할 것으로 기대
    df = df[['Symbol', 'Name']]
    # df = df.head(1)
    # df = df.head(10)
    # df = df.head(20)
    # df = df.head(100)
    df_usa = df
    # DebuggingUtil.print_ment_magenta(rf'''df_usa : {df_usa}''')
    DebuggingUtil.print_magenta(rf'''len(df_usa) : {len(df_usa)}''')
    # fig = ff.create_table(df_usa)
    # fig.show()

    # count_ticker_current 에 저장
    count_ticker_current = len(df_krx) + len(df_usa)
    DebuggingUtil.print_magenta(rf'''count_ticker_current : {count_ticker_current}''')

    # count_ticker_previous 에 저장
    df2 = MySqlUtil.execute(f'''select COUNT(*) FROM finance_stock_ticker;''')
    # DebuggingUtil.print_ment_magenta(rf'''df2 : {df2}''')
    df2 = df2['COUNT(*)']
    count_ticker_previous = df2.item()
    DebuggingUtil.print_magenta(rf'''count_ticker_previous : {count_ticker_previous}''')

    # ticker 수에 변화가 있으면 finance_stock_ticker(DB 내의 ticker 목록) 업데이트
    if count_ticker_previous != count_ticker_current:

        # finance_stock_ticker 비우기
        MySqlUtil.execute(f'truncate table finance_stock_ticker;')

        # finance_stock_ticker 에 저장
        cnt_usa = 0
        for index, row in df.iterrows():
            dict_data = {
                'ticker': row['Symbol'],
                'stock_name': row['Name'],
                'market_name': market,
            }
            FinanceStockTickerUtil.insert_finance_stock_ticker(finance_stock_ticker=dict_data, db=MySqlUtil.get_session_local())
            cnt_usa += 1
            # DebuggingUtil.print_ment_magenta(rf'''cnt_usa : {cnt_usa}  dict_data : {dict_data}''')
        DebuggingUtil.print_magenta(rf'''cnt_usa : {cnt_usa}''')

        # finance_stock_ticker 에 저장
        cnt_kra = 0
        for index, row in df_krx.iterrows():
            dict_data = {
                'ticker': row['Code'],
                'stock_name': row['Name'],
                'market_name': row['Market'],
            }
            FinanceStockTickerUtil.insert_finance_stock_ticker(finance_stock_ticker=dict_data, db=MySqlUtil.get_session_local())
            cnt_kra += 1
            # DebuggingUtil.print_ment_magenta(rf'''cnt_kra : {cnt_kra}  dict_data : {dict_data}''')
        DebuggingUtil.print_magenta(rf'''cnt_kra : {cnt_kra}''')


@TestUtil.measure_seconds_performance_nth
def update_db_stock_info_via_naver_pay_finance():
    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
    '''네이버페이증권 전종목 주식정보'''
    try:
        from datetime import date
        from dateutil.relativedelta import relativedelta
        import requests as rq

        # ticker 에 저장
        tickers = []
        df = pd.read_excel(StateManagementUtil.FILE_DF_TICKER_XLSX)
        # DebuggingUtil.print_magenta(rf'''df.columns : {df.columns}''')
        df = df[['ticker', 'stock_name']]
        # DebuggingUtil.print_magenta(rf'''df : {df}''')
        tickers = df['ticker'].tolist()  # 특정열 제어 #특정열만 list 로 추출
        # DebuggingUtil.print_magenta(rf'''ticker : {ticker}''')

        # start_time/end_time 에 저장
        # start_time = (date.today() + relativedelta(years=-5)).strftime("%Y%m%d")
        # start_time = (date.today() + relativedelta(days=-1)).strftime("%Y%m%d") # days 로 하면 크롤링 막힘
        start_time = (date.today() + relativedelta(years=-1)).strftime("%Y%m%d")
        end_time = (date.today()).strftime("%Y%m%d")

        # stock_info 비우기
        MySqlUtil.execute(f'truncate table stock_info;')  # success

        # DB에 저장
        for ticker in tickers:
            # get request
            # url = f'''https://fchart.stock.naver.com/siseJson.nhn?symbol={ticker}&requestType=1&startTime={start_time}&endTime={end_time}&timeframe=day''', 처음에 됬는데 안됨
            url = f'''https://m.stock.naver.com/front-api/v1/external/chart/domestic/info?symbol={ticker}&requestType=1&startTime={start_time}&endTime={end_time}&timeframe=day'''  # 보통주
            DebuggingUtil.print_magenta(rf'''url : {url}''')
            response = rq.get(url)
            if response.status_code == 200:
                data_bytes = response.content
                # DebuggingUtil.print_magenta(rf'''data_bytes : {data_bytes}''')
                df = pd.read_csv(BytesIO(data_bytes))  # caution, timedelta 를 days -1 으로 하면 데이터 크롤링 막힘
                # df = pd.read_csv(BytesIO(data_bytes), encoding='euc-kr') # success
                # df = pd.read_csv(BytesIO(data_bytes), encoding='cp949') # success, cp949 가 euc-kr 보다 범용적
                # DebuggingUtil.print_magenta(rf'''df.columns : {df.columns}''')  # 헤더 제어, before
                df = df.iloc[:, 0:6]  # 0 에서 6 까지 컬럼 제어
                # DebuggingUtil.print_magenta(rf'''df.columns : {df.columns}''')  # 헤더 제어, after
                df.columns = ['날짜', '시가', '고가', '저가', '종가', '거래량']  # 컬럼 제어, 컬럼헤더가 데이터가 [[]] 이런식으로 이상했기에 재정의
                df = df.dropna()  # NaN 값을 포함하는 모든 행을 삭제
                df['날짜'] = df['날짜'].str.extract(r'(\d+)')  # "321" 321, 정규식으로 숫자추출
                df['날짜'] = pd.to_datetime(df['날짜'])
                df['종목코드'] = ticker  # 컬럼추가
                # DebuggingUtil.print_magenta(rf'''df : {df}''')
                ticker_updated = []
                for index, df_row in df.iterrows():
                    dict_data = {
                        'date': df_row['날짜'],
                        'open': df_row['시가'],
                        'high': df_row['고가'],
                        'low': df_row['저가'],
                        'close': df_row['종가'],
                        'volume': df_row['거래량'],
                        'ticker': df_row['종목코드'],
                    }
                    StockInfoUtil.insert_stock_info(stock_info=dict_data, db=MySqlUtil.get_session_local())
                    ticker_updated.append(df_row['종목코드'])
                # [DebuggingUtil.print_magenta(sample) for sample in ticker_updated ]
                # DebuggingUtil.print_magenta(rf'len(ticker_updated) : {len(ticker_updated)}')
            else:
                DebuggingUtil.print_ment_fail(f'url: {url} 요청이 실패')

            # 네이버 증권 크롤링 방어책 회피 시도
            BusinessLogicUtil.sleep(milliseconds=random.randint(5000, 10000), print_mode=False)
    except UnicodeDecodeError:
        traceback.print_exc(file=sys.stdout)
    except Exception:
        traceback.print_exc(file=sys.stdout)


@TestUtil.measure_seconds_performance_nth
def crawl_stock_info_via_naver_pay_finance(search_word: str):
    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
    '''네이버페이증권 특정종목 주식정보'''

    from io import StringIO
    import pandas as pd
    from bs4 import BeautifulSoup
    driver = None
    try:
        # 검색
        # search_word = "삼성"
        # search_word = "삼성전자"
        # search_word = "삼성전자우"

        data_list = FinanceStockTickerUtil.get_finance_stock_tickers(db=MySqlUtil.get_session_local())
        # DebuggingUtil.print_magenta(rf'data_list : {data_list}')
        # DebuggingUtil.print_magenta(rf'type(data_list) : {type(data_list)}')
        # DebuggingUtil.print_magenta(rf'len(data_list) : {len(data_list)}')
        if len(data_list) == 0:
            update_db_finance_stock_ticker()

        # df = pd.DataFrame(data_list)
        # DebuggingUtil.print_magenta(rf'df : {df}')
        # DebuggingUtil.print_magenta(rf'type(df) : {type(df)}')
        # DebuggingUtil.print_magenta(rf'len(df) : {len(df)}')

        df = BusinessLogicUtil.get_ticker_by_search(stock_name=search_word)
        df = df[['ticker', 'stock_name']]
        DebuggingUtil.print_magenta(rf'df : {df}')
        DebuggingUtil.print_magenta(rf'type(df) : {type(df)}')
        DebuggingUtil.print_magenta(rf'len(df) : {len(df)}')
        data_list = df['ticker'].tolist()
        tickers = data_list

        df_concated = pd.DataFrame()
        for ticker in tickers:
            # ticker = '068270'
            df = BusinessLogicUtil.get_stock_name(ticker)
            df = df[['stock_name']]
            data_list = df['stock_name'].tolist()
            # DebuggingUtil.print_magenta(rf'data_list : {data_list}')
            # DebuggingUtil.print_magenta(rf'type(data_list) : {type(data_list)}')
            # DebuggingUtil.print_magenta(rf'len(data_list) : {len(data_list)}')
            stock_name = data_list[0]
            # DebuggingUtil.print_ment_light_white(f'''{stock_name} 주식가격 정보 웹크롤링''')

            # selenium way
            driver = SeleniumUtil.get_driver_for_selenium()
            target_url = f'https://finance.naver.com/item/sise_day.nhn?code={ticker}&page=1'
            DebuggingUtil.print_magenta(rf'''target_url : {target_url}''')
            driver.get(target_url)
            html = driver.page_source
            # DebuggingUtil.print_magenta(rf'''html : {html}''')
            soup = BeautifulSoup(html, "lxml")
            # DebuggingUtil.print_magenta(rf'soup : {soup}')
            # DebuggingUtil.print_magenta(rf'type(soup) : {type(soup)}')
            # DebuggingUtil.print_magenta(rf'len(soup) : {len(soup)}')
            table = soup.select("table")
            # DebuggingUtil.print_magenta(rf'table : {table}')
            # DebuggingUtil.print_magenta(rf'type(table) : {type(table)}')
            # DebuggingUtil.print_magenta(rf'len(table) : {len(table)}')
            data_str = str(table[0])
            data_string_io = StringIO(data_str)
            data_list = pd.read_html(data_string_io)
            # DebuggingUtil.print_magenta(rf'data_list[0] : {data_list[0]}')
            # DebuggingUtil.print_magenta(rf'type(data_list[0]) : {type(data_list[0])}')
            # DebuggingUtil.print_magenta(rf'len(data_list[0]) : {len(data_list[0])}')
            df = data_list[0]
            # DebuggingUtil.print_magenta(rf'df : {df}')
            # DebuggingUtil.print_magenta(rf'type(df) : {type(df)}')
            # DebuggingUtil.print_magenta(rf'len(df) : {len(df)}')
            df = df.dropna()  # NaN 값을 포함하는 모든 행을 삭제
            # DebuggingUtil.print_magenta(rf'df : {df}')
            # DebuggingUtil.print_magenta(rf'type(df) : {type(df)}')
            # DebuggingUtil.print_magenta(rf'len(df) : {len(df)}')
            # DebuggingUtil.print_magenta(rf'''df.columns : {df.columns}''')
            # DebuggingUtil.print_magenta(rf'type(df.columns) : {type(df.columns)}')
            # DebuggingUtil.print_magenta(rf'len(df.columns) : {len(df.columns)}')
            df.columns = ['날짜', '종가', '전일비', '시가', '고가', '저가', '거래량']
            # DebuggingUtil.print_magenta(rf'''df.columns : {df.columns}''')
            # DebuggingUtil.print_magenta(rf'type(df.columns) : {type(df.columns)}')
            # DebuggingUtil.print_magenta(rf'len(df.columns) : {len(df.columns)}')
            df = df[['날짜', '시가', '고가', '저가', '종가', '거래량']]
            df = df.head(3)
            df['주식명'] = stock_name
            # DebuggingUtil.print_magenta(rf'df : {df}')
            # DebuggingUtil.print_magenta(rf'type(df) : {type(df)}')
            # DebuggingUtil.print_magenta(rf'len(df) : {len(df)}')
            df_concated = pd.concat([df_concated, df], ignore_index=True, axis=0)  # df 병합 # 두 데이터프레임 병합, 0 수직병합(기본값) 1 수평병합

        DebuggingUtil.print_magenta(f'df_concated : \n{df_concated}')
        DebuggingUtil.print_magenta(rf'type(df_concated) : {type(df_concated)}')
        DebuggingUtil.print_magenta(rf'len(df_concated) : {len(df_concated)}')

        # 통계
        df_describe = df_concated.groupby('주식명')['종가'].describe()
        # DebuggingUtil.print_magenta(f'df_describe : \n{df_describe}')
        # DebuggingUtil.print_magenta(rf'type(df_describe) : {type(df_describe)}')
        # DebuggingUtil.print_magenta(rf'len(df_describe) : {len(df_describe)}')
        mean_close = df_concated.groupby('주식명')['종가'].mean()
        # DebuggingUtil.print_magenta(f'mean_close : \n{mean_close}')
        # DebuggingUtil.print_magenta(rf'type(mean_close) : {type(mean_close)}')
        # DebuggingUtil.print_magenta(rf'len(mean_close) : {len(mean_close)}')
        stock_name_biggist_mean_close = df_concated.groupby('주식명')['종가'].mean().idxmax()  # 평균종가 가 가장큰 '주식명'
        # DebuggingUtil.print_magenta(f'stock_name_biggist_mean_close : \n{stock_name_biggist_mean_close}')
        # DebuggingUtil.print_magenta(rf'type(stock_name_biggist_mean_close) : {type(stock_name_biggist_mean_close)}')
        # DebuggingUtil.print_magenta(rf'len(stock_name_biggist_mean_close) : {len(stock_name_biggist_mean_close)}')

        # 검색된주식 날짜 종가 시각화(테이블)
        # df_to_visualize = df_concated
        # fig = ff.create_table(df_to_visualize)
        # fig.show()

        return df_concated

    finally:
        # driver.close()
        driver.quit()


# @TestUtil.measure_seconds_performance_nth # 이 데코레이션 두개 걸어두면 중간에 멈춰버림
def crawl_won_dollar_exchange_rate_via_naver_pay_finance():
    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
    '''환율 크롤링'''
    # 1USD == ?KRW
    import requests as rq

    url = "https://finance.naver.com/marketindex/"
    DebuggingUtil.print_magenta(rf'''url : {url}''')
    response = rq.get(url)
    # response = rq.get(url).json()
    if response.status_code == 200:
        data_bytes = response.content
        # DebuggingUtil.print_magenta(rf'''data_bytes : {data_bytes}''')
        soup = BeautifulSoup(data_bytes, "lxml")
        # DebuggingUtil.print_magenta(f'soup : \n{soup}')
        # DebuggingUtil.print_magenta(rf'type(soup) : {type(soup)}')
        # DebuggingUtil.print_magenta(rf'len(soup) : {len(soup)}')
        # data_rs = soup.find_all(class_='head_info head_info') # 2024 03 04 새벽에 SUCCESS, 2024 03 04 보니 head_info point_dn 로 변경됨 FAIL
        data_rs = soup.find_all(class_='head_info point_dn')  # 2024 03 04 새벽에 SUCCESS, 2024 03 04 보니 head_info point_dn 로 변경됨 FAIL
        # DebuggingUtil.print_magenta(f'data_rs : \n{data_rs}')
        # DebuggingUtil.print_magenta(rf'type(data_rs) : {type(data_rs)}')
        # DebuggingUtil.print_magenta(rf'len(data_rs) : {len(data_rs)}')
        # DebuggingUtil.print_magenta(f'data_rs[0] : \n{data_rs[0]}')
        # DebuggingUtil.print_magenta(rf'type(data_rs[0]) : {type(data_rs[0])}')
        # DebuggingUtil.print_magenta(rf'len(data_rs[0]) : {len(data_rs[0])}')
        data_tag = data_rs[0]
        # DebuggingUtil.print_magenta(f'data_tag : \n{data_tag}')
        # DebuggingUtil.print_magenta(rf'type(data_tag) : {type(data_tag)}')
        # DebuggingUtil.print_magenta(rf'len(data_tag) : {len(data_tag)}')
        data_tag = data_tag.find(class_='value')
        # DebuggingUtil.print_magenta(f'data_tag : \n{data_tag}')
        # DebuggingUtil.print_magenta(rf'type(data_tag) : {type(data_tag)}')
        # DebuggingUtil.print_magenta(rf'len(data_tag) : {len(data_tag)}')
        data_str = data_tag.text
        data_str = data_str.replace(",", '')
        # DebuggingUtil.print_magenta(f'data_str : \n{data_str}')
        data_float = float(data_str)
        won_dollar_exchange_rate = data_float
        # DebuggingUtil.print_magenta(f'won_dollar_exchange_rate : {won_dollar_exchange_rate}')
        DebuggingUtil.print_magenta(f'네이버 페이 증권 원달러-환율정보 크롤링 결과, 1달러(USD)는  {won_dollar_exchange_rate}원(KRW) 입니다')
        return won_dollar_exchange_rate
    else:
        DebuggingUtil.print_ment_fail(f'url: {url} 요청이 실패')


# @TestUtil.measure_seconds_performance_nth
def update_ticker_xlsx_watched():
    '''
    주식 관심종목 티커정보 업데이트 함수
    update_ticker_xlsx().xlsx 의 데이터를 의존함.
    '''
    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
    from tqdm import tqdm

    # df 에 저장
    FILE_XLSX = fr"{StateManagementUtil.DIRECTORY_PKG_XLSX}/update_ticker_xlsx().xlsx"
    DebuggingUtil.print_magenta(rf'''FILE_XLSX : {FILE_XLSX}''')
    df_xlsx = pd.read_excel(FILE_XLSX)
    # DebuggingUtil.print_magenta(f'df_xlsx : \n{df_xlsx}')
    # DebuggingUtil.print_magenta(rf'type(df_xlsx) : {type(df_xlsx)}')
    DebuggingUtil.print_magenta(rf'len(df_xlsx) : {len(df_xlsx)}')

    # 관심종목 레코드 df 최상단 재배치 진행률
    # df의 특정(조건에 충족하는)레코드들을 df 최상단으로 배치
    watch_keywords_list = StateManagementUtil.WATCH_KEYWORDS_LIST
    df_concated = df_xlsx

    # for i in tqdm(range(0, len(watch_keywords_list)), desc=f"{inspect.currentframe().f_code.co_name}()"):
    for i in tqdm(range(0, len(watch_keywords_list)), desc=f"관심종목 레코드 df 최상단 재배치 진행률"):
        pattern = watch_keywords_list[i]
        pattern = re.compile(pattern, re.IGNORECASE)
        condition = df_concated['stock_name'].str.contains(pattern)
        df_meeted = df_concated[condition]
        df_meeted_not = df_concated[~condition]
        df_concated = pd.concat([df_meeted, df_meeted_not], ignore_index=True, axis=0)

    condition = df_concated['stock_name'].isin(watch_keywords_list)
    df_meeted = df_concated[condition]
    df_meeted_not = df_concated[~condition]
    df_concated = pd.concat([df_meeted, df_meeted_not], ignore_index=True, axis=0)
    # DebuggingUtil.print_magenta(f'df_concated : \n{df_concated}')
    # DebuggingUtil.print_magenta(rf'type(df_concated) : {type(df_concated)}')
    # DebuggingUtil.print_magenta(rf'len(df_concated) : {len(df_concated)}')

    condition = df_concated['ticker'].isin(watch_keywords_list)
    df_meeted = df_concated[condition]
    df_meeted_not = df_concated[~condition]
    df_concated = pd.concat([df_meeted, df_meeted_not], ignore_index=True, axis=0)
    # DebuggingUtil.print_magenta(f'df_concated : \n{df_concated}')
    # DebuggingUtil.print_magenta(rf'type(df_concated) : {type(df_concated)}')
    # DebuggingUtil.print_magenta(rf'len(df_concated) : {len(df_concated)}')
    df_concated = df_concated[['ticker', 'stock_name', 'market_name']]

    # 샘플 출력
    df_headed = df_concated.head(100)
    DebuggingUtil.print_magenta(f'df_headed : \n{df_headed}')
    # DebuggingUtil.print_magenta(rf'type(df_headed) : {type(df_headed)}')
    # DebuggingUtil.print_magenta(rf'len(df_headed) : {len(df_headed)}')

    # func().xlsx 에 저장
    FILE_XLSX = f"{StateManagementUtil.DIRECTORY_PKG_XLSX}/{inspect.currentframe().f_code.co_name}().xlsx"
    FileSystemUtil.make_leaf_file(FILE_XLSX)
    df_concated.to_excel(FILE_XLSX)

    # df 에 저장
    FILE_XLSX = f"{StateManagementUtil.DIRECTORY_PKG_XLSX}/{inspect.currentframe().f_code.co_name}().xlsx"
    DebuggingUtil.print_magenta(rf'''FILE_XLSX : {FILE_XLSX}''')
    df_xlsx = pd.read_excel(FILE_XLSX)
    # DebuggingUtil.print_magenta(f'df_xlsx : \n{df_xlsx}')
    # DebuggingUtil.print_magenta(rf'type(df_xlsx) : {type(df_xlsx)}')
    DebuggingUtil.print_magenta(rf'len(df_xlsx) : {len(df_xlsx)}')


# @TestUtil.measure_seconds_performance_nth
def update_stack_info_xlsx_watched():
    '''
    주식 관심종목 주식 정보 업데이트
    update_ticker_xlsx_watched().xlsx 파일을 의존함.
    '''
    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
    import yfinance as yf
    from matplotlib import pyplot as plt

    # # df 에 저장
    # FILE_XLSX = fr"{StateManagementUtil.DIRECTORY_PKG_XLSX}/update_ticker_xlsx_watched().xlsx"
    # # DebuggingUtil.print_magenta(rf'''FILE_XLSX : {FILE_XLSX}''')
    # df = pd.read_excel(FILE_XLSX)
    # # DebuggingUtil.print_magenta(f'df : \n{df}')
    # # DebuggingUtil.print_magenta(rf'type(df) : {type(df)}')
    # # DebuggingUtil.print_magenta(rf'len(df) : {len(df)}')
    # df = df.head(len(StateManagementUtil.WATCH_KEYWORDS_LIST)) # 모든 종목을 크콜링하려면 주석처리 len(StateManagementUtil.WATCH_KEYWORDS_LIST) 는 얼추 맞춘거지 정확도가 낮음.
    # # DebuggingUtil.print_magenta(f'df : \n{df}')
    # # DebuggingUtil.print_magenta(rf'type(df) : {type(df)}')
    # # DebuggingUtil.print_magenta(rf'len(df) : {len(df)}')
    # df_ticker_info = df[['ticker', 'stock_name', 'market_name']]
    # # DebuggingUtil.print_magenta(f'df_ticker_info : \n{df_ticker_info}')
    # # DebuggingUtil.print_magenta(rf'type(df_ticker_info) : {type(df_ticker_info)}')
    # # DebuggingUtil.print_magenta(rf'len(df_ticker_info) : {len(df_ticker_info)}')
    # df = df[['ticker']]
    # data_list = df['ticker'].tolist()
    # tickers = data_list
    # DebuggingUtil.print_magenta(f'tickers : {tickers}')
    # DebuggingUtil.print_magenta(rf'len(tickers) : {len(tickers)}')
    #
    # tickers_errored = []  # fail?, try 처리 안되는 것 같은데?
    # df_concated_yf = pd.DataFrame()
    # df_concated_krx = pd.DataFrame()
    # for i in range(0, len(tickers)):
    #     # for i in tqdm(range(0, len(tickers)), desc="미국/한국 주식정보 크롤링 진행률"):
    #     try:
    #         if tickers[i].isdigit():  # 한국주식 ticker는 숫자구성, 추가적으로 아닌 경우있다면 수정필요.
    #             # df = BusinessLogicUtil.get_stock_name(tickers[i])
    #             # df = df[['stock_name']]
    #             # data_list = df['stock_name'].tolist()
    #             # DebuggingUtil.print_magenta(rf'data_list : {data_list}')
    #             # DebuggingUtil.print_magenta(rf'type(data_list) : {type(data_list)}')
    #             # DebuggingUtil.print_magenta(rf'len(data_list) : {len(data_list)}')
    #             # stock_name = data_list[0]
    #             # DebuggingUtil.print_ment_light_white(f'''{stock_name} 주식가격 정보 웹크롤링''')
    #
    #             # selenium way
    #             driver = SeleniumUtil.get_driver_for_selenium()
    #             target_url = f'https://finance.naver.com/item/sise_day.nhn?code={tickers[i]}&page=1'
    #             DebuggingUtil.print_magenta(rf'''target_url : {target_url}''')
    #             driver.get(target_url)
    #             html = driver.page_source
    #             # DebuggingUtil.print_magenta(rf'''html : {html}''')
    #             soup = BeautifulSoup(html, "lxml")
    #             # DebuggingUtil.print_magenta(rf'soup : {soup}')
    #             # DebuggingUtil.print_magenta(rf'type(soup) : {type(soup)}')
    #             # DebuggingUtil.print_magenta(rf'len(soup) : {len(soup)}')
    #             table = soup.select("table")
    #             # DebuggingUtil.print_magenta(rf'table : {table}')
    #             # DebuggingUtil.print_magenta(rf'type(table) : {type(table)}')
    #             # DebuggingUtil.print_magenta(rf'len(table) : {len(table)}')
    #             data_str = str(table[0])
    #             data_string_io = StringIO(data_str)
    #             data_list = pd.read_html(data_string_io)
    #             # DebuggingUtil.print_magenta(rf'data_list[0] : {data_list[0]}')
    #             # DebuggingUtil.print_magenta(rf'type(data_list[0]) : {type(data_list[0])}')
    #             # DebuggingUtil.print_magenta(rf'len(data_list[0]) : {len(data_list[0])}')
    #             df = data_list[0]
    #             # DebuggingUtil.print_magenta(rf'df : {df}')
    #             # DebuggingUtil.print_magenta(rf'type(df) : {type(df)}')
    #             # DebuggingUtil.print_magenta(rf'len(df) : {len(df)}')
    #             df = df.dropna()  # NaN 값을 포함하는 모든 행을 삭제
    #             # DebuggingUtil.print_magenta(rf'df : {df}')
    #             # DebuggingUtil.print_magenta(rf'type(df) : {type(df)}')
    #             # DebuggingUtil.print_magenta(rf'len(df) : {len(df)}')
    #             # DebuggingUtil.print_magenta(rf'''df.columns : {df.columns}''')
    #             # DebuggingUtil.print_magenta(rf'type(df.columns) : {type(df.columns)}')
    #             # DebuggingUtil.print_magenta(rf'len(df.columns) : {len(df.columns)}')
    #             df.columns = ['날짜', '종가', '전일비', '시가', '고가', '저가', '거래량']
    #             # DebuggingUtil.print_magenta(rf'''df.columns : {df.columns}''')
    #             # DebuggingUtil.print_magenta(rf'type(df.columns) : {type(df.columns)}')
    #             # DebuggingUtil.print_magenta(rf'len(df.columns) : {len(df.columns)}')
    #             # DebuggingUtil.print_magenta(f'stock_name : \n{stock_name}')
    #             # DebuggingUtil.print_magenta(rf'type(stock_name) : {type(stock_name)}')
    #             # DebuggingUtil.print_magenta(rf'len(stock_name) : {len(stock_name)}')
    #             # df['주식명'] = stock_name
    #             df['날짜'] = pd.to_datetime(df['날짜'])
    #             df['날짜'] = df['날짜'].dt.strftime('%Y-%m-%d %H:%M:%S')
    #             df['티커'] = tickers[i]
    #             data_list = df['종가'].tolist()
    #             df['수정종가'] = pd.DataFrame(data_list)  # 수정종가 를 알 수 없어, 종가를 수정종가 와 동등하도록 임의 초기화
    #             df = df[['티커', '날짜', '시가', '고가', '저가', '종가', '수정종가', '거래량']]
    #             # DebuggingUtil.print_magenta(rf'df : {df}')
    #             # DebuggingUtil.print_magenta(rf'type(df) : {type(df)}')
    #             # DebuggingUtil.print_magenta(rf'len(df) : {len(df)}')
    #             # df_concated_krx = pd.concat([df_concated_krx, df], ignore_index=True, axis=0)
    #             df_concated_krx = pd.concat([df_concated_krx, df], axis=0)  # df 세로병합
    #         else:
    #             df = yf.download(tickers[i], progress=False)
    #             # DebuggingUtil.print_magenta(f'df : {df}')
    #             # DebuggingUtil.print_magenta(rf'type(df) : {type(df)}')
    #             # DebuggingUtil.print_magenta(rf'len(df) : {len(df)}')
    #             # DebuggingUtil.print_magenta(f'df : \n{df}')
    #             # DebuggingUtil.print_magenta(rf'type(df) : {type(df)}')
    #             # DebuggingUtil.print_magenta(rf'len(df) : {len(df)}')
    #             date_list = df.index
    #             # DebuggingUtil.print_magenta(f'date_list : \n{date_list}')
    #             # DebuggingUtil.print_magenta(rf'type(date_list) : {type(date_list)}')
    #             # DebuggingUtil.print_magenta(rf'len(date_list) : {len(date_list)}')
    #             df_date = pd.DataFrame(date_list)
    #             df_date.columns = ['date']
    #             # DebuggingUtil.print_magenta(f'df_date : \n{df_date}')
    #             # DebuggingUtil.print_magenta(rf'type(df_date) : {type(df_date)}')
    #             # DebuggingUtil.print_magenta(rf'len(df_date) : {len(df_date)}')
    #             df.reset_index(drop=True, inplace=True)  # drop=True df.index를 drop, inplace=True df.index의 제자리에서 수정
    #             df = pd.concat([df, df_date], axis=1)
    #             # DebuggingUtil.print_magenta(f'df.columns : \n{df.columns}')
    #             df.columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'date']
    #             # DebuggingUtil.print_magenta(f'df : \n{df}')
    #             # DebuggingUtil.print_magenta(rf'type(df) : {type(df)}')
    #             # DebuggingUtil.print_magenta(rf'len(df) : {len(df)}')
    #             df['date'] = pd.to_datetime(df['date'])
    #             df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    #             df['ticker'] = tickers[i]
    #             df = df[['ticker', 'date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
    #             df = pd.concat([df_concated_yf, df], axis=0)  # df 세로병합
    #             # DebuggingUtil.print_magenta(f'df : \n{df}')
    #             # DebuggingUtil.print_magenta(rf'type(df) : {type(df)}')
    #             # DebuggingUtil.print_magenta(rf'len(df) : {len(df)}')
    #             df_concated_yf = df
    #             BusinessLogicUtil.sleep(milliseconds=random.randint(1777, 2111), print_mode=False)
    #     except:
    #         traceback.print_exc(file=sys.stdout)
    #         # TestUtil.pause()
    #         tickers_errored.append(tickers[i])
    # DebuggingUtil.print_magenta(f'tickers_errored : {tickers_errored}')
    # DebuggingUtil.print_magenta(rf'len(tickers_errored) : {len(tickers_errored)}')
    # df_concated_krx = df_concated_krx[['티커', '날짜', '시가', '고가', '저가', '종가', '수정종가', '거래량']]
    # # DebuggingUtil.print_magenta(f'df_concated_krx : \n{df_concated_krx}')
    # # DebuggingUtil.print_magenta(rf'type(df_concated_krx) : {type(df_concated_krx)}')
    # # DebuggingUtil.print_magenta(rf'len(df_concated_krx) : {len(df_concated_krx)}')
    # df_concated_krx.columns = ['ticker', 'date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    # # DebuggingUtil.print_magenta(f'df_concated_krx : \n{df_concated_krx}')
    # # DebuggingUtil.print_magenta(rf'type(df_concated_krx) : {type(df_concated_krx)}')
    # # DebuggingUtil.print_magenta(rf'len(df_concated_krx) : {len(df_concated_krx)}')
    # won_dollar_exchange_rate = crawl_won_dollar_exchange_rate_via_naver_pay_finance()  # 원에서 달러로 단위변환(원달러 환율 적용)
    # df_concated_krx['Open'] = df_concated_krx['Open'] / won_dollar_exchange_rate
    # df_concated_krx['High'] = df_concated_krx['High'] / won_dollar_exchange_rate
    # df_concated_krx['Low'] = df_concated_krx['Low'] / won_dollar_exchange_rate
    # df_concated_krx['Close'] = df_concated_krx['Close'] / won_dollar_exchange_rate
    # df_concated_krx['Adj Close'] = df_concated_krx['Adj Close'] / won_dollar_exchange_rate
    # df_concated_krx['Volume'] = df_concated_krx['Volume'] / won_dollar_exchange_rate
    # # DebuggingUtil.print_magenta(f'df_concated_krx : \n{df_concated_krx}')
    # # DebuggingUtil.print_magenta(rf'type(df_concated_krx) : {type(df_concated_krx)}')
    # # DebuggingUtil.print_magenta(rf'len(df_concated_krx) : {len(df_concated_krx)}')
    # # DebuggingUtil.print_magenta(f'df_concated_yf : \n{df_concated_yf}')
    # # DebuggingUtil.print_magenta(rf'type(df_concated_yf) : {type(df_concated_yf)}')
    # # DebuggingUtil.print_magenta(rf'len(df_concated_yf) : {len(df_concated_yf)}')
    # # DebuggingUtil.print_magenta(rf'''df_concated_krx.columns : {df_concated_krx.columns}''')
    # # DebuggingUtil.print_magenta(rf'''df_concated_yf.columns : {df_concated_yf.columns}''')
    #
    # # df join/merge
    # # df_concated = pd.concat([df_ticker_info, df], ignore_index=True, axis=0)  # df 세로병합
    # # df_merged = pd.merge(df_ticker_info, df, on='ticker', how='outer')
    # # df_merged = pd.merge(df_ticker_info, df, on='ticker', how='inner')
    # # df_merged = pd.merge(df_ticker_info, df, on='ticker', how='left')
    # # df_merged = pd.merge(df_ticker_info, df, on='ticker', how='right')
    # # df_diff = pd.concat([df1, df2], axis=0 ).drop_duplicates(keep=False)
    #
    # # df join
    # df_usa = pd.merge(df_ticker_info, df_concated_yf, on='ticker', how='inner')
    # df_usa['ticker'] = df_usa['ticker'] + "[" + df_usa['stock_name'] + "]"
    # df_krx = pd.merge(df_ticker_info, df_concated_krx, on='ticker', how='inner')
    # # df_krx['ticker'] = f"{df_krx['stock_name']}[{df_krx['ticker']}]" # fail
    # df_krx['ticker'] = df_krx['stock_name'] + "[" + df_krx['ticker'] + "]"
    # df = pd.concat([df_usa, df_krx], ignore_index=True, axis=0)
    #
    #
    # # DebuggingUtil.print_magenta(f'df : \n{df}')
    # # DebuggingUtil.print_magenta(rf'type(df) : {type(df)}')
    # # DebuggingUtil.print_magenta(rf'len(df) : {len(df)}')
    #
    # # function().xlsx 에 저장
    # FILE_XLSX = f"{StateManagementUtil.DIRECTORY_PKG_XLSX}/{inspect.currentframe().f_code.co_name}().xlsx"
    # FileSystemUtil.make_leaf_file(FILE_XLSX)
    # df.to_excel(FILE_XLSX)
    # # DebuggingUtil.print_magenta(f'df : \n{df}')
    # # DebuggingUtil.print_magenta(rf'type(df) : {type(df)}')
    # # DebuggingUtil.print_magenta(rf'len(df) : {len(df)}')

    # df 에 저장
    FILE_XLSX = f"{StateManagementUtil.DIRECTORY_PKG_XLSX}/{inspect.currentframe().f_code.co_name}().xlsx"
    DebuggingUtil.print_magenta(rf'''FILE_XLSX : {FILE_XLSX}''')
    df = pd.read_excel(FILE_XLSX)
    DebuggingUtil.print_magenta(f'df : \n{df}')
    DebuggingUtil.print_magenta(rf'type(df) : {type(df)}')
    DebuggingUtil.print_magenta(rf'len(df) : {len(df)}')
    # df = pd.read_csv(rf"{pkg_park4139_for_linux.Park4139.PROJECT_DIRECTORY}\$cache_recycle_bin\test.xlsx")
    # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv')
    # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv')
    # df = pd.read_html(FILE_HTML)

    #  df에서 ticker 별로 x축은 date 이고, y축은 Adj Close에 대한 변화를 꺽은선 그래프로 plot 을 사용해서 html 에 그리고 싶어
    # df.groupby('ticker')['Adj Close'].plot(legend=True)
    # plt.title("Ticker별 date에 따른 Adj Close 변화")
    plt.title('날짜에 따른 Ticker별 관심종목 수정종가(Close) 변화', color='red')
    plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글폰트 적용
    # font_abspath = rf"{pkg_park4139_for_linux.Park4139.PROJECT_DIRECTORY}\$cache_fonts\GmarketSans\GmarketSansTTFLight.ttf"
    # # font_abspath = rf"{pkg_park4139_for_linux.Park4139.PROJECT_DIRECTORY}\$cache_fonts\Rubik_Doodle_Shadow\RubikDoodleShadow-Regular.ttf" # 너무 귀여운 입체감 있는 영어폰트
    # plt.rcParams['font.family'] = pkg_park4139_for_linux.Park4139.get_font_name_for_mataplot(font_abspath)
    # 폰트가 깨진것 같을 때, 캐싱된 폰트 캐시 삭제하기 위해 사용
    # import matplotlib.font_manager as fm
    # fm._rebuild()
    # plt.grid(True)
    # plt.rcParams['figure.facecolor'] = 'black'  # '바탕색'
    # plt.rcParams['axes.edgecolor'] = 'white'  # '테두리 색'
    # plt.rcParams['axes.facecolor'] = 'black'  # '바탕색'
    # plt.rc('font', family='NanumGothicOTF') # For MacOS
    # plt.rc('font', family='NanumGothic')  # For Windows
    fig, ax = plt.subplots()
    for ticker, data in df.groupby('ticker'):
        ax.plot(data['date'], data['Adj Close'], label=ticker)

    # x 축에 날짜 형식을 지정
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.ticker import MultipleLocator
    # date_formatter = mdates.DateFormatter('%Y-%m-%d')
    date_formatter = mdates.DateFormatter('%Y')
    # ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    # ax.xaxis.set_major_locator(MultipleLocator(base=5))
    ax.xaxis.set_major_locator(mdates.YearLocator(base=10))
    ax.xaxis.set_major_formatter(date_formatter)
    ax.tick_params(axis='x', rotation=45)
    ax.tick_params(axis='y', rotation=45)
    ax.set_xlabel('날짜', rotation=0, verticalalignment='center')
    # ax.xaxis.set_label_coords(-0.15, 0)
    ax.set_ylabel('수정 종가', rotation=0, verticalalignment='center')  # '수정 종가' 텍스트를 90도로 회전하고 수직으로 정렬합니다.
    ax.yaxis.set_label_coords(-0.15, 0.5) # '수정 종가'와 y축 스케일과 글자가 겹침,  y 축 레이블의 위치를 보정.
    ax.legend()
    plt.tight_layout()  # '날짜' 글자가 잘리는 것을 예방

    # png에 저장(그래프)
    FILE_PNG = f"{StateManagementUtil.DIRECTORY_PKG_PNG}/{inspect.currentframe().f_code.co_name}().png"
    FileSystemUtil.make_leaf_file(FILE_PNG)
    plt.savefig(FILE_PNG)

    # HTML에 저장(그래프)
    FILE_HTML = f"{StateManagementUtil.DIRECTORY_PKG_HTML}/{inspect.currentframe().f_code.co_name}().html"
    FileSystemUtil.make_leaf_file(FILE_HTML)
    data_html = f"""
    <html>
    <body>
    <h1>Ticker별 Adj Close 변화</h1>
    <img src="{FILE_PNG}">
    </body>
    </html>
    """
    with open(FILE_HTML, "w") as f:
        f.write(data_html)

    # # 꺽은선 그래프 (line plot)
    # import plotly.express as px
    # # DebuggingUtil.print_magenta(f'df.columns : \n{df.columns}')
    # fig = px.line(data_frame=df, y=df['Adj Close'], x=df['date'], markers=True, color=df['ticker'])
    # # line_color = ['yellowgreen', 'yellow', 'whitesmoke', 'white', 'wheat', 'violet', 'turquoise', 'tomato', 'thistle', 'teal', 'tan', 'steelblue', 'springgreen', 'snow', 'slategrey', 'slategray', 'slateblue', 'skyblue', 'silver', 'sienna', 'seashell', 'seagreen', 'sandybrown', 'salmon', 'saddlebrown', 'royalblue', 'rosybrown', 'red', 'rebeccapurple', 'purple', 'powderblue', 'plum', 'pink', 'peru', 'peachpuff', 'papayawhip', 'palevioletred', 'paleturquoise', 'palegreen', 'palegoldenrod', 'orchid', 'orangered', 'orange', 'olivedrab', 'olive', 'oldlace', 'navy', 'navajowhite', 'moccasin', 'mistyrose', 'mintcream', 'midnightblue', 'mediumvioletred', 'mediumturquoise', 'mediumspringgreen', 'mediumslateblue', 'mediumseagreen', 'mediumpurple', 'mediumorchid', 'mediumblue', 'mediumaquamarine', 'maroon', 'magenta', 'linen', 'limegreen', 'lime', 'lightyellow', 'lightsteelblue', 'lightslategrey', 'lightslategray', 'lightskyblue', 'lightseagreen', 'lightsalmon', 'lightpink', 'lightgrey', 'lightgreen', 'lightgray', 'lightgoldenrodyellow', 'lightcyan', 'lightcoral', 'lightblue', 'lemonchiffon', 'lawngreen', 'lavenderblush', 'lavender', 'khaki', 'ivory', 'indigo', 'indianred', 'hotpink', 'honeydew', 'grey', 'greenyellow', 'green', 'gray', 'goldenrod', 'gold', 'ghostwhite', 'gainsboro', 'fuchsia', 'forestgreen', 'floralwhite', 'firebrick', 'dodgerblue', 'dimgrey', 'dimgray', 'deepskyblue', 'deeppink', 'darkviolet', 'darkturquoise', 'darkslategrey', 'darkslategray', 'darkslateblue', 'darkseagreen', 'darksalmon', 'darkred', 'darkorchid', 'darkorange', 'darkolivegreen', 'darkmagenta', 'darkkhaki', 'darkgrey', 'darkgreen', 'darkgray', 'darkgoldenrod', 'darkcyan', 'darkblue', 'cyan', 'crimson', 'cornsilk', 'cornflowerblue', 'coral', 'chocolate', 'chartreuse', 'cadetblue', 'burlywood', 'brown', 'blueviolet', 'blue', 'blanchedalmond', 'black', 'bisque', 'beige', 'azure', 'aquamarine', 'aqua', 'antiquewhite', 'aliceblue']
    # # line_color = line_color[:len(df.columns)]
    # # line_color = random.choice([line_color])
    # # fig.update_traces(line_width=1, line_dash='dash', line_color=line_color)
    # fig.show()

    # fig = ff.create_table(df)
    # fig.show()


@TestUtil.measure_seconds_performance_nth
def test_test_test():
    '''

    '''
    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")

    # crawl 을 할 때 대상 url 이 get 방식이면 request/bs 사용, 추후 빠른동작을 기대
    # crawl 을 할 때 대상 url 이 post 방식이면 selenium/bs 사용, request/bs 방식이 안되는 경우 해결 기대

    # 티커 중복처리 코드
    # 국가의 중복
    # 티커.국가코드
    # 티커.거래소코드

    # 26,전업투자자, 적은 금액으로 미수금을 풀, 스켈핑, 돌파매매, 소액으로 안되면 큰돈으로 해도 안된다.
    # 40, 전업투자자, 이평선 매매 이격이 크면, 이격 사이에 반등이 나올 확률이 크다, 월 5%-10 수익 목표, 한가지매매법 1년 이상 유지
    # 봉차트
    # 키움, 차트보기
    # 하나대투, 주문
    # 인베스팅 닷컴 크롤링
    # # speak("매수신호발생")
    #
    # 예수금 100만원 일수익금 1만원 월수익금 20만원, 1년간 90프로 확율료
    # 예수금 10000만원 일수익금 100만원 월수익금 20만원, 1년간 90프로 확율료
    # 뇌동매매 안해야 한다
    #
    # 돌파매매
    # 종가베팅
    # 대형주베팅
    # 상따
    #
    # 강방천 회장, 1년 뒤에 저 기업이 수면제 먹고 눈 떴을 때 있을까?,  기업의 서비스가 주머니를 열게 하나?,분산투자 반드시 할 것
    #
    # 휴대폰, 한 집에 두개
    # 네이버 꺼 하나 사고
    # 삼성oo랑 메타랑 협업 한다고 하잖아, 큰 그림 그리길 기대하고 하나 하보자.
    #
    # 최원호, 힐링여행자, 약세장이 1-2년에 모아서, 강세장이 4-5년에 팔면, 가진돈의 두배 정도가 될 것, 웃음이 새어나오는
    #
    # 피터린치, 칵테일파티 면 고점분위기, 아니면 저점분위기, 이 관점에서는 AI 는 고점

    # 죽음 # 주가담보대출 # 반대매매

    # 유퀴즈, 원양어선, 일등항해사, 억대연봉
    # https://www.youtube.com/watch?v=6hYpI_5kXHY

    # 시세정보 via DataReader(),
    # fdr_dr = fdr.DataReader('000150', '2018-01-01', '2019-10-30', exchange='KRX')  # 005930 삼성전자 # 000150 두산 # 특정기간 # exchange='KRX' 거래소, # exchange='KRX-DELISTING' KRX에서 상장폐지된
    # ticker 제한
    # 티커란, 미국에서 사용하는 종목 코드이며 네 자리로 제안
    # DebuggingUtil.print_ment_magenta(rf'type(fdr_dr) : {type(fdr_dr)}')
    # DebuggingUtil.print_ment_magenta(rf'''fdr_dr : {fdr_dr}''')

    # DebuggingUtil.print_ment_magenta(rf'''df['학번'].to_string(index=False) : {df['학번'].to_string(index=False)}''')  # 특정 컬럼만 보기(데이터조회), index 제거하고
    # df = df.query("학번==1001")
    # df = df.query("continent == 'Europe' and year == 2007 and pop > 2.e6")

    # 산점도 그래프 (scatter plot)
    # fig = px.scatter(df, y=columns[1], x=columns[2], color=columns[1], color_continuous_scale=px.colors.sequential.Viridis)

    # 꺽은선 그래프 (line plot)
    # fig = px.line(data_frame=df, y=columns[2], x=columns[1],markers=True , color=columns[2])
    # fig = px.line(data_frame=df, y=columns[2], x=columns[1], markers=True)  # success
    # fig.update_traces(line_width=1, line_dash='dash', line_color="red")

    # 막대그래프 (bar plot)
    # fig = px.bar(df, y=columns[2], x=columns[1], color=columns[2], color_discrete_sequence=px.colors.qualitative.G10) # 세로형, color 는 범례
    # fig = px.bar(df, y=columns[1], x=columns[2], color=columns[1], color_discrete_sequence=px.colors.qualitative.G10)  # 가로형
    # fig.update_traces(textfont_size=12, textfont_color='red', textfont_family="Times", textangle=0, textposition="outside")
    # fig.update_traces(textfont_size=12, textfont_color='red', textfont_family="Times", textangle=0, textposition="inside")
    # fig.update_traces(textfont_size=12, textfont_color='red', textfont_family="Times", textangle=0, textposition="auto")
    # 5개 막대 색 설정( x 가 5개 여야 할 듯)
    # colors = ['lightslategray', 'crimson', 'lightslategray', 'lightslategray', 'lightslategray']
    # import plotly.graph_objects as go
    # fig = go.Figure()
    # fig.add_trace(go.Bar(x=['Feature A', 'Feature B', 'Feature C', 'Feature D', 'Feature E'], y=[20, 14, 23, 25, 22],
    #                      marker_color=colors))

    # 원 그래프 (Pie chart)
    # fig = px.pie(values=[4500, 2500, 1053, 500], names=['Oxygen', 'Hydrogen', 'Carbon_Dioxide', 'Nitrogen'])
    # fig.update_traces(textposition='outside', textinfo='label+percent+value', textfont_size=20, textfont_color="black")
    # fig.update_traces(marker_colors=px.colors.sequential.RdBu, marker_line_color="black", marker_line_width=2)

    # 테이블(Table)
    # import plotly.graph_objects as go
    # fig = go.Figure()
    # fig.add_trace(go.Table(
    #     header=dict(values=['A Scores', 'B Scores'],
    #                 line_color='darkslategray',
    #                 # fill_color='lightskyblue',
    #                 fill_color=['rgb(239, 243, 255)', 'rgb(189, 215, 231)'], # 컬럼 색상
    #
    #                 align="center"),
    #     cells=dict(values=[[100, 90, 80, 90],  # 1열
    #                        [95, 85, 75, 95]],  # 2열
    #                line_color='darkslategray',
    #                # fill_color='lightcyan',
    #                fill_color=['rgb(230, 240, 250)', 'rgb(180, 210, 230)'],
    #                align="center")))
    # fig.show()

    # Plotly 의 Available templates 테스트
    # import plotly.io as pio
    # DebuggingUtil.print_ment_magenta(rf'''pio.templates : {pio.templates}''')
    # templates_available = ['ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff', 'ygridoff', 'gridon', 'none']
    # for template in templates_available:
    #     fig = px.scatter(df,
    #                      y=columns[2], x=columns[1], color=columns[1], size=columns[2],
    #                      # log_x=True,
    #                      size_max=60,
    #                      template=template, title=f"Plotly 내장 템플릿들을 직접 보고 고르세요: based on '{template}' theme")
    #     fig.show()

    # Hover 말풍선 텍스트 편집
    # fig.update_traces(hovertemplate='x: %{x} <br>y: %{y}')
    # fig.update_traces(hovertemplate='이름: %{x} <br>점수: %{y}')
    # fig.update_traces(hovertemplate=None, selector={'name': 'Europe?????????'})  # revert to default hover

    # 마우스 팁을 따라다니는 수평 수직선 설정
    # fig.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across", spikethickness=0.5)
    # fig.update_yaxes(showspikes=True, spikecolor="green", spikethickness=0.5)

    # 로컬 테스트 화면 chrome 에서 출력
    # config = {'displayModeBar': False} # 모든버튼 제거
    # config = {'modeBarButtonsToRemove': ['zoom', 'pan']}  # 특정버튼 제거
    # fig.show(config=config)

    # fig = px.histogram(df, y=columns[2], x=columns[1], histfunc='sum', facet_col=columns[1], )

    # 파일로 저장하기
    # fig.write_image("df_fig.png")
    # fig.write_image("df_fig.jpeg")
    # fig.write_image("df_fig.svg")
    # fig.write_image("df_fig.webp")
    # fig.write_image("df_fig.pdf")
    # fig.write_html("df_fig.html")

    # # FILE_XLS = rf"{pkg_park4139_for_linux.Park4139.PROJECT_DIRECTORY}\$cache_recycle_bin\test.xlsx"
    # df = pd.read_csv(FILE_CSV)
    # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv')
    # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv')
    # df = pd.read_sql(FILE_SQL)
    # df = pd.read_html(FILE_HTML)
    # df = pd.read_excel(FILE_XLS)
    # DebuggingUtil.print_ment_magenta(rf'''str(df) : {str(df)}''')
    # import plotly.figure_factory as ff
    # fig = ff.create_table(df)

    # pandas 공부 후기
    # # 엑셀에 있는 데이터들 처럼 데이터배열 을 예쁘게 해주는 라이브러리
    # # sr(series) 는 key, value 형태의 1차원배열데이터 에 사용. df 기능으로 대체가 되므로 굳이 잘 안쓸듯.
    # # df(dataframe) 은 2차원배열데이터에 사용. 즉, 엑셀처럼 사용, 엄청유용할 듯
    # # df 를 출력하면 기본적으로 auto increment number 가 auto fill 된다!, 유용함!, 근데 지우는 방법도 찾아보기
    # # csv/txt/xls/sql/html/json 파일 읽어올 수 있다고 하는데, html 도 되는데? 크롤링과 연계할 때 편리한 부분이 있을 수 있겠다

    # data: np.ndarray
    # data = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]])  # 하드코딩으로 데이터배열
    # # data = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])  # 하드코딩으로 데이터배열
    # # data = np.zeros(shape=(3,3)) # shape=(3,3)인 배열에 모든 값이 0
    # # data = np.ones(shape=(3,3)) # shape=(3,3)인 배열에 모든 값이 1
    # # data = np.eye(3)# shape=(3,3)인 배열에 대각선 값이 1, 나머지 값이 0, 이거 활용도 높을 수 있겠다. 100  010  001 이런 순서 필요할때 있지 않겠나?
    # # data = np.random.random((2,2)) # shape=(3,3)인 배열에 모든 값이 1보다 작은 float(1인 경우가 있나 모르겠음)
    # # data = np.full(shape=(2,3), 7)#  # shape=(3,3)인 배열에 모든 값이 7
    # # data = np.arange(10) #배열개수가 10 인 1차원데이터배열 # 0~9
    # # data = np.arange(0, 10, 1) # 시작0, 종료10, 1씩증가 인1차원데이터배열 # 0~9
    # # data = [i for i in range(0,10,1)] # 0~9
    # # data = np.array(np.arange(30)).reshape((5, 6)) # shape = (5,6) 으로 reshape 한다, shape 안의 숫자들(5, 6) 을 곱(5 x 6)하면 원데이터의 개수(5 x 6 = 30)인와 같게 설정해야 된다. 실험해봐도 이게 맞음, list를 적당한 간격으로 자를때 유용하겠다!
    # # data = data[0, :]# 첫번째 줄 출력
    # # data = data[:,0]# 첫번째 기둥 출력
    # # data = data[1,1]# 특정위치의 원소
    # # data = data[[0, 2], [2, 0]]  # 특정 위치의 원소 두 개를 가져와 새로운 배열 # data[0, 2] 와 data[2, 0] 를 가져와 새로운 배열에 넣었습니다
    # # data = data[0, 2] + data[2, 0] # 원소 두개를 가져와, 합을 구한다
    # # data = data[0, 2] * data[2, 0] # 곱을 구한다, 이는 행렬에 대한 곱이 아니다. 좌표에 대한 곱이다
    # # data = data[0, 2] ** data[2, 0] # 거듭제곱을 구한다
    # # data = data[0, 2] / data[2, 0] # 나눈 결과를 구한다 Q + R/B  B = 나누는 수
    # # data = data[0, 2] // data[2, 0] # 몫을 구한다
    # # data = data[0, 2] % data[2, 0] # 나머지를 구한다
    # # data_ = np.dot(data1, data2)# 행렬곱
    # # test_result = f"""
    # # mat 의 data           :
    # # {str(data)}
    # #
    # # mat 의 축의 개수       :
    # # {data.ndim}
    # #
    # # mat 의 배열의 모양     :
    # # {data.shape}
    # # """
    # DebuggingUtil.print_ment_magenta(rf'''test_result : {test_result}''')  # 특정 컬럼만 보기(데이터조회)

    # # numpy 공부 후기
    # # 배열은 행렬과 같은 관계처럼 느껴졌다.
    # # 다차원 행렬 자료구조 : 그냥 엑셀에서 사용하는 자료구조.
    # # ndarray 는 다차원 행렬 자료구조로 되어 있다.
    # # shape 배열의 생김새 정도 겠다, 표현은 shape=(3,3) 이런 형태
    # # 실험을 해보니 첫번째 shape=(줄번호, 기둥번호) 정도로 생각하면 되겠다
    # # 이제는 shape=(100,101) 이런 코드를 보면 데이터배열을 상상할 때 어떤 모양인지 알겠다.

    # # 행렬 공부 후기
    # # 행렬은 좌표 같다.
    # # 행렬의 연산은 각 좌표끼리 더하거나 곱하는 것과 같다.

    # import matplotlib.pyplot as plt
    #
    # # dir /b /s *.ttf | clip 으로 추출
    #
    # # 빨간 꺽은선 그래프
    # x = [1, 2, 3, 4, 5]
    # y = [2, 4, 6, 8, 10]
    # plt.plot(x, y, color="red")
    #
    # # 노란 꺽은선 그래프
    # plt.plot([1.5, 2.5, 3.5, 4.5], [3, 5, 8, 10], color="yellow")  # 라인 새로 추가
    #
    # # 범례 설정
    # legend = plt.legend(['학생 A', '학생 B'], facecolor='k', labelcolor='white')
    # ax = plt.gca()
    # leg = ax.get_legend()
    # leg.legendHandles[0].set_color('red')
    # leg.legendHandles[1].set_color('yellow')
    #
    # # 전체화면 설정
    # # mng = plt.get_current_fig_manager()
    # # mng.full_screen_toggle()
    #
    # # 레이블 설정
    # plt.xlabel('x 축 레이블', color='white')
    # plt.ylabel('y 축 레이블', color='white')
    # plt.tick_params(labelcolor='white')
    #
    # plt.show()
    #
    # # Matplotlib 공부 후기
    # # 맷플롯립
    # # 데이터 시각화 패키지 : 차트/도표/..를 그려주는 도구
    # # 설치 : pip install matplotlib --upgrade
    # # import 시 네이밍 관례 : as plt 로 import 한다 : import matplotlib.pyplot as plt
    # # 조아써 이제 그래프 그릴 수 있어
    pass


error_cnt = 0
if __name__ == '__main__':
    try:
        # ____________________________________________________________
        # won_dollar_exchange_rate = crawl_won_dollar_exchange_rate_via_naver_pay_finance()
        # BROADCOM
        # update_db_stock_info_via_naver_pay_finance() # 이건 watched 된 krx 만 하는 게 좋겠다.
        # update_db_finance_stock_ticker()
        # crawl_geo_info()
        # crawl_pm_ranking()
        # crawl_korean_ultrafine_dust()
        # crawl_naver_weather()

        # crawl_finance_data_via_fdr() # krx stock info via fdr
        # crawl_stock_info_via_naver_pay_finance(search_word="삼성전자") # krx stock info via naver pay finance

        # update_ticker_xlsx() # ETF-US/NASDAQ/KRX 티커 업데이트, 상장소식 있으면 호출
        # update_ticker_xlsx_watched() # 관심종목 ticker 업데이트, 관심종목 변경 되면 호출
        update_stack_info_xlsx_watched()  # 관심종목 주식가격 업데이트, 장끝나면 호출, 매일 호출

        # test_test_test()
        # ____________________________________________________________
        # Park4139.sleep(milliseconds=1000)# 루프 텀 설정
        # ____________________________________________________________
        # 의도적 트러블 발생 테스트
        # raise shutil.Error("의도적 트러블 발생")
    except Exception as e:
        # print(str(e))
        # logger.info(f'logger: dst : {"??????"}')
        # logger.error(msg="에러발생?????")
        # logger.error(f'logger: str(e) : {"????????"}')
        # DebuggingUtil.trouble_shoot("%%%FOO%%%")
        traceback.print_exc(file=sys.stdout)
        # TestUtil.pause()

# 코드세그먼트 라이브스니펫
# 웹크롤링
