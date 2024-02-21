__author__ = 'PARK4139 : Jung Hoon Park'

import inspect
import os
# -*- coding: utf-8 -*-  # python 3.x 하위버전 호환을 위한코드
import sys
import traceback

from PySide6.QtWidgets import QApplication

from pkg_park4139_for_linux import TestUtil, TextToSpeechUtil, DebuggingUtil, BusinessLogicUtil


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
        DebuggingUtil.commentize(f"__________________________________________________{inspect.currentframe().f_code.co_name}")
        BusinessLogicUtil.print_today_time_info()
        os.system('pause >nul')

    @staticmethod
    def measure_seconds_performance(function):
        """시간성능 측정 데코레이터 코드"""

        # def wrapper(*args, **kwargs):
        def wrapper(**kwargs):  # **kwargs, keyword argument, dictionary 로 parameter 를 받음. named parameter / positional parameter 를 받을 사용가능?
            # def wrapper(*args):# *args, arguments, tuple 로 parameter 를 받음.
            # def wrapper():
            DebuggingUtil.commentize("TEST START")
            test_cycle_max_limit = 5
            if TestUtil.is_first_test_lap:
                ment = rf"총 {test_cycle_max_limit}번의 시간성능측정 테스트를 시도합니다"
                TestUtil.is_first_test_lap = False
                TextToSpeechUtil.speak_ment(ment=ment, sleep_after_play=1)
                DebuggingUtil.debug_as_cli(ment)
            seconds_performance_test_results = TestUtil.test_results
            import time
            time_s = time.time()
            # function(*args, **kwargs)
            function(**kwargs)
            # function(*args)
            # function()
            time_e = time.time()
            mesured_seconds = time_e - time_s
            DebuggingUtil.commentize(rf"시간성능측정 결과")
            seconds_performance_test_results.append(f"{round(mesured_seconds, 2)}sec")
            print(rf'seconds_performance_test_results : {seconds_performance_test_results}')
            print(rf'type(seconds_performance_test_results) : {type(seconds_performance_test_results)}')
            print(rf'len(seconds_performance_test_results) : {len(seconds_performance_test_results)}')
            if len(seconds_performance_test_results) == test_cycle_max_limit:
                TextToSpeechUtil.speak_ment("시간성능측정이 완료 되었습니다", sleep_after_play=0.55)
                DebuggingUtil.commentize("TEST END")
                TestUtil.pause()

        return wrapper

    @staticmethod
    def measure_milliseconds_performance(function):
        """시간성능 측정 코드"""

        def wrapper(*args, **kwargs):
            # def wrapper(*args):# *args, arguments, tuple 로 parameter 를 받음.
            # def wrapper():
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
                TextToSpeechUtil.speak_ments("시간성능측정이 완료 되었습니다", sleep_after_play=0.65)
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
    def wrapper():
        DebuggingUtil.commentize(rf"test status")
        function()

    return wrapper


@decorate_test_status_printing_code
def print_with_test_status(status: str):
    print(status)


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
# @decorate_for_pause  # 테스트 루프 마다 정지 설정
def test_sprint_core():
    try:
        # cmd = rf'python "{test_target_file}"' # SUCCESS # 가상환경이 아닌 로컬환경에서 실행이 됨.
        # cmd = rf'start cmd /k "{test_helping_bat_file}" {test_target_file}'  # SUCCESS # 가상환경에서 실행 # 새 cmd.exe 창에서 열린다
        # cmd = rf'start /b cmd /c "{test_helping_bat_file}" {test_target_file}' # FAIL  # 가상환경에서 실행되나 콘솔에 아무것도 출력되지 않음
        # cmd = rf'call "{test_helping_bat_file}" {test_target_file}'  # FAIL  # 가상환경에서 실행되나 콘솔에 사용자 입력만 출력됨
        # cmd = rf'"{test_helping_bat_file}" {test_target_file}' # FAIL  # 가상환경에서 실행되나  콘솔에 사용자 입력만 출력됨
        # cmd = rf'call cmd /c "{test_helping_bat_file}" {test_target_file}'  # FAIL  # 가상환경에서 실행되나 콘솔에 사용자 입력만 출력됨
        # cmd = rf'start cmd /c "{test_helping_bat_file}" {test_target_file}'  # SUCCESS # 가상환경에서 실행 # 새 cmd.exe 창에서 열린다 #이걸로 선정함
        # park4139.get_cmd_output(cmd)

        # Park4139.debug_as_cli(f"test")
        # Park4139.debug_as_gui(f"test")

        # Park4139.ask_to_google(question)
        # Park4139.ask_to_bard(question)
        # Park4139.ask_to_wrtn(question)

        # Park4139.speak_alt("테스트")

        # app = QApplication()
        # Park4139.get_comprehensive_weather_information_from_web()
        # app.exec()

        # __________________________________________________________________________________________________________________________________ TESTED SECTION 1 S
        # import os
        #
        # import matplotlib
        # import pandas as pd  # 데이터 분석용
        # # import metaplotlib # pip install metaplotlib --upgrade
        # import numpy as np  # pip install numpy --upgrade
        # import FinanceDataReader as fdr  # alt+f12 # pip install -U finance-datareader #  FinanceDataReade.chart.plot()는 plotly에 의존성이 있습니다. pip install plotly --upgrade 를 진행하세요
        # from PySide6.QtCore import QCoreApplication
        # from PySide6.QtWidgets import QApplication
        #
        # import pkg_park4139_for_linux
        #
        # # pyside6의 app이 없으면 pyside6 app을 만들어줌.
        # app: QApplication
        # if QCoreApplication.instance() == None:
        #     app = QApplication()
        #
        # # DataReader() 거래소주식정보(*,시세정보) 를 가져옴
        # # 005930 삼성전자
        # # fdr_dr = fdr.DataReader("005930") # 모든기간
        # # fdr_dr = fdr.DataReader("005930", "2021-01-01", "2022-02-23") # 특정기간
        # fdr_dr = fdr.DataReader("005930", "2023")  # 특정기간(특정년도)
        # #
        # # fdr_dr = fdr.DataReader('000150', '2018-01-01', '2019-10-30', exchange='KRX')  # 두산
        # # fdr_dr = fdr.DataReader('000150', '2018-01-01', '2019-10-30', exchange='SZSE')  # Yihua Healthcare Co Ltd
        # # fdr_dr = fdr.DataReader('036360', exchange='KRX-DELISTING') # KRX에서 상장폐지된
        #
        # # StockListing() 거래소주식정보(*,거래소상장주식목록)  가져옴
        # # df = fdr.StockListing('SSE')  # 상해
        # # df = fdr.StockListing('KONEX') # 코넥스
        # # df = fdr.StockListing('SZSE')
        # # df = fdr.StockListing('KRX')  # 한국
        # # df = fdr.StockListing('KOSDAQ')
        # # df = fdr.StockListing('KOSPI')
        # # df = fdr.StockListing('S&P500')
        # # df = fdr.StockListing('NYSE')  # 뉴욕거래소
        #
        # # test_result = df.plot.
        #
        # # sr = pd.Series(index=["피자", "치킨", "콜라", "맥주"], data=[17000, 18000, 1000, 5000])
        # # test_result = f"""
        # # {sr}
        # #
        # # {'-' * 79}
        # #
        # # index : {sr.index}
        # # values : {sr.values}
        # # """
        # # dialog = pkg_park4139_for_linux.CustomDialogReplica(title="1차원데이터배열 출력 테스트결과 ( feat. pandas.시리즈 자료구조)", contents=test_result, buttons=["확인"])
        # # dialog.exec_()
        # #
        # #
        # #
        # #
        # #
        # #
        # # columns=['학번', '이름', '점수']
        # # data = [
        # #     ['1000', 'Steve', 90.72],
        # #     ['1001', 'James', 78.09],
        # #     ['1002', 'Doyeon', 98.43],
        # #     ['1003', 'Jane', 64.19],
        # #     ['1004', 'Pilwoong', 81.30],
        # #     ['1005', 'Tony', 99.14],
        # # ]
        # # df = pd.DataFrame(data=data, columns=columns)
        # # test_result= str(df)
        # # dialog = pkg_park4139_for_linux.CustomDialogReplica(title="2차원데이터배열 출력 테스트결과 ( df 찐활용 feat. list )", contents=test_result, buttons=["확인"])
        # # dialog.exec_()
        #
        # # data = {
        # #     '학번' : ['1000', '1001', '1002', '1003', '1004', '1005'],
        # #     '이름' : [ 'Steve', 'James', 'Doyeon', 'Jane', 'Pilwoong', 'Tony'],
        # #     '점수': [90.72, 78.09, 98.43, 64.19, 81.30, 99.14]
        # #     }
        # #
        # # index=None # df 의 index 파라미터의 default , 자동증가숫자가 auto fill 됨
        # # # index=pd.RangeIndex(start=0, stop=5, step=1) # df 의 index 제어
        # # df = pd.DataFrame(data, index=index)
        # # # test_result= df.to_string() # 모든 줄 보기(데이터조회)
        # # # test_result= df.head(3).to_string() # 3 줄만 보기(데이터조회)
        # # # test_result= df['학번'].to_string() # 특정 컬럼만 보기(데이터조회)
        # # # test_result= df['학번'].to_string(index=False) # 특정 컬럼만 보기(데이터조회)
        # # test_result= df['학번'].to_string() # 특정 컬럼만 보기(데이터조회)
        # # dialog = pkg_park4139_for_linux.CustomDialogReplica(title="2차원데이터배열 출력 테스트결과 ( df 찐활용 feat. dict )", contents=test_result, buttons=["확인"])
        # # dialog.exec_()
        #
        # # FILE_XLS = rf"{pkg_park4139_for_linux.Park4139.PROJECT_DIRECTORY}\$cache_recycle_bin\test.xlsx"
        # # # df = pd.read_csv(FILE_CSV)
        # # # df = pd.read_sql(FILE_SQL)
        # # # df = pd.read_html(FILE_HTML)
        # # df = pd.read_excel(FILE_XLS)
        # # test_result = df.to_string()
        # # dialog = pkg_park4139_for_linux.CustomDialogReplica(title="csv파일의 2차원데이터배열 출력 테스트결과", contents=test_result, buttons=["확인"])
        # # dialog.exec_()
        #
        # # pandas 공부 후기
        # # 엑셀에 있는 데이터들 처럼 데이터배열 을 예쁘게 해주는 라이브러리
        # # sr(series) 는 key, value 형태의 1차원배열데이터 에 사용. df 기능으로 대체가 되므로 굳이 잘 안쓸듯.
        # # df(dataframe) 은 2차원배열데이터에 사용. 즉, 엑셀처럼 사용, 엄청유용할 듯
        # # df 를 출력하면 기본적으로 auto increment number 가 auto fill 된다!, 유용함!, 근데 지우는 방법도 찾아보기
        # # csv/txt/xls/sql/html/json 파일 읽어올 수 있다고 하는데, html 도 되는데? 크롤링과 연계할 때 편리한 부분이 있을 수 있겠다
        #
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
        # # dialog = pkg_park4139_for_linux.CustomDialogReplica(title="2차원데이터배열 출력 테스트결과 ( feat. numpy )", contents=test_result, buttons=["확인"])
        # # dialog.exec_()
        #
        # # numpy 공부 후기
        # # 배열은 행렬과 같은 관계처럼 느껴졌다.
        # # 다차원 행렬 자료구조 : 그냥 엑셀에서 사용하는 자료구조.
        # # ndarray 는 다차원 행렬 자료구조로 되어 있다.
        # # shape 배열의 생김새 정도 겠다, 표현은 shape=(3,3) 이런 형태
        # # 실험을 해보니 첫번째 shape=(줄번호, 기둥번호) 정도로 생각하면 되겠다
        # # 이제는 shape=(100,101) 이런 코드를 보면 데이터배열을 상상할 때 어떤 모양인지 알겠다.
        #
        # # 행렬 공부 후기
        # # 행렬은 좌표 같다.
        # # 행렬의 연산은 각 좌표끼리 더하거나 곱하는 것과 같다.
        #
        # import matplotlib.pyplot as plt
        #
        # # dir /b /s *.ttf | clip 으로 추출
        # # plt.rcParams['font.family'] ='Malgun Gothic' # 한글폰트 적용
        # font_abspath = rf"{pkg_park4139_for_linux.Park4139.PROJECT_DIRECTORY}\$cache_fonts\GmarketSans\GmarketSansTTFLight.ttf"
        # # font_abspath = rf"{pkg_park4139_for_linux.Park4139.PROJECT_DIRECTORY}\$cache_fonts\Rubik_Doodle_Shadow\RubikDoodleShadow-Regular.ttf" # 너무 귀여운 입체감 있는 영어폰트
        # plt.rcParams['font.family'] = pkg_park4139_for_linux.Park4139.get_font_name_for_mataplot(font_abspath)
        # plt.rcParams['figure.facecolor'] = 'black'  # '바탕색'
        # plt.rcParams['axes.edgecolor'] = 'white'  # '테두리 색'
        # plt.rcParams['axes.facecolor'] = 'black'  # '바탕색'
        #
        # # 제목 설정
        # plt.title('그래프 제목', color='white')
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
        # # 읽는 법 : 맷플롯립 이라고 읽는다.
        # # 데이터 시각화 패키지 : 쉽게 데이터로 차트를 그려주는 도구
        # # 설치 : pip install matplotlib --upgrade
        # # import 시 네이밍 관례 : as plt 로 import 한다 : import matplotlib.pyplot as plt
        # # 조아써 이제 그래프 그릴 수 있어
        #
        # # pyside6의 app이 없으면 pyside6 app을 실행
        # try:
        #     app.exec()
        # except:
        #     pass

        # __________________________________________________________________________________________________________________________________ TESTED SECTION 1 E
        # __________________________________________________________________________________________________________________________________ TESTED SECTION 2
        # dialog =  pkg_park4139_for_linux.CustomDialog(contents="테스트를 시작할까요?", buttons=["시작하기", "시작하지 않기"])
        # dialog.exec()
        # dialog.show()

        # global dialog
        # dialog = pkg_park4139_for_linux.CustomDialog(contents="다운로드하고 싶은 URL을 제출해주세요?", buttons=["제출", "제출하지 않기"], is_input_text_box=True)
        # dialog.show()
        # text_of_clicked_btn = dialog.text_of_clicked_btn
        # DebuggingUtil.commentize("text_of_clicked_btn")
        # Park4139.debug_as_cli(text_of_clicked_btn)
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
        #         self.show_dialog_signal.emit()
        # def show_dialog():
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
        import sprint_core  # sprint_core.py 테스트
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
        # Park4139.debug_as_gui(context=f"{results}")

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
        #         abspaths_and_mtimes = Park4139List.get_list_added_elements_alternatively(abspaths[start_index:end_index], mtimes[start_index:end_index])  # from [1, 2, 3] + [ x, y, z] to [1, x, 2, y, 3, z]
        #         abspaths_and_mtimes_ = Park4139List.get_nested_list_grouped_by_each_two_elements_in_list(abspaths_and_mtimes)  # from ["a", "b", "c", "d"] to [["a","b"], ["c","d"]]
        #         abspaths_and_mtimes__ = Park4139List.get_nested_list_sorted_by_column_index(nested_list=abspaths_and_mtimes_, column_index=1, decending_order=True)
        #         abspaths_and_mtimes___ = Park4139List.get_list_seperated_by_each_elements_in_nested_list(abspaths_and_mtimes__)  # from [["a","b"], ["c","d"]] to ["a", "b", "c", "d"]
        #         abspaths_and_mtimes____[start_index:end_index] = Park4139List.get_list_each_two_elements_joined(abspaths_and_mtimes___)  # from ["a", "b", "c", "d"] to ["ab", "cd"]
        #
        #     # 비동기 이벤트 루프 설정
        #     def run_async_event_loop(start_index: int, end_index: int ):
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
        # 서른넘어 수학공부
        #
        #
        # 함수목록  최신화일시="2023년 12월 30일 (토) 10:25:44"
        # def activate_window_by_pid(pid: int):
        # def aes_decrypt(key, ciphertext):
        # def aes_encrypt(key, plaintext):
        # def afterpause(function):
        # def ask_something_to_ai():
        # def ask_something_to_ai(self):
        # def ask_to_bard(question: str):
        # def ask_to_google(question: str):
        # def ask_to_web(question):
        # def ask_to_wrtn(question: str):
        # def bkup_biggest_targets():
        # def bkup_by_manual(target_abspath):
        # def bkup_db_toml():
        # def bkup_smallest_targets():
        # def bkup(target_abspath):
        # def move_this_window_to_front(self):
        # def move_window_to_front_by_pid(pid):
        # def bubble_sort_nested_list(nested_list, column_index):
        # def centerOnScreen(self):
        # def change_console_color():
        # def classify_targets_between_smallest_targets_biggest_targets():
        # def click_center_of_img_recognized_by_mouse_left(img_abspath: str, recognize_loop_limit_cnt=0, is_zoom_toogle_mode=False):
        # def click_mouse_left_btn(abs_x=None, abs_y=None):
        # def click_mouse_right_btn(abs_x=None, abs_y=None):
        # def close(self):
        # def cls():
        # def commentize(title):
        # def compress_string(original_string):
        # def connect_remote_rdp1():
        # def connect_to_remote_computer_via_chrome_desktop():
        # def convent_bytes_to_str(target: bytes):
        # def convent_str_to_bytes(target: str):
        # def convert_as_zip_with_timestamp(target_abspath):
        # def convert_img_to_img_blurred(img_abspath):
        # def convert_img_to_img_cropped(img_abspath, abs_x: int, abs_y: int, width_px: int, height_px: int):
        # def convert_img_to_img_flipped_horizontally(img_abspath):
        # def convert_img_to_img_flipped_vertical(img_abspath):
        # def convert_img_to_img_grey(img_abspath):
        # def convert_img_to_img_resized(img_abspath, width_px, height_px):
        # def convert_img_to_img_rotated(img_abspath, degree: int):
        # def convert_img_to_img_watermarked(img_abspath):
        # def convert_mp3_to_flac(target_abspath):
        # def convert_mp4_to_flac(target_abspath):
        # def convert_mp4_to_wav(target_abspath):
        # def convert_mp4_to_webm(target_abspath):
        # def convert_wav_to_flac(target_abspath):
        # def copy_and_paste_with_keeping_clipboard_current_contents(contents_new):
        # def copy_label_text_to_clipboard(self):
        # def countdown_and_click_negative_btn(self):
        # def countdown_and_click_positive_btn(self):
        # def create_db_toml():
        # def data(self, value):
        # def data(self):
        # def debug_as_cli(context: str):
        # def debug_as_gui(context: str, is_app_instance_mode=False, input_text_default=""):
        # def decode_as_lzw_algorizm(encrypted_text):
        # def decompress_string(compressed_string):
        # def delete_db_toml():
        # def do_once():
        # def do_random_schedules():
        # def download_clip_alt(url: str):
        # def download_clip(url: str):
        # def download_from_youtube_to_webm_alt(urls_from_prompt):
        # def download_from_youtube_to_webm(urls_from_prompt):
        # def download_video_from_web1():
        # def download_video_from_web1(self):
        # def download_video_from_web2(self):
        # def download_youtube_as_wav(self):
        # def download_youtube_as_webm_only_sound(self):
        # def empty_recycle_bin():
        # def encode_as_lzw_algorizm(plaintext: str):
        # def enter_power_saving_mode():
        # def enum_windows_callback(hwnd, _):
        # def eventFilter(self, obj, event):
        # def excute_macro(self):
        # def exit_macro(self):
        # def explorer(file_abspath: str):
        # def find_direction_via_naver_map(destination: str):
        # def gather_storages():
        # def gen_dictionary_for_monitor_target_edited_and_bkup(directory_abspath):
        # def get_abs_x_and_y_from_img(img_abspath):
        # def get_added_files(previous_state, current_state):
        # def get_all_pid_and_process_name():
        # def get_btn_name_promised(self, button_name_without_shortcut):
        # def get_btn_name_with_shortcut_name(self, button_name_without_shortcut):
        # def get_btn(self, btn_name, function, btn_text_align="left"):
        # def get_btn(self, btn_name, function):
        # def get_cmd_output(cmd):
        # def get_column_of_2_dimension_list(list_2_dimension: [], column_no):  # return 은 list 아니고 ndarray 일 수 있다
        # def get_common_elements(list1, list2):  # 두 개의 리스트를 비교하여 서로 동일한 요소만 새로운 리스트로 출력 # 중복값 색출
        # def get_comprehensive_weather_information_from_web():
        # def get_count_args(func):
        # def get_current_mouse_abs_info():
        # def get_current_program_pid():
        # def get_db_toml_key(target_abspath):
        # def get_deleted_files(previous_state, current_state):
        # def get_different_elements(list1, list2):  # 두 개의 리스트를 비교하여 서로 다른 요소만 모아서 리스트로 출력
        # def get_directory_files_mtime_without_files_excepted(directory_abspath):
        # def get_display_info():
        # def get_display_setting():
        # def get_driver_for_selenium():
        # def get_elements_that_list1_only_have(list1, list2):  # 두 개의 리스트를 비교하여 특정 하나의 리스트 만 가진 요소만 모아서 리스트로 출력
        # def get_font_for_pyside6(font_path):
        # def get_font_name_for_mataplot(font_abspath):
        # def get_infos_of_img_when_img_recognized_succeed(img_abspath, recognize_loop_limit_cnt=0, is_zoom_toogle_mode=False):
        # def get_length_of_mp3(target_abspath: str):
        # def get_line_cnt_of_file(target_abspath: str):
        # def get_list_added_elements_alternatively(list_for_odd, list_for_even):  # from [1, 2, 3] + [ x, y, z] to [1,x,2,y,3,z]
        # def get_list_each_two_elements_joined(list: []):  # from ["a", "b", "c", "d"] to ["ab", "cd"]
        # def get_list_replaced_from_list_that_have_special_characters(target: [str], replacement: str):  # from [str] to [str]
        # def get_list_seperated_by_each_elements_in_nested_list(nested_list):
        # def get_modified_files(previous_state, current_state):
        # def get_name_space():  # name space # namespace # 파이썬 네임스페이스
        # def get_nested_list_converted_from_ndarray(ndarray: numpy.ndarray):  # ndarray 에서 list 로 변환 # ndarray 에서 list 로 변환 # ndarray to nested []  from [[1 2]] to [[1, 2]] # from [ [str str] [str str] ]  to  [ [str, str], [str, str] ]
        # def get_nested_list_grouped_by_each_two_elements_in_list(list: []):  # from ["a", "b", "c", "d"] to [["a","b"], ["c","d"]]
        # def get_nested_list_removed_row_that_have_nth_element_dulplicated_by_column_index_for_ndarray(ndarray: [[]], column_index: int):  # 중복된 행 제거하는게 아니고 행의 2번째 요소가 중복되는 것을 제거
        # def get_nested_list_removed_row_that_have_nth_element_dulplicated_by_column_index(nested_list: [[]], column_index: int):  # 중복된 행 제거하는게 아니고 행의 2번째 요소가 중복되는 것을 제거
        # def get_nested_list_sorted_by_column_index(nested_list: [[str]], column_index: int, decending_order=False):  # tree depth(sample[1]) 에 대한 내림차순 정렬 # list 2차원 배열의 특정 열의 내림차순 정렬 # from [[str, str]] to [[str, str]]
        # def get_os_sys_environment_variable(environment_variable_name: str):
        # def get_process_name_by_pid(pid):
        # def get_shortcut_name_promised(self, button_name_without_shortcut):
        # def get_str_replaced_special_characters(target: str, replacement: str):  # str to str
        # def get_target_bite(start_path='.'):
        # def get_target_gigabite(target_path):
        # def get_target_megabite(target_path):
        # def get_target_pid_by_process_name_legacy(target_process_name: str):
        # def get_target_pid_by_process_name(target_process_name: str):
        # def get_time_as_(pattern: str):
        # def get_tree_depth_level(file_abspath: str):
        # def get_validated(target: any):
        # def get_webdriver_options_customed():
        # def git_push_by_auto():
        # def inputbox_changed(self):
        # def inputbox_edit_finished(self):
        # def inputbox_return_pressed(self):
        # def insert_db_toml(key, value):
        # def insert(self, word):
        # def is_accesable_local_database():
        # def is_containing_eng(text):
        # def is_containing_jpn(text):
        # def is_containing_kor(text):
        # def is_containing_number(text):
        # def is_containing_special_characters(text: str):
        # def is_directory_changed(directory_abspath):
        # def is_empty_directory(target_abspath):
        # def is_eng_or_kor_ja(text: str):
        # def is_file_changed(file_abspath):
        # def is_file_edited(target_abspath: str):
        # def is_only_eng_and_kor_and_no_and_speacial_characters(text):
        # def is_only_eng_and_no_and_speacial_characters(text):
        # def is_only_eng_and_no(text):
        # def is_only_eng_and_speacial_characters(text):
        # def is_only_eng(text):
        # def is_only_no(text):
        # def is_only_speacial_characters(text):
        # def is_regex_in_contents_with_case_ignored(contents, regex):
        # def is_regex_in_contents(target, regex):
        # def is_shortcut_pressed_within_10_secs(key_plus_key: str):
        # def is_two_lists_equal(list1, list2):
        # def is_validated(target: any):
        # def is_void_function(func):
        # def keyDown(key: str):
        # def keyPressEvent(self, e):
        # def keyUp(key: str):
        # def kill_alsong():
        # def kill_thread(thread_name):
        # def log_e(log_title="종료로깅"):
        # def log_mid(log_title="중간로깅"):
        # def log_s(log_title="시작로깅"):
        # def login(self):
        # def make_leaf_directory(leaf_directory_abspath):
        # def make_leaf_file(leaf_file_abspath):
        # def make_matrix_console():
        # def make_park4139_go_to_sleep():
        # def make_party_console():
        # def measure_milliseconds_performance(function):
        # def measure_seconds_performance(function):
        # def merge_directories(directoryies: str):
        # def merge_two_directories_without_overwrite(directory_a, directory_b):
        # def merge_video_and_sound(file_v_abspath, file_a_abspath):
        # def monitor_mouse_position_per_second(self):
        # def monitor_mouse_position(self, x, y):
        # def monitor_target_edited_and_bkup(target_abspath: str):
        # def mousePressEvent(self, e):
        # def move_mouse_rel_x(rel_x: int, rel_y: int):
        # def move_mouse(abs_x: int, abs_y: int):
        # def move_target_to_trash_bin(target_abspath):
        # def move_window_to_center(self):
        # def move_with_overwrite(src: str, dst: str):
        # def move_without_overwrite(src, dst):
        # def on_keboard_press(self, key):
        # def on_keys_down(self, key):
        # def on_keys_up(self, key):
        # def on_mouse_btn_clicked(self, x, y, button, pressed):
        # def on_mouse_move(self, x, y):  # 아주 빠르게 감지
        # def on_player_eos():
        # def on_single_key_pressed(self, key):
        # def open_mouse_info():
        # def open_project_directory(self):
        # def parse_youtube_video_id(url):
        # def pause():
        # def press(*presses: str, interval=0.0):
        # def print_and_open_py_pkg_global_path():
        # def print_list_each_two_elements(list: []):  # print(rf'list[index] list[index+1] : {list[index]} {list[index+1]}') without out of index
        # def print_python_process_for_killing_zombie_process():
        # def print_today_time_info():
        # def process_thread_loop(ment):
        # def raise_error(str: str):
        # def read_db_toml():
        # def reboot_this_computer():
        # def recommand_console_color():
        # def remove_special_characters(text):
        # def rename_target(current_target_abspath, future_target_abspath):
        # def replace_with_auto_no_orderless(contents: str, unique_word: str, auto_cnt_starting_no=0):
        # def replace_with_auto_no(contents: str, unique_word: str, auto_cnt_starting_no=0):
        # def replace_words_based_on_tri_node(text, dictionary):
        # def return_korean_week_name():
        # def rotate_window_size_mode(self):
        # def rpa_program_method_decorator(function: Callable[[T], None]):
        # def run_async_event_loop(q_application):
        # def run_async_event_loop(start_index: int, end_index: int, text: str):
        # def run_async_loop(q_application):
        # def run_async_loop1():
        # def run_async_loop2():
        # def run_async_loop3():
        # def run_async_loop4():
        # def run_cmd_exe_as_admin():
        # def run_cmd_exe_as_admin(self):
        # def run_console_blurred_as_gui_as_thread(q_application: QApplication):
        # def run_console_blurred_as_gui(q_application: QApplication):
        # def run_console_blurred_as_scheduler_as_thread(q_application: QApplication):
        # def run_console_blurred_as_scheduler(q_application: QApplication):
        # def run_console_blurred():
        # def run_loop_for_speak_as_async(ment):
        # def run_no_paste_memo(self):
        # def run_targets_promised():
        # def run_up_and_down_game():
        # def run(self):
        # def sanitized_input(user_input: str):
        # def save_all_list():
        # def save_macro_log(self, contents: str):
        # def search_animation_data_from_web(text_of_clicked_btn):
        # def search(self, word):
        # def select_db_toml(key):
        # def set_shortcut(self, btn_name_promised, function):
        # def set_shortcut(self, key_plus_key: str, function):
        # def shoot_custom_screenshot():
        # def shoot_full_screenshot():
        # def shoot_img_for_rpa():
        # def shoot_screenshot_custom(self):
        # def shoot_screenshot_for_rpa(self):
        # def shoot_screenshot_full(self):
        # def should_i_back_up_target():
        # def should_i_back_up_target(self):
        # def should_i_check_your_routine_before_coding():
        # def should_i_classify_special_files():
        # def should_i_connect_to_rdp1():
        # def should_i_connect_to_rdp1(self):
        # def should_i_download_youtube_as_webm_alt():
        # def should_i_download_youtube_as_webm_alt(self):
        # def should_i_download_youtube_as_webm():
        # def should_i_download_youtube_as_webm(self):
        # def should_i_empty_trash_can():
        # def should_i_empty_trash_can(self):
        # def should_i_enter_to_power_saving_mode():
        # def should_i_enter_to_power_saving_mode(self):
        # def should_i_exit_this_program():
        # def should_i_exit_this_program(self):
        # def should_i_find_direction_via_naver_map():
        # def should_i_find_direction_via_naver_map(self):
        # def should_i_gather_empty_directory():
        # def should_i_gather_special_files():
        # def should_i_gather_useless_files():
        # def should_i_merge_directories():
        # def should_i_reboot_this_computer():
        # def should_i_reboot_this_computer(self):
        # def should_i_record_macro():
        # def should_i_record_macro(self):
        # def should_i_run_targets_promised():
        # def should_i_show_animation_information_from_web():
        # def should_i_show_animation_information_from_web(self):
        # def should_i_shutdown_this_computer():
        # def should_i_shutdown_this_computer(self):
        # def should_i_speak_today_time_info():
        # def should_i_start_test_core():
        # def should_i_start_test(self):
        # def should_i_taskkill_useless_programs():
        # def should_i_translate_eng_to_kor():
        # def should_i_translate_eng_to_kor(self):
        # def should_i_translate_kor_to_eng():
        # def should_i_translate_kor_to_eng(self):
        # def show_weather_from_web(self):
        # def shutdown_this_computer():
        # def sleep(milliseconds):
        # def speak_after_x_min(mins: int):
        # def speak_alt_for_emergency(contents: str):
        # def speak_server_hh_mm():  # '몇 시야' or usr_input_txt == '몇시야':
        # def speak_server_ss():
        # def speak_that_service_is_in_preparing():
        # def speak_today_time_info():
        # def speak_without_async(ment):  # 많이 쓸 수록 프로그램이 느려진다
        # def speak(ment):
        # def stop_all_sounds():
        # def taskkill_useless_programs():
        # def taskkill(program_img_name):
        # def tmp(string: str):
        # def tmp2(q_application: QApplication):
        # def toogle_console_color(color_bg, colors_texts):
        # def toogle_rpa_window(self):
        # def translate_eng_to_kor_deprecated(request: str):
        # def translate_eng_to_kor(question: str):
        # def translate_kor_to_eng_deprecated(request: str):
        # def translate_kor_to_eng(question: str):
        # def trouble_shoot(trouble_id: str):
        # def update_db_toml(key, value):
        # def update_global_pkg_park4139_for_linux():
        # def update_label(self):
        # def update_os_sys_environment_variable(environment_variable_name: str, new_path: str):
        # def update_text_of_clicked_btn_and_close(self, text_of_clicked_button):
        # def update_text_of_clicked_btn(self, text_of_clicked_button):
        # def what_does_this_consist_of(text: str):
        # def write_fast(presses: str):
        # def write_slow(presses: str):
        # def xcopy_with_overwrite(target_abspath_from, future_target_abspath):
        #
        #
        #
        # 진행완료팝업,
        #     TIMER 기능
        #     개발배경 : 음악 듣거나, 애니볼때, 말로 하는게 시끄러워서
        #

        # 파일변경감지 아이디어
        # (이것 git으로 할 수 있잖아!)
        # 감지이벤트를 걸어 파일변경감지 시 비동기 빽업처리... 아 git 설치 안되있으면 안됨.

        # 파일 동기화 모듈로 로컬 1차 백업

        # 파일분류 기능
        # 이름에 [subplease] 가 있다면 [subplease] 디렉토리를 만들어 그곳으로 move_without_overwrite

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
        # - import 중 이름충돌 예상 시 as 사용 : 충돌의 소지가 있을 때 as 를 썻다. PEP8을 알고 지킨건 아니고 jetbrain IDE 의 가이드기능을 잘 따르다 보니, 잘 지켜졌다. : import blahblah as blah

        # 국내주식과 미국주식을 크롤링해서 보고 싶어졌다.
        # 몇 가지 라이브러리가 있음을 확인했고 기획하는 중이다.
        # 데이터수집장소 : 다양한 웹사이트에서 크롤링하여 데이터를 수집하기로 생각하였다, 신뢰도가 높아보이는 데이터를 수집해야 한다
        # 데이터신뢰도판단 : 네이버 금융정보 데이터신뢰도가 높다고 판단한 이유는 타블로그에서 정보를 얻었으며, 여러 이유 중 가장 큰 이유는 네이버의 공인력을 내가 믿기때문이다.)
        # 데이터수집방식 : 특정데이터는 네이버에서 직접 크롤링할 것. 웹 크롤링도 약간 늘었고, 데이터를 엑셀의 형태로 핸들링 하기 위해서 pandas 배워야 겠다. 잠깐만 기다려라 배워서 다시 오겠다.
        # import pykrx # 국내증권데이터 공유 라이브러리,               네이버금융사이트(실시간수정되는 주식데이터),               한국증권사이트 의 데이터 기반, 고신뢰성데이터 인 국내주식정보 를 볼 수 있다.  pykrx의 특징은 국내 주식만 수집이 가능한대신 yfinance보다 국내주식 시세가 정확하고 PER, PBR, 배당수익률과 같은 지표는 신뢰성이 떨어진다 - 출처: https://bigdata-doctrine.tistory.com/7 [경제와 데이터:티스토리]
        # import yfinance # 증권데이터 공유 라이브러리,              야후 파이낸스에서 크롤링한 데이터를 제공하는 라이브러리, 미국주식데이터 는 상대적으로 정확 , 국내주식데이터 의 잦은누락,   결론은 다른게 나아보인다.

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


content = r"""


처리할 코드는 여기에 작성


"""

error_cnt = 0
if __name__ == '__main__':
    try:
        test_loop_cnt = 1
        DebuggingUtil.commentize("TRYING TO ENTER TEST LOOP...")
        while True:  # test loop
            try:
                if test_loop_cnt == test_loop_limit + 1:
                    break
                DebuggingUtil.commentize(f" TEST LOOP {test_loop_cnt} STARTED")
                test_sprint_core()
                DebuggingUtil.commentize(f" TEST LOOP {test_loop_cnt} ENDED")

            except:
                print_with_test_status()
                continue
            test_loop_cnt = test_loop_cnt + 1
            # Park4139.sleep(milliseconds=1000)# 루프 텀 설정

        # 의도적 트러블 발생 테스트
        # raise shutil.Error("의도적 트러블 발생")
    except Exception as e:
        # print(str(e))
        # logger.info(f'logger: dst : {"??????"}')
        # logger.error(msg="에러발생?????")
        # logger.error(f'logger: str(e) : {"????????"}')
        # DebuggingUtil.trouble_shoot("%%%FOO%%%")
        traceback.print_exc(file=sys.stdout)
        error_cnt = error_cnt + 1
        error_str = traceback.format_exc()
        DebuggingUtil.debug_as_cli(f"TEST LOOP ERROR CNT REPORT:\nerror_cnt : {error_cnt}\nerror_str : {error_str}")
        # TestUtil.pause()

# 코드세그먼트 라이브스니펫
# 웹 크롤링
# import requests
# from bs4 import BeautifulSoup
#
# # 크롤링할 페이지의 URL
# url = 'https://wikidocs.net/book/4706'
#
# # 페이지 요청
# response = requests.get(url)
#
# # 요청이 성공했을 경우에만 크롤링 진행
# if response.status_code == 200:
#     # BeautifulSoup 객체 생성
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     # 모든 텍스트 출력
#     print(soup.get_text())
# else:
#     print('페이지 요청이 실패했습니다.')
