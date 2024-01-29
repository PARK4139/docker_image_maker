# -*- coding: utf-8 -*-  # python 3.x 하위버전 호환을 위한코드
__author__ = 'PARK4139 : Jung Hoon Park'
# alpine linux 로 컨버팅 중인 커스텀 패키지
import asyncio
import inspect
import json
import os
import random
import re
import shutil
import string
import subprocess
import sys
import threading
import time
import traceback
import urllib.parse as urllib_parser
from datetime import datetime, timedelta
from enum import Enum
from functools import partial
from pathlib import Path
from typing import Literal, Optional, TypeVar
from uuid import uuid4

import mutagen
import numpy
import pyglet
import send2trash
import toml
from bs4 import BeautifulSoup, ResultSet
from colorama import Fore
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from googletrans import Translator
from gtts import gTTS  # Google TTS 적용
from mutagen.mp3 import MP3
from pydantic import BaseModel, Field, field_validator, constr
from pytube import Playlist
from tqdm import tqdm

T = TypeVar('T')  # 타입 힌팅 설정


class StateManagementUtil:
    PROJECT_DIRECTORY = str(Path(__file__).parent.parent.absolute())  # __init__ 해당파일로 되어 있기 때문에. 위치가 복잡하게 되어 버렸다. 이를 __file__ 로 기준을 잡아서 경로를 수정하였다. 빌드를 하면서 알게되었는데 상대경로의 사용은 필연적인데, 상대경로로 경로를 설정할때 기준이 되는 절대경로 하나는 반드시 필요한 것 같다.
    GIT_HUB_ADDRESS = "https://github.com/PARK4139"
    EMPTY_DIRECTORYIES = rf"E:/[noe] [8TB] [local]/`/$empty_directories"
    # SPECIAL_DIRECTORY = rf"E:/[noe] [8TB] [local]"
    USELESS_DIRECTORIES = rf"E:/[noe] [8TB] [local]/`/$useless_directories"
    USERPROFILE = os.environ.get('USERPROFILE')  # 환경변수를 통해 데이터 보안 강화
    SERVICE_DIRECTORY = os.path.dirname(PROJECT_DIRECTORY)
    PARK4139_ARCHIVE_TOML = rf'{PROJECT_DIRECTORY}/park4139_archive.toml'
    SUCCESS_LOG = rf'{PROJECT_DIRECTORY}/success.log'
    LOCAL_PKG_CACHE_FILE = rf'{PROJECT_DIRECTORY}/pkg_park4139/__pycache__/__init__.cpython-312.pyc'
    MACRO_LOG = rf'{PROJECT_DIRECTORY}/$cache_log/macro.log'
    DIRSYNC_LOG = rf'{PROJECT_DIRECTORY}/$cache_log/dirsync.log'
    ICON_PNG = rf"{PROJECT_DIRECTORY}/$cache_png/icon.PNG"
    YT_DLP_CMD = rf"{PROJECT_DIRECTORY}/pkg_yt_dlp/yt-dlp.cmd"
    FFMPEG_EXE = rf"{PROJECT_DIRECTORY}/$cache_tools/dev_tools_exe/LosslessCut-win-x64/resources/ffmpeg.exe"
    JQ_WIN64_EXE = rf"{PROJECT_DIRECTORY}/pkg_jq/jq-win64.exe"
    DB_TOML = rf"{PROJECT_DIRECTORY}/$cache_database/db.toml"
    MUSIC_FOR_WORK = rf"{PROJECT_DIRECTORY}/$cache_work_for_music/PotPlayer64.dpl"
    RDP_82106_BAT = rf"{PROJECT_DIRECTORY}/$cache_prison/rdp-82106.bat"
    JSON_DIRECTORY = rf'{PROJECT_DIRECTORY}/$cache_json'
    DB_JSON = rf"{JSON_DIRECTORY}/db.json"
    NAV_ITEMS_JSON = rf"{JSON_DIRECTORY}/nav_items.json"
    MEMBERS_JSON = rf"{JSON_DIRECTORY}/members.json"
    LOG_DIRECTORY = rf'{PROJECT_DIRECTORY}/$cache_log'
    USELESS_FILES = rf"{PROJECT_DIRECTORY}/$cache_database/useless_file_names.txt"
    POP_SOUND_WAV = rf"{PROJECT_DIRECTORY}/$cache_sound/pop_sound.wav"
    PYCHARM64_EXE: str
    is_do_routine_processing = False
    # db_template = {
    # 'park4139_archive_log_line_cnt': 0,
    # }
    LINE_LENGTH_PROMISED = '_' * 59  # 제목작성 시 앞부분에 적용되는 기준인데 pep8 최대권장길이(79)를 기준으로 20 자 내외로 제목작성을 작성
    time_s = 0.0
    time_e = 0.0
    biggest_targets = []  # 300 MB 이상 빽업대상
    smallest_targets = []

    # speak() 쓰레드 상태관리용
    # is_speak_as_async_running = False
    pyglet_player = None
    playing_sounds = []
    previous_mp3_length_used_in_speak_as_async = 0

    routines_promised = [
        '물 한컵',
        '선풍기로 방환기 1분 이상',
        '세수',
        '로션',
        '아침식사',
        "프로폴리스 한알",
        '물가글(혹시 구내염 있으시면 가글양치)',
        '양치 WITHOUT TOOTH PASTE',
        '양치 WITH TOOTH PASTE',
        '양치 WITH GARGLE',
        '물가글',
        '즐거운일 1개',
        '스트레칭 밴드 V 유지 런지 30개',
        '계단 스쿼트 30 개',
        '푸쉬업 30 개',
        '점심식사',
        '저녁식사',
        # '음악틀기',
    ]
    count_of_make_me_go_to_sleep = []

    def __init__(self):

        try:
            # os.system('chcp 65001 >nul')
            BusinessLogicUtil.PYCHARM64_EXE = rf'{os.environ.get("PyCharm Community Edition").replace(";", "")}/pycharm64.exe'
        except AttributeError:
            pass
        except Exception:
            DebuggingUtil.trouble_shoot("%%%FOO%%%")


class ColoramaColorUtil(Enum):
    RED = "RED"
    GREEN = "GREEN"
    BLACK = "BLACK"
    YELLOW = "YELLOW"
    BLUE = "BLUE"
    MAGENTA = "MAGENTA"
    CYAN = "CYAN"
    WHITE = "WHITE"
    RESET = "RESET"
    LIGHTBLACK_EX = "LIGHTBLACK_EX"
    LIGHTRED_EX = "LIGHTRED_EX"
    LIGHTGREEN_EX = "LIGHTGREEN_EX"
    LIGHTYELLOW_EX = "LIGHTYELLOW_EX"
    LIGHTBLUE_EX = "LIGHTBLUE_EX"
    LIGHTMAGENTA_EX = "LIGHTMAGENTA_EX"
    LIGHTCYAN_EX = "LIGHTCYAN_EX"
    LIGHTWHITE_EX = "LIGHTWHITE_EX"


class TestUtil:
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
        BusinessLogicUtil.print_today_time_info()
        os.system('pause >nul')

    @staticmethod
    def measure_seconds_performance_nth(function):
        """시간성능 측정 데코레이터 코드"""

        # def wrapper(*args, **kwargs):
        def wrapper(**kwargs):  # **kwargs, keyword argument, dictionary 로 parameter 를 받음. named parameter / positional parameter 를 받을 사용가능?
            # def wrapper(*args):# *args, arguments, tuple 로 parameter 를 받음.
            # def wrapper():
            DebuggingUtil.print_ment_via_colorama("___________________________________________________________ TEST START", colorama_color=ColoramaColorUtil.LIGHTWHITE_EX)
            n = 5  # 테스트 루프 반복 횟수 설정
            if TestUtil.is_first_test_lap:
                ment = rf"총 {n}번의 시간성능측정 테스트를 시도합니다"
                TestUtil.is_first_test_lap = False
                DebuggingUtil.print_ment_via_colorama(ment, colorama_color=ColoramaColorUtil.BLUE)
                TextToSpeechUtil.speak_ment(ment=ment, sleep_after_play=1)
            seconds_performance_test_results = TestUtil.test_results
            import time
            time_s = time.time()
            # function(*args, **kwargs)
            function(**kwargs)
            # function(*args)
            # function()
            time_e = time.time()
            mesured_seconds = time_e - time_s
            seconds_performance_test_results.append(f"{round(mesured_seconds, 2)}sec")
            if len(seconds_performance_test_results) == n:
                ment = rf"총 {n}번의 시간성능측정 테스트가 성공 되었습니다"
                TextToSpeechUtil.speak_ment(ment=ment, sleep_after_play=0.55)
                DebuggingUtil.print_ment_via_colorama(rf'seconds_performance_test_results = {seconds_performance_test_results}', colorama_color=ColoramaColorUtil.BLUE)
                DebuggingUtil.print_ment_via_colorama(rf'type(seconds_performance_test_results) : {type(seconds_performance_test_results)}', colorama_color=ColoramaColorUtil.BLUE)
                DebuggingUtil.print_ment_via_colorama(rf'len(seconds_performance_test_results) : {len(seconds_performance_test_results)}', colorama_color=ColoramaColorUtil.BLUE)
                DebuggingUtil.print_ment_via_colorama("___________________________________________________________ TEST END", colorama_color=ColoramaColorUtil.LIGHTWHITE_EX)
                TestUtil.pause()

        return wrapper

    @staticmethod
    def measure_seconds_performance_once(function):
        """시간성능 측정 데코레이터 코드"""

        # def wrapper(*args, **kwargs):
        def wrapper(**kwargs):  # **kwargs, keyword argument, dictionary 로 parameter 를 받음. named parameter / positional parameter 를 받을 사용가능?
            # def wrapper(*args):# *args, arguments, tuple 로 parameter 를 받음.
            # def wrapper():
            DebuggingUtil.print_ment_via_colorama("___________________________________________________________ TEST START", colorama_color=ColoramaColorUtil.LIGHTWHITE_EX)
            if TestUtil.is_first_test_lap:
                TestUtil.is_first_test_lap = False
            seconds_performance_test_results = TestUtil.test_results
            import time
            time_s = time.time()
            # function(*args, **kwargs)
            function(**kwargs)
            # function(*args)
            # function()
            time_e = time.time()
            mesured_seconds = time_e - time_s
            DebuggingUtil.print_ment_via_colorama(rf'mesured_seconds = {round(mesured_seconds, 2)}', colorama_color=ColoramaColorUtil.BLUE)
            DebuggingUtil.print_ment_via_colorama("___________________________________________________________ TEST END", colorama_color=ColoramaColorUtil.LIGHTWHITE_EX)

        return wrapper

    @staticmethod
    def measure_milliseconds_performance(function):
        """시간성능 측정 코드"""

        def wrapper():
            # def wrapper(*args):# *args, arguments, tuple 로 parameter 를 받음.
            # def wrapper(*args, **kwargs):
            DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
            test_cycle_max_limit = 5
            milliseconds_performance_test_result = []
            import time
            time_s = time.time()
            function()
            # function(*args)
            # function(**kwargs)
            # function(*args, **kwargs)
            time_e = time.time()
            mesured_seconds = time_e - time_s
            DebuggingUtil.commentize(rf"시간성능측정 결과")
            milliseconds_performance_test_result.append(round(mesured_seconds * 1000, 5))
            print(rf'milliseconds_performance_test_result : {milliseconds_performance_test_result}')
            print(rf'type(milliseconds_performance_test_result) : {type(milliseconds_performance_test_result)}')
            print(rf'len(milliseconds_performance_test_result) : {len(milliseconds_performance_test_result)}')
            if len(milliseconds_performance_test_result) == test_cycle_max_limit:
                TextToSpeechUtil.speak_ments("시간성능측정이 성공 되었습니다", sleep_after_play=0.65)
                TestUtil.pause()

        return wrapper


class TextToSpeechUtil:
    @staticmethod
    def is_containing_kor(text):
        pattern = "[ㄱ-ㅎ가-힣]"
        if re.search(pattern, text):
            return True
        else:
            return False

    @staticmethod
    def is_containing_special_characters_without_thread(text: str):
        pattern = "[~!@#$%^&*()_+|<>?:{}]"  # , 는 제외인가?
        if re.search(pattern, text):
            return True

    @staticmethod
    def is_containing_special_characters_with_thread(text: str):
        # 비동기 처리 설정 ( advanced  )
        nature_numbers = [n for n in range(1, 101)]  # from 1 to 100
        work_quantity = len(text)
        n = 4  # thread_cnt # interval_cnt
        d = work_quantity // n  # interval_size
        r = work_quantity % n
        start_1 = 0
        end_1 = d - 1
        starts = [start_1 + (n - 1) * d for n in nature_numbers[:n]]  # 등차수열 공식
        ends = [end_1 + (n - 1) * d for n in nature_numbers[:n]]
        remained_start = ends[-1] + 1
        remained_end = work_quantity

        # print(rf'nature_numbers : {nature_numbers}')  # 원소의 길이의 합이 11넘어가면 1에서 3까지만 표기 ... 의로 표시 그리고 마지막에서 3번째에서 마지막에서 0번째까지 표기 cut_list_proper_for_pretty()
        # print(rf'work_quantity : {work_quantity}')
        # print(rf'n : {n}')
        # print(rf'd : {d}')
        # print(rf'r : {r}')
        # print(rf'start_1 : {start_1}')
        # print(rf'end_1 : {end_1}')
        # print(rf'starts : {starts}')
        # print(rf'ends : {ends}')
        # print(rf'remained_start : {remained_start}')
        # print(rf'remained_end : {remained_end}')

        # 비동기 이벤트 함수 설정 ( advanced  )
        async def is_containing_special_characters(start_index: int, end_index: int, text: str):
            pattern = "[~!@#$%^&*()_+|<>?:{}]"  # , 는 제외인가?
            if re.search(pattern, text[start_index:end_index]):
                # print(f"쓰레드 {start_index}에서 {end_index}까지 작업 성공 True return")
                result_list.append(True)
                # return True
            else:
                result_list.append(False)
                # print(f"쓰레드 {start_index}에서 {end_index}까지 작업 성공 False return")
                # return False

        # 비동기 이벤트 루프 설정
        def run_async_event_loop(start_index: int, end_index: int, text: str):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(is_containing_special_characters(start_index, end_index, text))

        # 스레드 객체를 저장할 리스트 생성
        threads = []

        # 각 스레드의 결과를 저장할 리스트
        # result_list = [None] * work_quantity
        result_list = []

        # 주작업 처리용 쓰레드
        for n in range(0, n):
            start_index = starts[n]
            end_index = ends[n]
            thread = threading.Thread(target=run_async_event_loop, args=(start_index, end_index, text))
            thread.start()
            threads.append(thread)

        # 남은 작업 처리용 쓰레드
        if remained_end <= work_quantity:
            start_index = remained_start
            end_index = remained_end
            thread = threading.Thread(target=run_async_event_loop, args=(start_index, end_index, text))
            thread.start()
            threads.append(thread)
        else:
            start_index = remained_start
            end_index = start_index  # end_index 를 start_index 로 하면 될 것 같은데 테스트필요하다.
            thread = threading.Thread(target=run_async_event_loop, args=(start_index, end_index, text))
            thread.start()
            threads.append(thread)

        # 모든 스레드의 작업이 종료될 때까지 대기
        for thread in threads:
            thread.join()

        # 먼저 종료된 스레드가 있는지 확인하고, 나머지 스레드 중지
        # for thread in threads:
        #     if not thread.is_alive():
        #         for other_thread in threads:
        #             if other_thread != thread:
        #                 other_thread.cancel()
        #         break

        # 바뀐 부분만 결과만 출력, 전체는 abspaths_and_mtimes 에 반영됨
        print(rf'result_list : {result_list}')
        print(rf'type(result_list) : {type(result_list)}')
        print(rf'len(result_list) : {len(result_list)}')

        if all(result_list):
            print("쓰레드 작업결과 result_list의 모든 요소가 True이므로 True를 반환합니다")
            return True
        else:
            print("쓰레드 작업결과 result_list에 False인 요소가 있어 False를 반환합니다")

    @staticmethod
    def is_containing_jpn(text):
        # pattern = r"^[\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Han}ー〜・]+$"
        # pattern = r"^\P{Script=Hiragana}\P{Script=Katakana}\P{Script=Han}ー〜・]+$"
        # pattern = r"^[\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Han}ー〜・]+$"
        # pattern = r"^[^\p{Script=Hiragana}^\p{Script=Katakana}^\p{Script=Han}ー〜・]+$"
        # pattern = r"^[^\p{Script=Hiragana}^\p{Script=Katakana}^\p{Script=Han}ー〜・]+$"
        pattern = r"^[^\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFFー〜・]+$"
        if re.search(pattern, text, flags=re.U):
            return True
        else:
            return False

    @staticmethod
    def is_containing_eng(text):
        pattern = "[a-zA-Z]"
        if re.search(pattern, text):
            return True
        else:
            return False

    @staticmethod
    def is_containing_number(text):
        pattern = "[0-9]"
        if re.search(pattern, text):
            return True
        else:
            return False

    @staticmethod
    def is_only_no(text):
        pattern = "^[0-9]+$"
        if re.search(pattern, text):
            return True
        else:
            return False

    @staticmethod
    def is_only_speacial_characters(text):
        pattern = "^[~!@#$%^&*()_+|<>?:{}]+$"
        if re.search(pattern, text):
            return True
        else:
            return False

    @staticmethod
    def is_only_eng_and_kor_and_no_and_speacial_characters(text):
        pattern = "^[ㄱ-ㅎ가-힣0-9a-zA-Z~!@#$%^&*()_+|<>?:{}]+$"
        if re.search(pattern, text):
            return True
        else:
            return False

    @staticmethod
    def is_only_eng_and_no_and_speacial_characters(text):
        pattern = "^[0-9a-zA-Z~!@#$%^&*()_+|<>?:{}]+$"
        if re.search(pattern, text):
            return True
        else:
            return False

    @staticmethod
    def is_only_eng_and_speacial_characters(text):
        pattern = "^[a-zA-Z~!@#$%^&*()_+|<>?:{}]+$"
        if re.search(pattern, text):
            return True
        else:
            return False

    @staticmethod
    def is_only_eng_and_no(text):
        pattern = "^[0-9a-zA-Z]+$"
        if re.search(pattern, text):
            return True
        else:
            return False

    @staticmethod
    def is_only_eng(text):
        pattern = "^[a-zA-Z]+$"
        if re.search(pattern, text):
            return True
        else:
            return False

    @staticmethod
    def is_eng_or_kor_ja(text: str):
        """
        한글처리 :
            한영숫특 :
            한숫특 :
            한숫
            한특
            숫특
            특
            숫
        영어처리 :
            영숫특
            영특
            영숫
            영
        일어처리 :
        빠진거있나? 일단 여기까지

        문자구성 판별기가 필요하다
            return "eng, kor, jap, special_characters ", ... 이런식 > what_does_this_consist_of() 를 만들었다.
        """
        if TextToSpeechUtil.is_only_speacial_characters(text=text):
            return "ko"
        elif TextToSpeechUtil.is_only_no(text=text):
            return "ko"
        elif TextToSpeechUtil.is_containing_kor(text=text):
            return "ko"
        if TextToSpeechUtil.is_only_eng_and_no_and_speacial_characters(text=text):
            return "en"
        elif TextToSpeechUtil.is_only_eng_and_speacial_characters(text=text):
            return "en"
        elif TextToSpeechUtil.is_only_eng_and_no(text=text):
            return "en"
        elif TextToSpeechUtil.is_only_eng(text=text):
            return "en"
        else:
            return "ko"

    @staticmethod
    def what_does_this_consist_of(text: str):
        result = []
        if TextToSpeechUtil.is_containing_kor(text=text):
            result.append("kor")
        if TextToSpeechUtil.is_containing_eng(text=text):
            result.append("eng")
        if TextToSpeechUtil.is_containing_number(text=text):
            result.append("number")
        if TextToSpeechUtil.is_containing_special_characters_with_thread(text=text):
            result.append("special_characters")
        if TextToSpeechUtil.is_containing_jpn(text=text):
            result.append("jpn")
        print(rf'text : {text}')
        print(rf'result : {result}')
        return result

    @staticmethod
    def get_length_of_mp3(target_abspath: str):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        try:
            audio = MP3(target_abspath)
            return audio.info.length
        except mutagen.MutagenError:
            # DebuggingUtil.trouble_shoot("%%%FOO%%%") # gtts 모듈 불능? mutagen 모듈 불능? license 찾아보자 으로 어쩔수 없다.
            return
        except Exception:
            DebuggingUtil.trouble_shoot("%%%FOO%%%")

    @staticmethod
    def run_loop_for_speak_as_async_deprecated(ment):
        async def speak_as_async(ment):
            DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
            # pyglet_player 가 play() 하고 있으면 before_mp3_length_used_in_speak_as_async 만큼 대기
            DebuggingUtil.print_ment_magenta(rf'before_mp3_length_used_in_speak_as_async 만큼 재생 대기')

            # Park4139.pyglet_player 을 del 을 한 경우:
            # Park4139.pyglet_player 에 대한 참조가 불가능해진다. 다른 참조법을 적용해보자. 시도해보니 Park4139.pyglet_player 는 더이상 쓸 수가 없다.
            # 재활용해야하는 Park4139.pyglet_player는 더이상 쓸 수 없어졌다.
            if StateManagementUtil.pyglet_player == None:
                StateManagementUtil.pyglet_player = pyglet.media.Player()
            # if hasattr(Park4139, 'pyglet_player') and Park4139.pyglet_player is None:
            #     # Park4139.pyglet_player가 None인 경우
            #     Park4139.pyglet_player = pyglet.media.Player()
            #     pass
            if StateManagementUtil.pyglet_player != None:
                if StateManagementUtil.pyglet_player.playing == True:
                    length_of_mp3 = BusinessLogicUtil.previous_mp3_length_used_in_speak_as_async
                    time.sleep(length_of_mp3 * 0.65)  # 이렇면 소리가 겹치지 않는 장점이 있으나, 실제로 일을 미리하고 나중에 보고하는 단점이 있다
                    # asyncio.sleep(length_of_mp3 * 0.65) # 이렇면 실제로 일을 하자마자 보고하는 장점이 있으나, 소리가 겹치는 않는 단점이 있다
                    # time.sleep(length_of_mp3 * 0.75)
                    # time.sleep(length_of_mp3 * 0.85)
                    # time.sleep(length_of_mp3 * 0.95)
                    # time.sleep(length_of_mp3 * 1.05)
                    # time.sleep(length_of_mp3 * 1.00)
            try:
                while True:
                    if type(ment) == str:
                        # while Park4139.is_speak_as_async_running:
                        #     Park4139.debug_as_cli(f"def {inspect.currentframe().f_code.co_name}() 에 대한 다른 쓰레드를 기다리는 중입니다")
                        #     pass
                        # Park4139.is_speak_as_async_running = True # 쓰레드상태 사용 중으로 업데이트

                        cache_mp3 = rf'{StateManagementUtil.PROJECT_DIRECTORY}\$cache_mp3'
                        FileSystemUtil.make_leaf_directory(leaf_directory_abspath=cache_mp3)

                        DebuggingUtil.print_ment_magenta("ment 전처리, 윈도우 경로명에 들어가면 안되는 문자들 공백으로 대체")
                        ment = BusinessLogicUtil.get_str_replaced_special_characters(target=ment, replacement=" ")
                        ment = ment.replace("\n", " ")

                        DebuggingUtil.print_ment_magenta(rf'파일 없으면 생성')
                        ment__mp3 = rf'{cache_mp3}\{ment}_.mp3'
                        ment_mp3 = rf'{cache_mp3}\{ment}.mp3'
                        if not os.path.exists(ment_mp3):
                            if not os.path.exists(ment__mp3):
                                if "special_characters" in TextToSpeechUtil.what_does_this_consist_of(text=ment):
                                    gtts = gTTS(text=ment, lang='ko')
                                    gtts.save(ment__mp3)
                                elif "kor" in TextToSpeechUtil.what_does_this_consist_of(text=ment):
                                    gtts = gTTS(text=ment, lang='ko')
                                    gtts.save(ment__mp3)
                                elif "eng" in TextToSpeechUtil.what_does_this_consist_of(text=ment):
                                    gtts = gTTS(text=ment, lang='en')
                                    gtts.save(ment__mp3)
                                elif "jpn" in TextToSpeechUtil.what_does_this_consist_of(text=ment):
                                    gtts = gTTS(text=ment, lang='ja')
                                    gtts.save(ment__mp3)
                                else:
                                    gtts = gTTS(text=ment, lang='ko')
                                    gtts.save(ment__mp3)

                        try:
                            # 앞부분 소리가 들리지 않는 현상 해결 아이디어.
                            # 앞부분의 단어가 들리지 않은채로 음악파일의 중간부터가 소리가 들린다. 전체 소리가 다 들려야 하는데.
                            # 음악파일의 앞부분에 빈소리를 추가해주려고 한다. ffmpeg를 이용하여 silent.mp3(1초간 소리가 없는 mp3 파일)을 소리를 재생해야할 mp3 파일의 앞부분에 합쳐서 재생시도.
                            silent_mp3 = rf"{cache_mp3}\silent.mp3"
                            if not os.path.exists(silent_mp3):
                                BusinessLogicUtil.debug("사일런트 mp3 파일이 없습니다")
                                break
                            if not os.path.exists(ment_mp3):
                                cmd = rf'echo y | "ffmpeg" -i "concat:{os.path.abspath(silent_mp3)}|{os.path.abspath(ment__mp3)}" -acodec copy -metadata "title=Some Song" "{os.path.abspath(ment_mp3)}" -map_metadata 0:-1  >nul 2>&1'
                                FileSystemUtil.get_cmd_output(cmd)
                        except Exception:
                            DebuggingUtil.trouble_shoot("%%%FOO%%%")

                        try:
                            # 자꾸 프로세스 세션을 빼앗기 때문에 불편한 코드
                            # os.system(rf'start /b cmd /c call "{ment_mp3}" >nul 2>&1')

                            # 프로세스 세션을 빼앗지 않고 mp3재생하는 다른 방법
                            # playsound.playsound(os.path.abspath(ment_mp3))

                            # Park4139.debug_as_cli(rf'프로세스 세션을 빼앗지 않고 mp3재생')
                            ment_mp3 = os.path.abspath(ment_mp3)
                            DebuggingUtil.print_ment_magenta(rf'{ment_mp3}')
                            try:
                                # 재생
                                # pyglet_player = Park4139.pyglet_player

                                pyglet_player = pyglet.media.Player()
                                source = pyglet.media.load(ment_mp3)
                                # Park4139.multiprocessed_source_play = source
                                pyglet_player.queue(source)

                                # 재생추적

                                # 재생 중인 사운드 리소스를 추적하는 이벤트 핸들러 함수
                                def on_player_eos():
                                    player = pyglet.media.Player()
                                    playing_sounds.remove(player)

                                pyglet_player.push_handlers(on_eos=on_player_eos)
                                # pyglet_player.play()  # 이거 재생 안되는데, 이게 공식문서에 나온 방식인데, media 객채 생성 순서가 문제였나 보다.이젠 된다
                                pyglet_player.play()
                                source.play()  # 웃긴다 이거 이렇게는 재생이 된다.
                                playing_sounds = StateManagementUtil.playing_sounds
                                playing_sounds.append(pyglet_player)
                                # 사운드 재생을 시작할 때마다 이벤트 핸들러를 등록하여 playing_sounds 리스트에 추가

                                # FAIL
                                # import  multiprocessing
                                # Park4139.multiprocessed_source_play = multiprocessing.Process(target= source.play , args=None)
                                # Park4139.multiprocessed_source_play.start()

                                if StateManagementUtil.pyglet_player.playing == False:
                                    StateManagementUtil.pyglet_player = None
                                    BusinessLogicUtil.previous_mp3_length_used_in_speak_as_async = 0

                                # Park4139.is_speak_as_async_running = False # 쓰레드상태 사용종료로 업데이트
                            except FileNotFoundError:
                                DebuggingUtil.print_ment_magenta(f"{ment_mp3} 재생할 파일이 없습니다")
                            except:
                                DebuggingUtil.trouble_shoot("%%%FOO%%%")
                                return

                            DebuggingUtil.commentize("before_mp3_length_used_in_speak_as_async 업데이트")
                            length_of_mp3 = round(float(TextToSpeechUtil.get_length_of_mp3(ment_mp3)), 1)
                            BusinessLogicUtil.previous_mp3_length_used_in_speak_as_async = length_of_mp3

                        except Exception:
                            DebuggingUtil.trouble_shoot("%%%FOO%%%")

                        # Park4139.debug_as_cli(rf'불필요 파일 삭제')
                        os.system(f'echo y | del /f "{ment__mp3}" >nul 2>&1')

                        # Park4139.debug_as_cli(rf'중간로깅')
                        return
                    return
            except Exception:
                DebuggingUtil.trouble_shoot("%%%FOO%%%")

        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(speak_as_async(ment))

    @staticmethod
    def speak_ments(ment, sleep_after_play=1.00, thread_join_mode=False):
        # if thread_for_speak_as_async is not None:
        #     # 이전에 생성된 쓰레드가 있다면 종료
        #     thread_for_speak_as_async.join()

        # 이미 실행 중인 speak()관련 쓰레드가 있다면 종료시킴
        # if threading.Event() != None:
        #     global exit_event
        #     exit_event = threading.Event()
        # else:
        #     exit_event.set()
        #     exit_event.clear()  # 종료 이벤트 객체 초기화

        # pyglet을 실행하는 스레드 종료
        # Park4139.kill_thread(thread_name="thread_for_speak")
        # Park4139.kill_thread(thread_name="thread_for_run_loop_for_speak_as_async")

        # 재생 중인 사운드 리소스를 중지하는 함수
        def stop_all_sounds():
            playing_sounds = StateManagementUtil.playing_sounds
            for player in playing_sounds:
                player.pause()  # 또는 player.stop()

        stop_all_sounds()
        if StateManagementUtil.pyglet_player != None:
            # if Park4139.pyglet_player.playing == True:
            # pyglet.app.exit()
            # Park4139.pyglet_player.delete()
            # Park4139.pyglet_player = None
            # Park4139.pyglet_player.pause()
            # pyglet.app.platform_event_loop.pause()
            # Park4139.pyglet_player.pause()
            # Park4139.pyglet_player.delete()

            # Park4139.pyglet_player 을 del 을 한 경우. 의도한대로 pyglet 의 play() 동작은 중지가 되는데.
            # Park4139.pyglet_player 에 대한 참조가 불가능해진다. 다른 참조법을 적용해보자. 시도해보니 Park4139.pyglet_player 는 더이상 쓸 수가 없다.
            # 재활용해야하는 Park4139.pyglet_player는 더이상 쓸 수 없어졌다.
            # del Park4139.pyglet_player
            # 혹시 몰라서 tmp 변수에 참조시켜서 del 시도 해보았는데, Park4139.pyglet_player에 대해 참조는 가능해 보인다.
            # tmp = Park4139.pyglet_player
            # del tmp
            # del 쓰는 것을 포기하자

            # TBD
            # sound = pyglet.resource.media('sound.wav')
            # sound.stop()
            pass
        else:
            import pyglet
            StateManagementUtil.pyglet_player = pyglet.media.Player()
            if StateManagementUtil.pyglet_player.playing == True:
                StateManagementUtil.pyglet_player.pause()
                # Park4139.pyglet_player.delete()
                # del Park4139.pyglet_player
                # tmp = Park4139.pyglet_player

        # 비동기 이벤트 함수 설정 (simple for void async processing)
        async def process_thread_speak(ment):
            # while not exit_event.is_set(): # 쓰레드 이벤트 제어
            DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
            ment = str(ment)
            ment = ment.strip()
            if ment == "":
                return None
            if TextToSpeechUtil.is_containing_special_characters_with_thread(text=ment):
                ment = TextToSpeechUtil.remove_special_characters(text=ment)
            while True:
                ments = [x.strip() for x in ment.replace(".", ",").split(",")]  # from "abc,abc.abc,abc." to ["abc","abc","abc","abc"] # , or . 를 넣으면 나누어 읽도록 업데이트
                ments = [x for x in ments if x.strip()]  # 리스트 요소 "" 제거,  from ["", A] to [A]
                # [print(sample) for sample in ments ]
                # print(rf'ments : {ments}')
                # print(rf'type(ments) : {type(ments)}')
                # print(rf'len(ments) : {len(ments)}')
                for ment in ments:
                    # Park4139Park4139.Tts.speak(ment)
                    # thread = threading.Thread(target=partial(Park4139Park4139.Tts.run_loop_for_speak_as_async, ment), name ="thread_for_run_loop_for_speak_as_async")
                    # thread.start()
                    # if thread.is_alive():
                    #     thread.join()
                    TextToSpeechUtil.speak_ment_without_async_and_return_last_word_mp3_length(ment, sleep_after_play=sleep_after_play)
                    pass
                return None

        # 비동기 이벤트 루프 설정 (simple for void async processing)
        def process_thread_loop(ment):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(process_thread_speak(ment))

        # 비동기 이벤트 루프 실행할 쓰레드 설정 (simple for void async processing)
        thread = threading.Thread(target=partial(process_thread_loop, ment), name="thread_for_speak")  # Q: 왜 thread.name 의 case 는 다른거야 ?  wrtn: 네, 스레드의 이름은 일반적으로 대소문자를 구분하지 않습니다.
        thread.start()
        if thread_join_mode == True:
            thread.join()

    @staticmethod
    def speak_ment(ment, sleep_after_play=1.00):  # 많이 쓸 수록 프로그램이 느려진다
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        ment = str(ment)
        ment = ment.strip()
        if TextToSpeechUtil.is_containing_special_characters_without_thread(text=ment):
            ment = TextToSpeechUtil.remove_special_characters(text=ment)
        if ment == "":
            return None
        try:
            while True:
                ments = []
                if "," in ment:  # , 를 넣으면 나누어 읽도록 업데이트
                    ments = ment.split(",")
                    for ment in ments:
                        DebuggingUtil.print_ment_magenta(ment)
                    break
                if type(ment) == str:
                    cache_mp3 = rf'{StateManagementUtil.PROJECT_DIRECTORY}\$cache_mp3'
                    FileSystemUtil.make_leaf_directory(leaf_directory_abspath=cache_mp3)

                    DebuggingUtil.print_ment_magenta("ment 전처리, 윈도우 경로명에 들어가면 안되는 문자들 공백으로 대체")
                    ment = BusinessLogicUtil.get_str_replaced_special_characters(target=ment, replacement=" ")
                    ment = ment.replace("\n", " ")

                    DebuggingUtil.print_ment_magenta(rf'파일 없으면 생성')
                    ment__mp3 = rf'{cache_mp3}\{ment}_.mp3'
                    ment_mp3 = rf'{cache_mp3}\{ment}.mp3'
                    if not os.path.exists(ment_mp3):
                        if not os.path.exists(ment__mp3):
                            if "special_characters" in TextToSpeechUtil.what_does_this_consist_of(text=ment):
                                gtts = gTTS(text=ment, lang='ko')
                                gtts.save(ment__mp3)
                            elif "kor" in TextToSpeechUtil.what_does_this_consist_of(text=ment):
                                gtts = gTTS(text=ment, lang='ko')
                                gtts.save(ment__mp3)
                            elif "eng" in TextToSpeechUtil.what_does_this_consist_of(text=ment):
                                gtts = gTTS(text=ment, lang='en')
                                gtts.save(ment__mp3)
                            elif "jpn" in TextToSpeechUtil.what_does_this_consist_of(text=ment):
                                gtts = gTTS(text=ment, lang='ja')
                                gtts.save(ment__mp3)
                            else:
                                gtts = gTTS(text=ment, lang='ko')
                                gtts.save(ment__mp3)
                    try:
                        silent_mp3 = rf"{cache_mp3}\silent.mp3"
                        if not os.path.exists(silent_mp3):
                            BusinessLogicUtil.debug("사일런트 mp3 파일이 없습니다")
                            break
                        if not os.path.exists(ment_mp3):
                            cmd = rf'echo y | "ffmpeg" -i "concat:{os.path.abspath(silent_mp3)}|{os.path.abspath(ment__mp3)}" -acodec copy -metadata "title=Some Song" "{os.path.abspath(ment_mp3)}" -map_metadata 0:-1  >nul 2>&1'
                            FileSystemUtil.get_cmd_output(cmd)
                    except Exception:
                        DebuggingUtil.trouble_shoot("%%%FOO%%%")
                    try:
                        ment_mp3 = os.path.abspath(ment_mp3)
                        DebuggingUtil.print_ment_magenta(rf'{ment_mp3}')
                        try:
                            source = pyglet.media.load(ment_mp3)
                            source.play()

                            length_of_mp3 = TextToSpeechUtil.get_length_of_mp3(ment_mp3)
                            time.sleep(length_of_mp3 * sleep_after_play)
                            return length_of_mp3
                        except FileNotFoundError:
                            DebuggingUtil.print_ment_magenta(f"{ment_mp3} 재생할 파일이 없습니다")
                        except:
                            DebuggingUtil.trouble_shoot("%%%FOO%%%")
                            break
                        DebuggingUtil.commentize("before_mp3_length_used_in_speak_as_async 업데이트")
                        length_of_mp3 = round(float(TextToSpeechUtil.get_length_of_mp3(ment_mp3)), 1)
                        BusinessLogicUtil.previous_mp3_length_used_in_speak_as_async = length_of_mp3
                    except Exception:
                        DebuggingUtil.trouble_shoot("%%%FOO%%%")

                    os.system(f'echo y | del /f "{ment__mp3}" >nul 2>&1')
                break
        except Exception:
            DebuggingUtil.trouble_shoot("%%%FOO%%%")

    @staticmethod
    def speak_ment_without_async_and_return_last_word_mp3_length(ment, sleep_after_play=1.00):  # 많이 쓸 수록 프로그램이 느려진다
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        ment = str(ment)
        ment = ment.strip()
        if TextToSpeechUtil.is_containing_special_characters_with_thread(text=ment):
            ment = TextToSpeechUtil.remove_special_characters(text=ment)
        if ment == "":
            return None
        try:
            while True:
                ments = []
                if "," in ment:  # , 를 넣으면 나누어 읽도록 업데이트
                    ments = ment.split(",")
                    for ment in ments:
                        DebuggingUtil.print_ment_magenta(ment)
                    break
                if type(ment) == str:
                    # while Park4139.is_speak_as_async_running:
                    #     Park4139.debug_as_cli(f"def {inspect.currentframe().f_code.co_name}() 에 대한 다른 쓰레드를 기다리는 중입니다")
                    #     pass
                    # Park4139.is_speak_as_async_running = True # 쓰레드상태 사용 중으로 업데이트

                    cache_mp3 = rf'{StateManagementUtil.PROJECT_DIRECTORY}\$cache_mp3'
                    FileSystemUtil.make_leaf_directory(leaf_directory_abspath=cache_mp3)

                    DebuggingUtil.print_ment_magenta("ment 전처리, 윈도우 경로명에 들어가면 안되는 문자들 공백으로 대체")
                    ment = BusinessLogicUtil.get_str_replaced_special_characters(target=ment, replacement=" ")
                    ment = ment.replace("\n", " ")

                    DebuggingUtil.print_ment_magenta(rf'파일 없으면 생성')
                    ment__mp3 = rf'{cache_mp3}\{ment}_.mp3'
                    ment_mp3 = rf'{cache_mp3}\{ment}.mp3'
                    if not os.path.exists(ment_mp3):
                        if not os.path.exists(ment__mp3):
                            if "special_characters" in TextToSpeechUtil.what_does_this_consist_of(text=ment):
                                gtts = gTTS(text=ment, lang='ko')
                                gtts.save(ment__mp3)
                            elif "kor" in TextToSpeechUtil.what_does_this_consist_of(text=ment):
                                gtts = gTTS(text=ment, lang='ko')
                                gtts.save(ment__mp3)
                            elif "eng" in TextToSpeechUtil.what_does_this_consist_of(text=ment):
                                gtts = gTTS(text=ment, lang='en')
                                gtts.save(ment__mp3)
                            elif "jpn" in TextToSpeechUtil.what_does_this_consist_of(text=ment):
                                gtts = gTTS(text=ment, lang='ja')
                                gtts.save(ment__mp3)
                            else:
                                gtts = gTTS(text=ment, lang='ko')
                                gtts.save(ment__mp3)

                    try:
                        # 앞부분 소리가 들리지 않는 현상 해결 아이디어.
                        # 앞부분의 단어가 들리지 않은채로 음악파일의 중간부터가 소리가 들린다. 전체 소리가 다 들려야 하는데.
                        # 음악파일의 앞부분에 빈소리를 추가해주려고 한다. ffmpeg를 이용하여 silent.mp3(1초간 소리가 없는 mp3 파일)을 소리를 재생해야할 mp3 파일의 앞부분에 합쳐서 재생시도.
                        silent_mp3 = rf"{cache_mp3}\silent.mp3"
                        if not os.path.exists(silent_mp3):
                            BusinessLogicUtil.debug("사일런트 mp3 파일이 없습니다")
                            break
                        if not os.path.exists(ment_mp3):
                            cmd = rf'echo y | "ffmpeg" -i "concat:{os.path.abspath(silent_mp3)}|{os.path.abspath(ment__mp3)}" -acodec copy -metadata "title=Some Song" "{os.path.abspath(ment_mp3)}" -map_metadata 0:-1  >nul 2>&1'
                            FileSystemUtil.get_cmd_output(cmd)
                    except Exception:
                        DebuggingUtil.trouble_shoot("%%%FOO%%%")

                    try:
                        # 자꾸 프로세스 세션을 빼앗기 때문에 불편한 코드
                        # os.system(rf'start /b cmd /c call "{ment_mp3}" >nul 2>&1')

                        # 프로세스 세션을 빼앗지 않고 mp3재생하는 다른 방법
                        # playsound.playsound(os.path.abspath(ment_mp3))

                        # Park4139.debug_as_cli(rf'프로세스 세션을 빼앗지 않고 mp3재생')
                        ment_mp3 = os.path.abspath(ment_mp3)
                        DebuggingUtil.print_ment_magenta(rf'{ment_mp3}')
                        try:
                            # 재생
                            source = pyglet.media.load(ment_mp3)
                            # pyglet_player = Park4139.pyglet_player
                            # pyglet_player.queue(source)
                            source.play()  # 웃긴다 이거 이렇게는 재생이 된다.

                            length_of_mp3 = TextToSpeechUtil.get_length_of_mp3(ment_mp3)
                            # time.sleep(length_of_mp3 * 0.65)
                            # time.sleep(length_of_mp3 * 0.75)
                            # time.sleep(length_of_mp3 * 0.85)
                            # time.sleep(length_of_mp3 * 0.95)
                            # time.sleep(length_of_mp3 * 1.05)
                            # time.sleep(length_of_mp3 * 1.00)
                            time.sleep(length_of_mp3 * sleep_after_play)

                            return length_of_mp3
                            # Park4139.is_speak_as_async_running = False # 쓰레드상태 사용종료로 업데이트
                        except FileNotFoundError:
                            DebuggingUtil.print_ment_magenta(f"{ment_mp3} 재생할 파일이 없습니다")
                        except:
                            DebuggingUtil.trouble_shoot("%%%FOO%%%")
                            break

                        DebuggingUtil.commentize("before_mp3_length_used_in_speak_as_async 업데이트")
                        length_of_mp3 = round(float(TextToSpeechUtil.get_length_of_mp3(ment_mp3)), 1)
                        BusinessLogicUtil.previous_mp3_length_used_in_speak_as_async = length_of_mp3

                    except Exception:
                        DebuggingUtil.trouble_shoot("%%%FOO%%%")

                    # Park4139.debug_as_cli(rf'불필요 파일 삭제')
                    os.system(f'echo y | del /f "{ment__mp3}" >nul 2>&1')
                break
        except Exception:
            DebuggingUtil.trouble_shoot("%%%FOO%%%")

    @staticmethod
    def remove_special_characters(text):
        # pattern = r"[^\w\s]" #  \s(whitespace characters = [" ", "\t", "\n", ".", "\n", "_" ])      # space = " " #공백
        # pattern = r"[^\w.,]" # \w(알파벳, 숫자, 밑줄 문자)와 "." 그리고 ","를 제외한 모든문자를 선택, \t, \n, _ 도 삭제되는 설정
        pattern = r"[~!@#$%^&*()_+|<>?:{}]"
        return re.sub(pattern, "", text)

    @staticmethod
    def speak_server_hh_mm():  # '몇 시야' or usr_input_txt == '몇시야':
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        server_hour = BusinessLogicUtil.get_time_as_('%H')
        server_minute = BusinessLogicUtil.get_time_as_('%M')
        DebuggingUtil.print_ment_magenta(f'{server_hour}시 {server_minute}분 입니다')

    @staticmethod
    def speak_server_ss():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        server_seconds = BusinessLogicUtil.get_time_as_('%S')
        DebuggingUtil.print_ment_magenta(f'{server_seconds}초')

    @staticmethod
    def speak_today_time_info():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        yyyy = BusinessLogicUtil.get_time_as_('%Y')
        MM = BusinessLogicUtil.get_time_as_('%m')
        dd = BusinessLogicUtil.get_time_as_('%d')
        HH = BusinessLogicUtil.get_time_as_('%H')
        mm = BusinessLogicUtil.get_time_as_('%M')
        week_name = BusinessLogicUtil.return_korean_week_name()
        TextToSpeechUtil.speak_ment_without_async_and_return_last_word_mp3_length(ment=f'현재 시각 {int(yyyy)}년 {int(MM)}월 {int(dd)}일 {week_name}요일 {int(HH)}시 {int(mm)}분', sleep_after_play=0.75)


class DebuggingUtil:
    # @afterpause # gui 가 뜨면 pause() 수행되는 것과 동일한 효과가 나타난다.
    @staticmethod
    def trouble_shoot(trouble_id: str):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        ment = f"TROUBLE SHOOT REPORT:\n{traceback.format_exc()}\ntrouble_id : {trouble_id}"
        print(ment)
        # BusinessLogicUtil.debug(ment, input_text_default=trouble_id, auto_click_positive_btn_after_seconds=600)
        return trouble_id

    @staticmethod
    def commentize(ment):
        # print(f'{StateManagementUtil.LINE_LENGTH_PROMISED} {ment}')
        # DebuggingUtil.print_ment_via_colorama(f'{StateManagementUtil.LINE_LENGTH_PROMISED} {ment}', colorama_color=ColoramaColorUtil.LIGHTGREEN_EX)
        DebuggingUtil.print_ment_via_colorama(f'{StateManagementUtil.LINE_LENGTH_PROMISED} {ment}', colorama_color=ColoramaColorUtil.LIGHTBLACK_EX)
        # self.speak(title) # 생각보다 너무 말이 많아 주석처리
        return f'{StateManagementUtil.LINE_LENGTH_PROMISED} {ment}'

    @staticmethod
    # def print_ment_via_colorama(ment, color:Union[ColoramaColorUtil.GREEN, ColoramaColorUtil.RED]):
    def print_ment_via_colorama(ment, colorama_color: Enum):
        # colorama_color 값에 해당하는 Fore 값으로 매핑, 리펙토리 후
        colorama_to_fore = {
            ColoramaColorUtil.BLACK: Fore.BLACK,
            ColoramaColorUtil.RED: Fore.RED,
            ColoramaColorUtil.GREEN: Fore.GREEN,
            ColoramaColorUtil.YELLOW: Fore.YELLOW,
            ColoramaColorUtil.BLUE: Fore.BLUE,
            ColoramaColorUtil.MAGENTA: Fore.MAGENTA,
            ColoramaColorUtil.CYAN: Fore.CYAN,
            ColoramaColorUtil.WHITE: Fore.WHITE,
            ColoramaColorUtil.RESET: Fore.RESET,
            ColoramaColorUtil.LIGHTBLACK_EX: Fore.LIGHTBLACK_EX,
            ColoramaColorUtil.LIGHTRED_EX: Fore.LIGHTRED_EX,
            ColoramaColorUtil.LIGHTGREEN_EX: Fore.LIGHTGREEN_EX,
            ColoramaColorUtil.LIGHTYELLOW_EX: Fore.LIGHTYELLOW_EX,
            ColoramaColorUtil.LIGHTBLUE_EX: Fore.LIGHTBLUE_EX,
            ColoramaColorUtil.LIGHTMAGENTA_EX: Fore.LIGHTMAGENTA_EX,
            ColoramaColorUtil.LIGHTCYAN_EX: Fore.LIGHTCYAN_EX,
            ColoramaColorUtil.LIGHTWHITE_EX: Fore.LIGHTWHITE_EX
        }
        colorama_color = colorama_to_fore.get(colorama_color, Fore.RESET)

        print(f"{colorama_color}{ment}")
        # init(autoreset=False)

    @staticmethod
    def print_ment_fail(ment):
        DebuggingUtil.print_ment_via_colorama(ment, colorama_color=ColoramaColorUtil.RED)

    @staticmethod
    def print_ment_success(ment):
        DebuggingUtil.print_ment_via_colorama(ment, colorama_color=ColoramaColorUtil.LIGHTGREEN_EX)

    @staticmethod
    def print_ment_magenta(ment):
        DebuggingUtil.print_ment_via_colorama(ment, colorama_color=ColoramaColorUtil.LIGHTMAGENTA_EX)

    @staticmethod
    def print_ment_light_white(ment):
        DebuggingUtil.print_ment_via_colorama(ment, colorama_color=ColoramaColorUtil.LIGHTWHITE_EX)

    @staticmethod
    def print_ment_light_yellow(ment):
        DebuggingUtil.print_ment_via_colorama(ment, colorama_color=ColoramaColorUtil.LIGHTYELLOW_EX)


class DbTomlUtil:
    @staticmethod
    def create_db_toml():
        try:
            db_abspath = StateManagementUtil.DB_TOML
            # db_template =Park4139.db_template
            DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
            if not os.path.exists(os.path.dirname(db_abspath)):
                os.makedirs(os.path.dirname(db_abspath))  # 이거 파일도 만들어지나? 테스트 해보니 안만들어짐 디렉토리만 만들어짐
            # DebuggingUtil.commentize("db 파일 존재 검사 시도")
            if not os.path.isfile(db_abspath):
                # with open(db_abspath, "w") as f2:
                #     toml.dump(db_template, f2)
                FileSystemUtil.make_leaf_file(db_abspath)
                DebuggingUtil.print_ment_magenta(f"DB를 만들었습니다 {db_abspath}")
            else:
                DebuggingUtil.print_ment_magenta(f"DB가 이미존재합니다 {db_abspath}")
        except:
            DebuggingUtil.trouble_shoot("%%%FOO%%%")

    @staticmethod
    def read_db_toml():
        try:
            DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
            print("DB 의 모든 자료를 가져왔습니다")
            return toml.load(StateManagementUtil.DB_TOML)
        except:
            DebuggingUtil.trouble_shoot("%%%FOO%%%")

    @staticmethod
    def get_db_toml_key(unique_id):
        return BusinessLogicUtil.get_str_replaced_special_characters(target=unique_id, replacement="_")

    @staticmethod
    def select_db_toml(key):
        try:
            key = str(key)
            DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
            db_abspath = StateManagementUtil.DB_TOML
            try:
                # return toml.load(DB_TOML)[key]
                with open(db_abspath, 'r', encoding='utf-8') as f:
                    db = toml.load(f)
                return db[key]

            except KeyError:
                print(f"DB 에 해당키가 존재하지 않습니다 {key}")
                return None
        except:
            DebuggingUtil.trouble_shoot("%%%FOO%%%")

    @staticmethod
    def update_db_toml(key, value):
        try:
            db_abspath = StateManagementUtil.DB_TOML
            key: str = str(key)
            DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
            # 기존의 DB 의 데이터
            with open(db_abspath, 'r', encoding='utf-8') as f:
                db = toml.load(f)
                # DebuggingUtil.commentize("DB 업데이트 전 ")
                # Park4139.debug_as_cli(context=str(db))

            # 데이터 업데이트
            if key in db:
                db[key] = value
            else:
                # db[key] = value
                print(f"DB에 key가 없어서 업데이트 할 수 없습니다 key:{key} value:{value}")

            # TOML 파일에 데이터 쓰기
            with open(db_abspath, 'w', encoding='utf-8') as f:
                toml.dump(db, f)
                print(f"DB에 데이터가 업데이트되었습니다")

            # DB 변경 확인
            # with open(db_abspath, 'r') as f:
            #     db = toml.load(f)
            #     DebuggingUtil.commentize("DB 변경 확인")
            #     Park4139.debug_as_cli(context=str(db))
        except:
            DebuggingUtil.trouble_shoot("%%%FOO%%%")

    @staticmethod
    def insert_db_toml(key, value):
        try:
            key = str(key)
            db_abspath = StateManagementUtil.DB_TOML
            DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
            db_abspath = StateManagementUtil.DB_TOML
            # 기존의 DB 의 데이터
            with open(db_abspath, 'r', encoding='utf-8') as f:
                db = toml.load(f)
                # DebuggingUtil.commentize("DB 업데이트 전 ")
                # Park4139.debug_as_cli(context=str(db))

            # 데이터 삽입
            if key in db:
                # db[key] = value
                print(f"이미 값이 존재하여 삽입할 수 없습니다 key:{key} value:{value}")
            else:
                db[key] = value

            # TOML 파일에 데이터 쓰기
            with open(db_abspath, 'w', encoding='utf-8') as f:
                toml.dump(db, f)
                print(f"DB에 데이터가 삽입되었습니다")

            # DB 변경 확인
            # with open(db_abspath, 'r') as f:
            #     db = toml.load(f)
            #     DebuggingUtil.commentize("DB 변경 확인")
            #     Park4139.debug_as_cli(context=str(db))
        except:
            DebuggingUtil.trouble_shoot("%%%FOO%%%")

    @staticmethod
    def back_up_db_toml():
        try:
            DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
            BusinessLogicUtil.back_up_target(StateManagementUtil.DB_TOML)
        except:
            DebuggingUtil.trouble_shoot("%%%FOO%%%")

    @staticmethod
    def delete_db_toml():
        try:
            DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
            FileSystemUtil.convert_as_zip_with_timestamp(StateManagementUtil.DB_TOML)
        except:
            DebuggingUtil.trouble_shoot("%%%FOO%%%")

    @staticmethod
    def is_accesable_local_database():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        if not os.path.exists(StateManagementUtil.DB_TOML):
            DbTomlUtil.create_db_toml()
            return False
        else:
            return True


class FileSystemUtil:
    @staticmethod
    def get_tree_depth_level(file_abspath: str):
        return len(file_abspath.split("\\")) - 1

    @staticmethod
    def get_target_as_pnx(target_abspath):
        """디렉토리/파일 대상 테스트 성공"""
        return target_abspath

    @staticmethod
    def get_target_as_pn(target_abspath):
        """디렉토리/파일 대상 테스트 성공"""
        return rf"{os.path.dirname(target_abspath)}\{os.path.splitext(os.path.basename(target_abspath))[0]}"

    @staticmethod
    def get_target_as_nx(target_abspath):
        """디렉토리/파일 대상 테스트 성공"""
        return rf"{os.path.splitext(os.path.basename(target_abspath))[0]}{os.path.splitext(os.path.basename(target_abspath))[1]}"

    @staticmethod
    def get_target_as_x(target_abspath):
        """디렉토리/파일 대상 테스트 성공"""
        return rf"{os.path.splitext(os.path.basename(target_abspath))[1]}"

    @staticmethod
    def get_target_as_n(target_abspath):
        """디렉토리/파일 대상 테스트 성공"""
        return rf"{os.path.splitext(os.path.basename(target_abspath))[0]}"

    @staticmethod
    def convert_mkv_to_wav(file_mkv):
        FileSystemUtil.get_cmd_output(rf'ffmpeg -i "{file_mkv}" -ab 160k -ac 2 -ar 44100 -vn {FileSystemUtil.get_target_as_pn(file_mkv)}.wav')

    @staticmethod
    def convert_mp4_to_webm(target_abspath):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        '''테스트 필요'''
        print(f'from : {target_abspath}')
        file_edited = f'{os.path.splitext(os.path.basename(target_abspath))[0]}.webm'
        print(f'to   : {file_edited}')

        path_started = os.getcwd()
        os.system('export LANG=en_US.UTF-8 >nul')

        os.system('mkdir storage >nul')
        os.chdir('storage')
        os.system(f'"{StateManagementUtil.FFMPEG_EXE}" -i "{target_abspath}" -f webm -c:v libvpx -b:v 1M -acodec libvorbis "{file_edited}" -hide_banner')
        os.chdir(path_started)

    @staticmethod
    def convert_wav_to_flac(target_abspath):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        '''테스트 필요'''

        # :: 한글 인코딩 setting
        os.system('export LANG=en_US.UTF-8 >nul')

        print(f'from : {target_abspath}')
        file_edited = f'{os.path.splitext(os.path.basename(target_abspath))[0]}.flac'
        print(f'to   : {file_edited}')

        # :: ffmpeg location setting
        ffmpeg_exe = rf"{StateManagementUtil.USERPROFILE}\Desktop\`workspace\tool\LosslessCut-win-x64\resources\ffmpeg.exe"
        destination = 'storage'
        try:
            os.makedirs(destination)
        except Exception as e:
            pass
        os.chdir(destination)
        print(f'"{ffmpeg_exe}" -i "{target_abspath}" -c:a flac "{file_edited}"        를 수행합니다.')
        subprocess.check_output(f'"{ffmpeg_exe}" -i "{target_abspath}" -c:a flac "{file_edited}"', shell=True)

    @staticmethod
    def convert_as_zip_with_timestamp(target_abspath):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        starting_directory = ''
        try:
            starting_directory = os.getcwd()

            target_dirname = os.path.dirname(target_abspath)
            target_dirname_dirname = os.path.dirname(target_dirname)
            target_basename = os.path.basename(target_abspath).split(".")[0]
            target_zip = rf'$zip_{target_basename}.zip'
            target_yyyy_mm_dd_HH_MM_SS_zip = rf'{target_basename} - {BusinessLogicUtil.get_time_as_("%Y %m %d %H %M %S")}.zip'
            # DebuggingUtil.commentize(rf'# target_dirname_dirname 로 이동')
            os.chdir(target_dirname_dirname)
            # DebuggingUtil.commentize(rf'부모디렉토리로 빽업')
            cmd = f'bandizip.exe c "{target_zip}" "{target_abspath}"'
            FileSystemUtil.get_cmd_output(cmd)
            # DebuggingUtil.commentize(rf'이름변경')
            cmd = f'ren "{target_zip}" "$deleted_{target_yyyy_mm_dd_HH_MM_SS_zip}"'
            FileSystemUtil.get_cmd_output(cmd)
            # DebuggingUtil.commentize(rf'부모디렉토리에서 빽업될 디렉토리로 이동')
            cmd = f'move "$deleted_{target_yyyy_mm_dd_HH_MM_SS_zip}" "{target_dirname}"'
            FileSystemUtil.get_cmd_output(cmd)
            # DebuggingUtil.commentize(rf'빽업될 디렉토리로 이동')
            os.chdir(target_dirname)
            # DebuggingUtil.commentize("os.getcwd()")
            # Park4139.debug_as_cli(os.getcwd())
            # DebuggingUtil.commentize("원본파일삭제")
            os.remove(target_abspath)

        except:
            DebuggingUtil.trouble_shoot("202312030000c")
        finally:
            DebuggingUtil.commentize(rf'프로젝트 디렉토리로 이동')
            os.chdir(starting_directory)

    @staticmethod
    def kill_thread(thread_name):
        # 종료할 스레드 이름

        # 현재 실행 중인 모든 스레드 가져오기
        current_threads = threading.enumerate()

        # 종료할 스레드 찾기
        target_thread = None
        for thread in current_threads:
            if thread.name == thread_name:
                target_thread = thread
                break

        # 스레드 종료
        if target_thread:
            target_thread.join()
            print(f"{thread_name} 스레드가 종료되었습니다.")
        else:
            print(f"{thread_name} 스레드를 찾을 수 없습니다.")

    @staticmethod
    def is_file_changed(file_abspath):
        # 조건문을 반복 작성해서 기능을 분리할 수가 있었다.
        # 여기서 알게된 사실은 조건문의 구조를 반복해서 특정 기능들의 로직들을 분리할 수 있었다.
        key = DbTomlUtil.get_db_toml_key(file_abspath)

        # 기존에 측정된 파일의 줄 수 : 없으면 새로 측정된 파일의 줄 수로 대신함.
        line_cnt_from_db = DbTomlUtil.select_db_toml(key=key)
        if line_cnt_from_db == None:
            DbTomlUtil.insert_db_toml(key=key, value=BusinessLogicUtil.get_line_cnt_of_file(file_abspath))  # 50000 줄의 str 다루는 것보다 50000 개의 list 다루는 것이 속도성능에 대하여 효율적이다.
            line_cnt_from_db = DbTomlUtil.select_db_toml(key=key)
        print(f"line_cnt_from_db : {line_cnt_from_db}")

        # 새로 측정된 파일의 줄 수
        line_cnt_measured = BusinessLogicUtil.get_line_cnt_of_file(file_abspath)
        print(f"line_cnt_measured : {line_cnt_measured}")

        # 로직분리 새로운 시도: 기능에 따라 조건문을 여러개 만들어 보았다.
        # commentize() 관련된 로직 분리
        if FileSystemUtil.is_file_edited(file_abspath) is None:
            DebuggingUtil.commentize("데이터베이스 타겟에 대한 key가 없어 key를 생성합니다")
        elif FileSystemUtil.is_file_edited(file_abspath):
            ment = f'모니터링 중 편집을 감지하였습니다.\n{os.path.basename(file_abspath)}\n 타겟빽업을 시도합니다.\n 타겟에 대한 key를 toml 데이터베이스에 업데이트합니다.'
            DebuggingUtil.print_ment_magenta(ment=ment)

        # db crud 관련된 로직 분리
        if FileSystemUtil.is_file_edited(file_abspath):
            DbTomlUtil.update_db_toml(key=key, value=BusinessLogicUtil.get_line_cnt_of_file(file_abspath))
        elif FileSystemUtil.is_file_edited(file_abspath) is None:
            DbTomlUtil.insert_db_toml(key=key, value=BusinessLogicUtil.get_line_cnt_of_file(file_abspath))
        if FileSystemUtil.is_file_edited(file_abspath):
            return True

    @staticmethod
    def sync_directory_remote(target_abspath):
        """ windows + wsl + rsync """
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        pass

    @staticmethod
    def sync_directory_local(target_abspath):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        try:
            from dirsync import sync

            target_abspath = target_abspath
            future_abspath = rf"{target_abspath}_sync"

            # 기존 작업 폴더가 없는 경우
            if not os.path.exists(future_abspath):
                shutil.copytree(target_abspath, future_abspath)
            else:
                FileSystemUtil.remove_target_parmanently(StateManagementUtil.DIRSYNC_LOG)
                # 로깅 설정 및 Park4139.DIRSYNC_LOG 생성
                import logging
                logging.basicConfig(filename=StateManagementUtil.DIRSYNC_LOG, level=logging.DEBUG, filemode='w', encoding='utf-8')
                dirsync_logger = logging.getLogger('dirsync')
                logging.debug('디버그 메시지 테스트')
                logging.info('정보 메시지 테스트')
                logging.warning('경고 메시지 테스트')
                logging.error('에러 메시지 테스트')
                logging.critical('심각한 에러 메시지 테스트')
                # result_sync = sync(sourcedir=target_abspath, targetdir=future_abspath, action='sync', verbose=True, logger=dirsync_logger) #success
                result_sync = sync(sourcedir=target_abspath, targetdir=future_abspath, action="sync", options=["--purge", "--verbose", "--force"], logger=dirsync_logger)
                # sync(sourcedir=future_abspath, targetdir=target_abspath , action='sync',verbose=True , logger = dirsync_logger)  # 양방향 으로 로컬동기화폴더를 만드려면 sync() 코드를 추가하여 sync() 함수가 총 2개가 targetdir 간에 sourcedir 서로 자리바뀌어 있도록 작성
                if result_sync:
                    # Park4139.DIRSYNC_LOG 내용 가져오기
                    if os.path.exists(StateManagementUtil.DIRSYNC_LOG):
                        lines = FileSystemUtil.get_lines_of_file(StateManagementUtil.DIRSYNC_LOG)[-4:-1]
                        lines = [sample.strip() for sample in lines]
                        for sample in lines:
                            # print(Park4139.translate_eng_to_kor_via_googletrans(sample))
                            print(sample)
                        print(rf'len(lines) : {len(lines)}')
                        FileSystemUtil.remove_target_parmanently(StateManagementUtil.DIRSYNC_LOG)
                        lines = [x for x in lines if x.strip("\n")]  # 리스트 요소 "" 제거,  from ["", A] to [A]       [""] to []
                        DebuggingUtil.print_ment_magenta(f"타겟의 동기화가 성공했습니다")
        except:
            DebuggingUtil.trouble_shoot("%%%FOO%%%")
        # from dirsync import sync
        # sources = [r'C:\Users\seon\Desktop\오리지널',
        #            r'C:\Users\seon\Desktop\오리지널2',
        #            r'C:\Users\seon\Desktop\오리지널3']
        # targets = [r'C:\Users\seon\Desktop\테스트',
        #            r'C:\Users\seon\Desktop\테스트2',
        #            r'C:\Users\seon\Desktop\테스트3']
        # total = dict(zip(sources, targets))
        # for source, target in total.items():
        #     sync(sourcedir=source, targetdir=target, action='sync', verbose=True, purge=True, create=True,  delete=True, update=True)  # 이것이 sync() default 파라미터들이다.
        #     sync(sourcedir=source, targetdir=target, action='sync', verbose=True, purge=True, create=True,  delete=True, update=True)  # purge=True 이면 targetdir 에 이물질 같은 파일이 있으면 삭제를 합니다, delete=False 이면 어떻게 되는거지? # verbose = True 이면 상세설명출력

        # 윈도우 디렉토리 경로를 WSL 경로로 변환
        # try:
        #     server_time = Park4139.get_time_as_('%Y_%m_%d_%H_%M_%S_%f')
        #     target_abspath = rf"/mnt/c/{target_abspath}" \ 에서 / 로 바꿔야한다
        #     # future_abspath = rf"/mnt/c/{target_abspath}_{server_time}"
        #     future_abspath = rf"/mnt/c/{target_abspath}_sync"
        #     command = f"rsync -avz {target_abspath} {future_abspath}"
        #     print(command)
        #     subprocess.call(command, shell=True)
        # except:
        #     pass

    @staticmethod
    def get_lines_of_file(file_abspath):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        try:
            if os.path.exists(file_abspath):
                # with open(file_abspath, 'r', encoding="utf-8") as f:
                # with open(file_abspath, 'r', errors='ignore') as f:
                with open(file_abspath, 'r', encoding="utf-8", errors='ignore') as f:
                    lines = f.readlines()  # from file.ext to ["한줄","한줄","한줄"]
                    return lines
        except:
            DebuggingUtil.trouble_shoot("%%%FOO%%%")

    @staticmethod
    def remove_target_parmanently(target_abspath):
        """
        정말 로직적으로 삭제해도 상관 없는 경우가 아니면 이 함수는 쓰지 말것
        이 메소드를 사용하는 것은 데이터소실과 관계된 위험한 일이다.
        쓰레기통으로 target을 옮기는 move_to_trash_bin_target() 함수를 만들어 두었으니 최대한 활용하자.
        유사 기능으로는 shutil.rmtree(path) 가 있다. rmdir /s 명령어랑 같은 것 결과가 기대된다.
        """
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        try:
            if BusinessLogicUtil.validate_and_return(value=target_abspath) is not False:
                if os.path.isdir(target_abspath):
                    FileSystemUtil.get_cmd_output(rf'echo y | rmdir /s "{target_abspath}"')
                    # shutil.rmtree(target_abspath)
                elif os.path.isfile(target_abspath):
                    FileSystemUtil.get_cmd_output(rf'echo y | del /f "{target_abspath}"')
                    os.remove(target_abspath)
        except:
            print("파일 삭제 중 에러가 발생했습니다")

    @staticmethod
    def is_directory_changed(directory_abspath):
        # 현재 디렉토리 상태
        current_directory_state = None
        previous_directory_state = None
        try:
            current_directory_state = FileSystemUtil.get_directory_files_files_for_monitoring_mtime_without_files_to_exclude(directory_abspath=directory_abspath)  # from str to [["abspath", "mtime"]]
            current_directory_state = sorted(current_directory_state, key=lambda item: item[1], reverse=True)  # from [["abspath", "mtime"]] to [["abspath", "mtime"]] (딕셔너리를 value(mtime)를 기준으로 내림차순으로 정렬), 날짜를 제일 현재와 가까운 날짜를 선택하는 것은 날짜의 숫자가 큰 숫자에 가깝다는 이야기이다. 그러므로  큰 수부터 작은 수의 순서로 가는 내림차순으로 정렬을 해주었다(reverse=True).
            current_directory_state = DataStructureUtil.get_list_seperated_by_each_elements_in_nested_list(current_directory_state)  # from [["a","b"], ["c","d"]] to ["a", "b", "c", "d"]
            current_directory_state = DataStructureUtil.get_list_each_two_elements_joined(current_directory_state)  # from ["a", "b", "c", "d"] to ["ab", "cd"]
            current_directory_state = BusinessLogicUtil.get_list_replaced_from_list_that_have_special_characters(target=current_directory_state, replacement="")  # from [] to [] (특수문자 제거 시킨) # 이부분을 암호화 시키면 어떨까 싶은데 #딕셔너리에 있는부분을 replace
            [print(sample) for sample in current_directory_state[0:10]]
            print(rf'type(current_directory_state) : {type(current_directory_state)}')
            print(rf'len(current_directory_state) : {len(current_directory_state)}')
        # 이전 디렉토리 상태
        except:
            pass
        try:
            previous_directory_state = DbTomlUtil.select_db_toml(key=DbTomlUtil.get_db_toml_key(directory_abspath))
            if previous_directory_state == None:
                DbTomlUtil.insert_db_toml(key=DbTomlUtil.get_db_toml_key(directory_abspath), value=current_directory_state)  # 50000 줄의 str 다루는 것보다 50000 개의 list 다루는 것이 속도성능에 대하여 효율적이다. # DB에 [] 로 저장
                previous_directory_state = DbTomlUtil.select_db_toml(key=DbTomlUtil.get_db_toml_key(directory_abspath))
            [print(sample) for sample in previous_directory_state[0:10]]
            print(rf'type(previous_directory_state) : {type(previous_directory_state)}')
            print(rf'len(previous_directory_state) : {len(previous_directory_state)}')
        except:
            pass

        # 변화 감지 ( 러프, 빠름)
        # 두 디렉토리 상태 합쳐서 중복제거 해서 디렉토리 처음 상태의 절반이 나오면 중복이 없다는 생각.
        # 위의 생각은 맞는데 실제로 내가 숫자를 잘 못 파악했다.
        # set() 함수는 중복을 제거한 나머지를 리스트에 저장하는 함수이다.
        # 따라서 a != b 인 경우,  a == b 인 경우, 중복이 없는것
        # str을 줄단위로 쪼개 [str]로 리스트를 합한다.
        # try:
        #     merged_list = current_directory_state + previous_directory_state  # from [1, 2, 3] + [ x, y, z] to [1, x, 2, y, 3, z]
        #     [print(sample) for sample in merged_list[0:10]]
        #     print(rf'type(merged_list) : {type(merged_list)}')
        #     print(rf'len(merged_list) : {len(merged_list)}')
        #     a = len(merged_list)/2
        #     b = len(list(set(merged_list)))
        #     print(rf'a : {a}  b : {b} ')
        #     # duplicates = list(set([x for x in merged_list if merged_list.count(x) == 1])) # 중복되는 것만 추출 # 너무 느림 # 추가된파일, 삭제된 파일
        #     # print(rf'a : {a}  b : {b}   duplicates : {duplicates}')
        # except:
        #     pass
        # try:
        #     merged_list = Park4139List.get_list_added_elements_alternatively(current_directory_state, previous_directory_state)  # from [1, 2, 3] + [ x, y, z] to [1, x, 2, y, 3, z]
        #     [print(sample) for sample in merged_list[0:10]]
        #     print(rf'type(merged_list) : {type(merged_list)}')
        #     print(rf'len(merged_list) : {len(merged_list)}')
        #     a = len(merged_list) / 2
        #     b = len(list(set(merged_list)))
        #     print(rf'a : {a}  b : {b} ')
        #     print(rf'a : {a}  b : {b}   duplicates : {duplicates}')
        # finally:
        #     pass

        # 변화 감지 ( 디테일, 느림)
        # try:
        #     added_files = Park4139.get_added_files(previous_directory_state, current_directory_state)
        #     if added_files:
        #         print(f"추가된 파일 개수: {len(added_files)} 추가된 파일: {added_files}")
        #     deleted_files = Park4139.get_deleted_files(previous_directory_state, current_directory_state)
        #     if deleted_files:
        #         print(f"삭제된 파일 개수: {len(deleted_files)} 삭제된 파일: {deleted_files}")
        #     modified_files = Park4139.get_modified_files(previous_directory_state, current_directory_state)
        #     if modified_files:
        #         print(f"변경된 파일 개수: {len(modified_files)} 변경된 파일: {modified_files}")
        # except:
        #     pass

        # 변화 감지 ( 러프, 덜 느림)
        try:
            if DataStructureUtil.is_two_lists_equal(list1=current_directory_state, list2=previous_directory_state):
                print("디렉토리가 변경되지 않았습니다")
                return False
            else:
                print("디렉토리 변경이 감지되었습니다")
                DbTomlUtil.update_db_toml(key=DbTomlUtil.get_db_toml_key(directory_abspath), value=current_directory_state)
                return True
        except:
            pass

    @staticmethod
    def get_directory_files_files_for_monitoring_mtime_without_files_to_exclude(directory_abspath):
        files_to_exclude = [
            StateManagementUtil.DB_TOML,
            StateManagementUtil.SUCCESS_LOG,
            StateManagementUtil.LOCAL_PKG_CACHE_FILE,
            StateManagementUtil.DIRSYNC_LOG,
        ]
        files_of_directory = []
        for root, dirs, files in os.walk(directory_abspath):
            for file in files:
                if not file.endswith(".mp3"):  # 모든 mp3 파일을 배제합니다
                    file_path = os.path.join(root, file)
                    if file_path not in files_to_exclude:
                        # files_of_directory[rf"{file_path}"] = os.path.getmtime(file_path)
                        files_of_directory.append([file_path, os.path.getmtime(file_path)])
        return files_of_directory

    @staticmethod
    def get_added_files(previous_state, current_state):
        return DataStructureUtil.get_elements_that_list1_only_have(list1=current_state, list2=previous_state)

    @staticmethod
    def get_deleted_files(previous_state, current_state):
        return DataStructureUtil.get_elements_that_list1_only_have(list1=previous_state, list2=current_state)

    @staticmethod
    def get_modified_files(previous_state, current_state):
        return DataStructureUtil.get_different_elements(list1=current_state, list2=previous_state)

    @staticmethod
    def make_leaf_file(file_abspath):
        if not os.path.exists(file_abspath):
            try:
                os.makedirs(os.path.dirname(file_abspath))
            except FileExistsError:
                pass
            # FileSystemUtil.get_cmd_output(rf'chcp 65001 >nul')
            FileSystemUtil.get_cmd_output(rf'export LANG=en_US.UTF-8')
            FileSystemUtil.get_cmd_output(rf'echo. > "{file_abspath}"')

    @staticmethod
    def make_leaf_directory(leaf_directory_abspath):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        DebuggingUtil.print_ment_via_colorama(ment=rf"leaf_directory_abspath : {leaf_directory_abspath}", colorama_color=ColoramaColorUtil.LIGHTWHITE_EX)
        if not os.path.exists(leaf_directory_abspath):
            os.makedirs(leaf_directory_abspath)

    @staticmethod
    def is_empty_directory(directory_abspath):
        try:
            if len(os.listdir(directory_abspath)) == 0:
                return True
            else:
                return False
        except FileNotFoundError:
            DebuggingUtil.print_ment_via_colorama(ment="FileNotFoundError", colorama_color=ColoramaColorUtil.RED)
            pass

    @staticmethod
    def rename_target(current_target_abspath, future_target_abspath):
        # directory 명을 변경하는 경우에 재귀적으로 바뀌어야 한는 것으로 생각되어 os.renames 를 테스트 후 적용하였다.
        # os.rename 와 os.renames 에는 큰 차이가 있는데
        # os.rename 사용 중에 old_path 가 directory  인 경우는 재귀적으로 변경이 안된다고 wrtn 은 말해주었다.
        os.renames(current_target_abspath, future_target_abspath)

    # @staticmethod
    # def merge_two_directories_without_overwrite(directory_a, directory_b):
    #     """디렉토리 머지용 기능"""
    #     # 빈디렉토리 머지 용도로도 많이 쓸것 같다
    #     while True:
    #         if directory_a == directory_b:
    #             DebuggingUtil.print_ment_magenta("동일한 디렉토리는 머지하실 수 없습니다")
    #             break
    #         dst_p = rf"{os.path.dirname(directory_a)}"
    #         dst_n = rf"[{os.path.basename(directory_a)}] [{os.path.basename(directory_b)}]"
    #         dst_n = dst_n.replace("[[", "[")
    #         dst_n = dst_n.replace("]]", "]")
    #         # dst_n = dst_n.split("] [")
    #         # dst_n = re.sub(pattern=r'\$\d{19}', repl='', string=dst_n, count=1) # count 파라미터를 count=1 로 설정하여, 패턴이 여러번 나타나도 첫번째 카운트만 제거
    #         dst_n = re.sub(pattern=r'\$\d{20}', repl='', string=dst_n)
    #         dst_n = rf"{dst_n} ${BusinessLogicUtil.get_time_as_('%Y%m%d%H%M%S%f')}"
    #         dst = rf"{dst_p}\{dst_n}"
    #         FileSystemUtil.make_leaf_directory(dst)
    #         print(rf'dst : {dst}')
    #         if os.path.isdir(directory_b):
    #             for target in os.listdir(directory_a):  # os.listdir 은 without walking 으로 동작한다
    #                 print(rf'target : {directory_a}\{target}')
    #                 FileSystemUtil.move_target_without_overwrite(target_abspath=rf'{directory_a}\{target}', dst=dst)
    #                 # Park4139.move_target_to_trash_bin(directory_a)
    #             for target in os.listdir(directory_b):  # os.listdir 은 without walking 으로 동작한다
    #                 print(rf'target : {directory_b}\{target}')
    #                 FileSystemUtil.move_target_without_overwrite(target_abspath=rf'{directory_b}\{target}', dst=dst)
    #         else:
    #             DebuggingUtil.print_ment_magenta("디렉토리만 머지하실 수 있습니다")
    #             break
    #         break
    # nagasarete airantou

    @staticmethod
    def merge_directories(directoryies: str):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")

        is_breaking = False
        # cmd /c dir /b /s /a:d | clip
        directoryies = directoryies.strip()
        directoryies = directoryies.strip("\t")
        directoryies_: [str] = directoryies.split("\n")
        directoryies_ = [x for x in directoryies_ if x.strip()]  # 리스트 요소 "" 제거,  from ["", A] to [A]    from [""] to []
        directoryies_ = [x.strip() for x in directoryies_]  # 리스트 각 요소 strip(),  ["   A", "B   "] from ["A", "B"]
        directoryies_ = [x.strip("\"") for x in directoryies_]  # 리스트 각 요소 strip("\""),  [""A""] from ["A"]
        directoryies_ = [x.strip("\'") for x in directoryies_]  # 리스트 각 요소 strip("\'),  ["'A'""] from ["A"]
        print(rf'directoryies_ : {directoryies_}')
        print(rf'type(directoryies_) : {type(directoryies_)}')
        print(rf'len(directoryies_) : {len(directoryies_)}')
        if 0 == len(directoryies_):
            DebuggingUtil.print_ment_magenta("타겟경로가 아무것도 입력되지 않았습니다")
            return
        elif 1 == len(directoryies_):
            DebuggingUtil.print_ment_magenta("하나의 타겟경로로는 머지를 시도할수 없습니다, 여러개의 타겟경로들을 입력해주세요")
            return
        elif 1 < len(directoryies_):
            for index, directory in enumerate(directoryies_):
                connected_drives = []
                for drive_letter in string.ascii_uppercase:
                    drive_path = drive_letter + ":\\"
                    if os.path.exists(drive_path):
                        connected_drives.append(drive_path)
                        if directory == drive_path:
                            DebuggingUtil.print_ment_magenta("입력된 타겟경로는 너무 광범위하여, 진행할 수 없도록 설정되어 있습니다")
                            break

            # FileSystemUtil.make_leaf_directory(StateManagementUtil.EMPTY_DIRECTORYIES)

            # indices_to_remove = []  # 제거할 인덱스를 기록할 리스트
            # for index, directory in enumerate(directoryies_):
            #     if os.path.isdir(directory):
            #         if FileSystemUtil.is_empty_directory(directory):
            #             FileSystemUtil.move_target_without_overwrite(target_abspath=directory, dst=StateManagementUtil.EMPTY_DIRECTORYIES)
            #             indices_to_remove.append(index)
            # for index in indices_to_remove:
            #     directoryies_.pop(index)

            # for index, directory in enumerate(directoryies_):
            #     if directory == "":
            #         DebuggingUtil.print_ment_magenta("하나 이상의 타겟경로가 공백으로 입력되었습니다")
            #         return
            #     if not os.path.exists(directory):
            #         DebuggingUtil.print_ment_magenta("하나 이상의 타겟경로가 존재하지 않습니다")
            #         return

            DebuggingUtil.commentize("빈 트리 리프디렉토리별로 해체한 뒤 제거")
            for index, directory in enumerate(directoryies_):
                if FileSystemUtil.is_empty_tree(directory):
                    for root, directories, files in os.walk(directory, topdown=True):
                        for directory in directories:
                            directory = os.path.abspath(os.path.join(root, directory))
                            if FileSystemUtil.is_leaf_directory(directory):
                                FileSystemUtil.move_target_without_overwrite(target_abspath=directory, dst=StateManagementUtil.EMPTY_DIRECTORYIES)
                                DebuggingUtil.print_ment_via_colorama(rf'directory : {directory}', colorama_color=ColoramaColorUtil.LIGHTWHITE_EX)
                                if directory in directoryies_:
                                    directoryies_.remove(directory)

            DebuggingUtil.commentize("빈 트리 제거된 directoryies_")
            DebuggingUtil.print_ment_via_colorama(rf'directoryies_      : {directoryies_}', colorama_color=ColoramaColorUtil.LIGHTWHITE_EX)
            DebuggingUtil.print_ment_via_colorama(rf'len(directoryies_) : {len(directoryies_)}', colorama_color=ColoramaColorUtil.LIGHTWHITE_EX)

            dst = rf"{os.path.dirname(directoryies_[0])}\{os.path.basename(directoryies_[0]).replace("_$merged", "")}_$merged"
            FileSystemUtil.make_leaf_directory(dst)

            if len(directoryies_) == len(list(set(directoryies_))):
                for index, directory in enumerate(directoryies_):
                    # for target in os.listdir(directoryies_[index]):  # os.listdir 은 without walking 으로 동작한다
                    #     DebuggingUtil.print_ment_via_colorama(rf'{directoryies_[index]}\{target}', colorama_color=ColoramaColorUtil.LIGHTWHITE_EX)
                    #     FileSystemUtil.move_target_without_overwrite(target_abspath=rf'{directoryies_[index]}\{target}', dst=dst)

                    for root, directories, files in os.walk(directoryies_[index], topdown=True):
                        for target in files:
                            FileSystemUtil.move_target_without_overwrite(target_abspath=os.path.join(root, target), dst=dst)

                    # if os.path.isdir(directory):
                    #     while True:
                    #         try:
                    #             if directoryies_[index+1]:
                    #                 pass
                    #         except:
                    #             DebuggingUtil.print_ment_via_colorama(rf"머지시도 중 인덱스가 넘어간것 같습니다. 이를 예외처리하고 넘어갑니다", colorama_color=ColoramaColorUtil.RED)
                    #             break
                    #
                    #
                    #         else:
                    #             DebuggingUtil.print_ment_magenta("디렉토리만 머지하실 수 있습니다")
                    #             break
                    #         break
            else:
                DebuggingUtil.print_ment_magenta("동일한 디렉토리는 머지하실 수 없습니다")
                return

            # 빈 디렉토리 트리 리프디렉토리별로 해체한 뒤 제거
            for index, directory in enumerate(directoryies_):
                if FileSystemUtil.is_empty_tree(directory):
                    for root, directories, files in os.walk(directory, topdown=True):
                        for directory in directories:
                            directory = os.path.abspath(os.path.join(root, directory))
                            if FileSystemUtil.is_leaf_directory(directory):
                                FileSystemUtil.move_target_without_overwrite(target_abspath=directory, dst=StateManagementUtil.EMPTY_DIRECTORYIES)
                                DebuggingUtil.print_ment_via_colorama(rf'directory : {directory}', colorama_color=ColoramaColorUtil.LIGHTWHITE_EX)
                                if directory in directoryies_:
                                    directoryies_.remove(directory)

            # 빈 디렉토리 제거
            for index, directory in enumerate(directoryies_):
                if FileSystemUtil.is_empty_directory(directory):
                    FileSystemUtil.move_target_without_overwrite(target_abspath=directory, dst=StateManagementUtil.EMPTY_DIRECTORYIES)
                    DebuggingUtil.print_ment_via_colorama(rf'directory : {directory}', colorama_color=ColoramaColorUtil.LIGHTWHITE_EX)
                    directoryies_.remove(directory)

    @staticmethod
    def reboot_this_computer():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        FileSystemUtil.get_cmd_output(rf'shutdown -r ')

    @staticmethod
    def shutdown_this_computer():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        FileSystemUtil.get_cmd_output(rf'%windir%\System32\Shutdown.exe -s ')
        # Park4139.get_cmd_output('Shutdown.exe -s ')

    @staticmethod
    def enter_power_saving_mode():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        cmd = rf'%windir%\System32\rundll32.exe powrprof.dll SetSuspendState'
        FileSystemUtil.get_cmd_output(cmd)

    @staticmethod
    def play_wav_file(file_abspath):
        # 종료가 되버린다
        # try:
        #     import playsound
        #     playsound.playsound(file_abspath)
        # except:
        #     pass

        # 너무 느리다.
        # try:
        #     import wave
        #     import pyaudio
        #     # WAV 파일 열기
        #     with wave.open(file_abspath, 'rb') as wav:
        #         audio = pyaudio.PyAudio()
        #         # 스트림 열기
        #         stream = audio.open(format=audio.get_format_from_width(wav.getsampwidth()),
        #                             channels=wav.getnchannels(),
        #                             rate=wav.getframerate(),
        #                             output=True)
        #         # 데이터 읽기
        #         data = wav.readframes(1024)
        #
        #         # 재생
        #         while data:
        #             stream.write(data)
        #             data = wav.readframes(1024)
        #
        #         # 스트림 닫기
        #         stream.stop_stream()
        #         stream.close()
        #
        #         # PyAudio 객체 종료
        #         audio.terminate()
        #
        #     # WAV 파일 닫기
        #     # wav.close()
        # except:
        #     pass

        # 소리 시끄러워서 주석처리, 소리 필요 시 주석해제
        # source = pyglet.media.load(file_abspath)
        # source.play()
        pass

    @staticmethod
    def get_cmd_output(cmd):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        print(rf'{cmd}')

        # os.Popen 으로 print 가능하도록 할 수 있다는 것 같았는데 다른 방식으로 일단 되니까. 안되면 시도.

        # cmd = ['dir', '/b']
        # fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout # 명령어 실행 후 반환되는 결과를 파일에 저장합니다.
        # fd_popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout # shell=True 옵션, cmd를 string 으로 설정
        # lines = fd_popen.read().strip().split('\n')# lines에 저장합니다.
        # fd_popen.close()# 파일을 닫습니다.
        lines = None
        try:
            # alpine linux utf-8 설정을 위해서, docker 파일의 RUN export LANG=en_US.UTF-8 로 대체
            # lines = subprocess.check_output('chcp 65001 >nul', shell=True).decode('utf-8').split('\n')
            lines = subprocess.check_output(cmd, shell=True).decode('utf-8').split('\n')
            return lines
        except UnicodeDecodeError:
            print("UnicodeDecodeError 가 발생했습니다. euc-kr 로 설정하여 명령어 실행을 재시도 합니다")
            try:
                lines = subprocess.check_output(cmd, shell=True).decode('euc-kr').split('\n')
            except Exception:
                print("????????  os.system(cmd)로 재시도 합니다")
                # os.system(cmd)
            return lines
        except subprocess.CalledProcessError:
            [print(sample) for sample in lines]
            print(rf'type(lines) : {type(lines)}')
            print(rf'len(lines) : {len(lines)}')
            print("subprocess.CalledProcessError 가 발생했습니다")
            # os.system(cmd)
            return lines
        except Exception:
            print("예상되지 않은 예외가 발생했습니다.")
            DebuggingUtil.trouble_shoot("%%%FOO%%%")
            return lines

    @staticmethod
    def explorer(target_abspath: str):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        target_abspath = str(target_abspath)
        target_abspath = target_abspath.replace('\"', '')
        target_abspath = rf'explorer "{target_abspath}"'
        print(rf'{target_abspath}')
        try:
            subprocess.check_output(target_abspath, shell=True).decode('utf-8').split('\n')
        except UnicodeDecodeError:
            subprocess.check_output(target_abspath, shell=True).decode('euc-kr').split('\n')
        except subprocess.CalledProcessError:
            pass
        except UnboundLocalError and Exception as e:
            DebuggingUtil.trouble_shoot("202312030015a")

    @staticmethod
    # 프로그램 PID 출력
    def get_current_program_pid():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        pro = subprocess.check_output(
            rf'powershell (Get-WmiObject Win32_Process -Filter ProcessId=$PID).ParentProcessId', shell=True).decode(
            'utf-8')  # 실험해보니 subprocess.check_output(cmd,shell=True).decode('utf-8') 코드는 프로세스가 알아서 죽는 것 같다. 모르겠는데 " " 가 있어야 동작함
        lines = pro.split('\n')
        pids = []
        for line in lines:
            if "" != line.strip():
                pid = line
                pids.append(pid)
                print(f'pid: {pid}')
        return pids

    @staticmethod
    def get_target_bite(start_path='.'):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        return total_size

    @staticmethod
    def get_target_megabite(target_path):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        return FileSystemUtil.get_target_bite(target_path.strip()) / 1024 ** 2

    @staticmethod
    def get_target_gigabite(target_path):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        return FileSystemUtil.get_target_bite(target_path.strip()) / 1024 ** 3

    @staticmethod
    def move_target_to_trash_bin(target_abspath):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")

        # 타겟 휴지통으로 이동
        send2trash.send2trash(target_abspath)

        # 휴지통 열기
        # Park4139.get_cmd_output('explorer.exe shell:RecycleBinFolder')

    @staticmethod
    def xcopy_with_overwrite(target_abspath, future_target_abspath):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        try:
            result = FileSystemUtil.get_cmd_output(rf'echo a | xcopy "{target_abspath}" "{future_target_abspath}" /e /h /k /y')
            if result == subprocess.CalledProcessError:
                if os.path.isfile(target_abspath):
                    FileSystemUtil.get_cmd_output(rf'echo f | xcopy "{target_abspath}" "{future_target_abspath}" /e /h /k /y')
                else:
                    FileSystemUtil.get_cmd_output(rf'echo d | xcopy "{target_abspath}" "{future_target_abspath}" /e /h /k /y')
        except Exception:
            DebuggingUtil.trouble_shoot('%%%FOO%%%')

    @staticmethod
    def xcopy_without_overwrite(target_abspath, future_target_abspath):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        try:
            if os.path.exists(future_target_abspath):
                future_target_abspath = rf"{os.path.dirname(future_target_abspath)}\{os.path.basename(target_abspath)[0]}_{BusinessLogicUtil.get_time_as_('%Y_%m_%d_%H_%M_%S_%f')}{os.path.basename(target_abspath)[1]}"
            FileSystemUtil.get_cmd_output(rf'echo a | xcopy "{target_abspath}" "{future_target_abspath}" /e /h /k')
            if os.path.isfile(target_abspath):
                FileSystemUtil.get_cmd_output(rf'echo f | xcopy "{target_abspath}" "{future_target_abspath}" /e /h /k')
            else:
                FileSystemUtil.get_cmd_output(rf'echo d | xcopy "{target_abspath}" "{future_target_abspath}" /e /h /k')
        except Exception:
            print(rf"subprocess.CalledProcessError 가 발생하여 재시도를 수행합니다 {inspect.currentframe().f_code.co_name}")
            DebuggingUtil.trouble_shoot('%%%FOO%%%')

    @staticmethod
    def is_file_edited(target_abspath: str):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        try:
            key = DbTomlUtil.get_db_toml_key(target_abspath)
            db = DbTomlUtil.read_db_toml()
            line_cnt_measured = BusinessLogicUtil.get_line_cnt_of_file(target_abspath)
            if line_cnt_measured != db[key]:
                DebuggingUtil.commentize("파일편집 감지되었습니다")
            else:
                DebuggingUtil.commentize("파일편집 감지되지 않았습니다")
                pass
            if line_cnt_measured != db[key]:
                return True
            else:
                return False
        except KeyError:
            DbTomlUtil.insert_db_toml(key=DbTomlUtil.get_db_toml_key(target_abspath), value=BusinessLogicUtil.get_line_cnt_of_file(target_abspath))
            DebuggingUtil.commentize("파일편집 확인 중 key 에러가 발생하였습니다")
        except Exception:  # except Exception:으로 작성하면 KeyError 를 뺀 나머지 에러처리 설정 , except: 를 작성하면 모든 에러처리 설정
            DebuggingUtil.commentize("데이터베이스 확인 중 예상되지 않은 에러가 감지되었습니다")
            DebuggingUtil.trouble_shoot("202312030000b")

    @staticmethod
    def move_target_without_overwrite(target_abspath, dst):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        try:
            # 시간 포멧팅 ms 까지 설정
            # get_time_as_() 로 %f 를 pettern 인자에 str 으로서 덧붙여 전달하면, 에러가 났는데
            # time 모듈이 %f 를 지원하지 않아서 나던 것.
            # %f를 지원하는 datetime 으로 교체했다
            target_dirname = os.path.dirname(target_abspath)
            spaceless_time_pattern = rf"{BusinessLogicUtil.get_time_as_('%Y%m%d%H%M%S%f')}"
            target_n = FileSystemUtil.get_target_as_n(target_abspath)
            target_x = FileSystemUtil.get_target_as_x(target_abspath)
            # future_abspath = rf"{dst}\{target_n}{target_x}"
            # future_abspath = copy.deepcopy(future_abspath)

            target_n = re.sub(pattern=r'\$\d{22}', repl='', string=target_n)
            target_abspath_with_timestamp = rf'{target_dirname}\{target_n}${spaceless_time_pattern}{random.randint(10, 99)}{target_x}'  # 시각적으로 _ 가 늘어나니까 좋을 수 도 있음.
            if dst != os.path.dirname(target_abspath_with_timestamp):
                DebuggingUtil.print_ment_via_colorama(ment=rf"target_abspath_with_timestamp : {target_abspath_with_timestamp}", colorama_color=ColoramaColorUtil.LIGHTWHITE_EX)
                DebuggingUtil.print_ment_via_colorama(ment=rf"dst                           : {dst}", colorama_color=ColoramaColorUtil.LIGHTWHITE_EX)
                if os.path.isfile(target_abspath):
                    try:
                        os.rename(target_abspath, target_abspath_with_timestamp)
                        shutil.move(src=target_abspath_with_timestamp, dst=dst)
                        DebuggingUtil.print_ment_via_colorama(ment=rf"파일이동성공", colorama_color=ColoramaColorUtil.LIGHTCYAN_EX)
                    except Exception:
                        # traceback.print_exc()
                        DebuggingUtil.print_ment_via_colorama(ment=rf"파일이동실패", colorama_color=ColoramaColorUtil.RED)
                elif os.path.isdir(target_abspath):
                    try:
                        os.rename(target_abspath, target_abspath_with_timestamp)
                        shutil.move(src=target_abspath_with_timestamp, dst=dst)
                        DebuggingUtil.print_ment_via_colorama(ment=rf"디렉토리이동성공", colorama_color=ColoramaColorUtil.LIGHTCYAN_EX)
                    except Exception:
                        # traceback.print_exc()
                        DebuggingUtil.print_ment_via_colorama(ment=rf"디렉토리이동실패", colorama_color=ColoramaColorUtil.RED)
        except:
            DebuggingUtil.trouble_shoot("202312030021")

    @staticmethod
    def move_without_overwrite_via_robocopy(target_abspath, dst):  # 명령어 자체가 안되는데 /mir 은 되는데 /move 안된다
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        try:
            DebuggingUtil.commentize('타겟이동 시도')
            # Park4139.get_cmd_output(rf'robocopy "{target_abspath}" "{dst}" /MOVE')
            if os.path.exists(rf'{dst}\{os.path.dirname(target_abspath)}'):
                FileSystemUtil.move_target_to_trash_bin(target_abspath)

        except Exception:
            DebuggingUtil.trouble_shoot("202312030021")

    @staticmethod
    def is_empty_tree(directory_path):
        '''디렉토리의 내부를 순회하며 돌면서 모든 하위 디렉토리에 파일이 하나도 없는지를 판단합니다'''
        try:
            # 디렉토리 내부의 파일과 하위 디렉토리 목록을 가져옵니다.
            contents = os.listdir(directory_path)

            # 파일이 존재하는 경우, 디렉토리가 비어있지 않습니다.
            for content in contents:
                content_path = os.path.join(directory_path, content)
                if os.path.isfile(content_path):
                    return False

            # 디렉토리가 비어있습니다.
            return True
        except FileNotFoundError:
            DebuggingUtil.print_ment_via_colorama('FileNotFoundError', colorama_color=ColoramaColorUtil.RED)
        except OSError:
            DebuggingUtil.print_ment_via_colorama('OSError', colorama_color=ColoramaColorUtil.RED)
        except UnboundLocalError:
            DebuggingUtil.print_ment_via_colorama('UnboundLocalError', colorama_color=ColoramaColorUtil.RED)

    @staticmethod
    def is_leaf_directory(directory_path):
        # leaf 디렉토리란, 하위 디렉토리를 가지지 않는 가장 마지막 단계의 디렉토리를 말합니다

        # 디렉토리 내부의 파일과 하위 디렉토리 목록을 가져옵니다.
        try:
            contents = os.listdir(directory_path)

            # 디렉토리 내에 파일이 존재하면 leaf 디렉토리가 아닙니다.
            if len(contents) > 0:
                return False

            # 디렉토리 내에 하위 디렉토리가 존재하는지 확인합니다.
            for content in contents:
                content_path = os.path.join(directory_path, content)
                if os.path.isdir(content_path):
                    return False

            # 디렉토리가 leaf 디렉토리입니다.
            return True
        except FileNotFoundError:
            DebuggingUtil.print_ment_via_colorama('FileNotFoundError', colorama_color=ColoramaColorUtil.RED)
        except:
            DebuggingUtil.print_ment_via_colorama(f'{inspect.currentframe().f_code.co_name}() 기타에러발생', colorama_color=ColoramaColorUtil.RED)

    @staticmethod
    def add_text_to_file(file_abspath, text):
        with open(file_abspath, 'a') as file:
            file.write(text)

    @staticmethod
    def get_cnts_of_line_of_file(file_abspath):
        with open(file_abspath, 'r') as file:
            return sum(1 for line in file)

    @staticmethod
    def is_letters_cnt_zero(file_abspath):
        try:
            with open(file_abspath, 'r') as file:
                contents = file.read().strip()
                # print(rf'len(contents) : {len(contents)}')
                if len(contents) == 0:
                    return True
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")
            return False
        except UnicodeDecodeError:
            with open(file_abspath, 'r', encoding='utf-8') as file:
                contents = file.read().strip()
                # print(rf'len(contents) : {len(contents)}')
                if len(contents) == 0:
                    return True
            return False
        except:
            DebuggingUtil.trouble_shoot("%%%FOO%%%")
            print("오류가 발생했습니다.")
            return False


#


#     time_s = 0.0
#     time_e = 0.0
#     biggest_targets = []  # 300 MB 이상 빽업대상
#     smallest_targets = []
#
#     # speak() 쓰레드 상태관리용
#     # is_speak_as_async_running = False
#     pyglet_player = None
#     playing_sounds = []
#     previous_mp3_length_used_in_speak_as_async = 0
#
#     routines_promised = [
#         '물 한컵',
#         '선풍기로 방환기 1분 이상',
#         '세수',
#         '로션',
#         '아침식사',
#         "프로폴리스 한알",
#         '물가글(혹시 구내염 있으시면 가글양치)',
#         '양치 WITHOUT TOOTH PASTE',
#         '양치 WITH TOOTH PASTE',
#         '양치 WITH GARGLE',
#         '물가글',
#         '즐거운일 1개',
#         '스트레칭 밴드 V 유지 런지 30개',
#         '계단 스쿼트 30 개',
#         '푸쉬업 30 개',
#         '점심식사',
#         '저녁식사',
#         # '음악틀기',
#     ]
#     count_of_make_me_go_to_sleep = []
#
#     def __init__(self):
#
#         try:
#             os.system('chcp 65001 >nul')
#             BusinessLogicUtil.PYCHARM64_EXE = rf'{os.environ.get("PyCharm Community Edition").replace(";", "")}\pycharm64.exe'
#         except AttributeError:
#             pass
#         except Exception:
#             DebuggingUtil.trouble_shoot("%%%FOO%%%")
#
#
class MentsUtil:
    NO = "아니"
    YES = "응"
    CHECKED = "확인"
    OK_I_WILL_DO_IT_NOW = "지금할게"
    DONE = "했어"
    I_WANT_TO_TO_DO_NEXT_TIME = "다음에 할게"


class DataStructureUtil:
    @staticmethod
    def get_list_added_elements_alternatively(list_for_odd, list_for_even):  # from [1, 2, 3] + [ x, y, z] to [1,x,2,y,3,z]
        """
        두 리스트를 더할때 사용하는 함수
        list, ndarray 모두 사용이 가능한 함수이다.

        result = get_list_added_elements_alternatively(list1 = [1, 2, 3], list_to_added_as_even_order = ['x', 'y', 'z'])
        """
        result = []
        for i in range(len(list_for_odd)):
            result.append(list_for_odd[i])
            if i < len(list_for_even):
                result.append(list_for_even[i])
        return result

    @staticmethod
    def print_list_each_two_elements(list: []):  # print(rf'list[index] list[index+1] : {list[index]} {list[index+1]}') without out of index
        for index, item in enumerate(list):  # enumerate 로 리스트의 원소를 2개씩 출력
            if index + 1 < len(list):
                print(rf'list[index] list[index+1] : {list[index]} {list[index + 1]}')

    @staticmethod
    def get_list_each_two_elements_joined(list: []):  # from ["a", "b", "c", "d"] to ["ab", "cd"]
        return [f"{list[i]}{list[i + 1]}" for i in range(0, len(list), 2)]

    @staticmethod
    def get_nested_list_grouped_by_each_two_elements_in_list(list: []):  # from ["a", "b", "c", "d"] to [["a","b"], ["c","d"]]
        result = []
        for i in range(0, len(list), 2):
            if i + 1 < len(list):
                result.append([list[i], list[i + 1]])
        return result

    @staticmethod
    def get_column_of_2_dimension_list(list_2_dimension: [], column_no):  # return 은 list 아니고 ndarray 일 수 있다
        import numpy as np
        arr = np.array(list_2_dimension)
        second_column = arr[:, column_no]
        print(second_column)

    @staticmethod
    def get_nested_list_converted_from_ndarray(ndarray: numpy.ndarray):  # ndarray 에서 list 로 변환 # ndarray 에서 list 로 변환 # ndarray to nested []  from [[1 2]] to [[1, 2]] # from [ [str str] [str str] ]  to  [ [str, str], [str, str] ]
        return ndarray.tolist()

    @staticmethod
    def get_nested_list_sorted_by_column_index(nested_list: [[str]], column_index: int, decending_order=False):  # tree depth(sample[1]) 에 대한 내림차순 정렬 # list 2차원 배열의 특정 열의 내림차순 정렬 # from [[str, str]] to [[str, str]]
        """
         중첩리스트를 첫 번째 행을 기준으로 내림차순으로 정렬
         from
         [
             [ 1 a z ]
             [ 7 a b ]
             [ 4 a c ]
         ]
         to
         [
             [ 7 a b ]
             [ 4 a c ]
             [ 1 a z ]
         ]
         튜플도 된다
         from
         [
             ( 1 a z )
             ( 7 a b )
             ( 4 a c )
         ]
         to
         [
             ( 7 a b )
             ( 4 a c )
             ( 1 a z )
         ]
        """

        def bubble_sort_nested_list(nested_list, column_index):
            """버블 소팅 테스트"""
            if type(nested_list[0][column_index]) == float:
                column_index = int(column_index)
                n = len(nested_list)
                for i in range(n):
                    for j in range(0, n - i - 1):
                        if decending_order == True:
                            if int(str(nested_list[j][column_index]).replace(".", "")) < int(str(nested_list[j + 1][column_index]).replace(".", "")):
                                nested_list[j], nested_list[j + 1] = nested_list[j + 1], nested_list[j]
                        elif decending_order == False:
                            if int(str(nested_list[j][column_index]).replace(".", "")) > int(str(nested_list[j + 1][column_index]).replace(".", "")):
                                nested_list[j], nested_list[j + 1] = nested_list[j + 1], nested_list[j]
                return nested_list
            elif type(nested_list[0][column_index]) == int or nested_list[0][column_index].isdigit():  # 에고 힘들다. 머리아팠다
                column_index = int(column_index)
                n = len(nested_list)
                for i in range(n):
                    for j in range(0, n - i - 1):
                        if decending_order == True:
                            if int(nested_list[j][column_index]) < int(nested_list[j + 1][column_index]):
                                # print(rf'{nested_list[j][column_index]}>{nested_list[j + 1][column_index]}')
                                # print(rf'nested_list[j][column_index] > nested_list[j+1][column_index] : {int(nested_list[j][column_index]) > int(nested_list[j+1][column_index])}')
                                nested_list[j], nested_list[j + 1] = nested_list[j + 1], nested_list[j]
                        elif decending_order == False:
                            if int(nested_list[j][column_index]) > int(nested_list[j + 1][column_index]):
                                # print(rf'{nested_list[j][column_index]}>{nested_list[j + 1][column_index]}')
                                # print(rf'nested_list[j][column_index] > nested_list[j+1][column_index] : {int(nested_list[j][column_index]) > int(nested_list[j+1][column_index])}')
                                nested_list[j], nested_list[j + 1] = nested_list[j + 1], nested_list[j]
                return nested_list
            elif type(nested_list[0][column_index]) == str:
                column_index = int(column_index)
                n = len(nested_list)
                for i in range(n):
                    for j in range(0, n - i - 1):
                        if decending_order == True:
                            if nested_list[j][column_index] < nested_list[j + 1][column_index]:
                                # print(rf'{nested_list[j][column_index]}>{nested_list[j + 1][column_index]}')
                                # print(rf'nested_list[j][column_index] > nested_list[j+1][column_index] : {int(nested_list[j][column_index]) > int(nested_list[j+1][column_index])}')
                                nested_list[j], nested_list[j + 1] = nested_list[j + 1], nested_list[j]
                        if decending_order == False:
                            if nested_list[j][column_index] > nested_list[j + 1][column_index]:
                                # print(rf'{nested_list[j][column_index]}>{nested_list[j + 1][column_index]}')
                                # print(rf'nested_list[j][column_index] > nested_list[j+1][column_index] : {int(nested_list[j][column_index]) > int(nested_list[j+1][column_index])}')
                                nested_list[j], nested_list[j + 1] = nested_list[j + 1], nested_list[j]
                return nested_list

        return bubble_sort_nested_list(nested_list, column_index)

    @staticmethod
    def get_nested_list_removed_row_that_have_nth_element_dulplicated_by_column_index_for_ndarray(ndarray: [[]], column_index: int):  # 중복된 행 제거하는게 아니고 행의 2번째 요소가 중복되는 것을 제거
        seen = set()
        unique_rows = []
        for row in ndarray:
            if row[column_index] not in seen:
                unique_rows.append(row)
                seen.add(row[column_index])
        return unique_rows

    @staticmethod
    def get_nested_list_removed_row_that_have_nth_element_dulplicated_by_column_index(nested_list: [[]], column_index: int):  # 중복된 행 제거하는게 아니고 행의 2번째 요소가 중복되는 것을 제거
        seen = set()  # 중복된 행의 두 번째 요소를 추적하기 위한 집합(set) 생성
        unique_rows = []
        for row in nested_list:
            if row[column_index] not in seen:
                unique_rows.append(row)  # 중복된 행의 두 번째 요소가 중복되지 않는 행들만 추출하여 unique_rows 리스트에 추가
                seen.add(row[column_index])
        return unique_rows  # 중복된 행의 두 번째 요소가 중복되지 않는 행들만 남게 됩니다.

    @staticmethod
    def get_list_seperated_by_each_elements_in_nested_list(nested_list):
        return [item for sublist in nested_list for item in sublist]

    @staticmethod
    def is_two_lists_equal(list1, list2):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        # 두 리스트의 요소들이 동일한지만 확인 # 하나라도 발견되면 탐색 중지 # 두 리스트의 동일 인덱스에서 진행하다 달라도 다른거다
        if len(list1) != len(list2):
            print(f"두 리스트의 줄 수가 다릅니다 {len(list1)}, {len(list2)}")
            return False
        for i in range(len(list1)):
            if list1[i] != list2[i]:
                print(f"두 리스트의 같은 인덱스 중 다른 리스트 발견={list1[i]}, {list2[i]}")
                return False
        return True

    @staticmethod
    def get_elements_that_list1_only_have(list1, list2):  # 두 개의 리스트를 비교하여 특정 하나의 리스트 만 가진 요소만 모아서 리스트로 출력
        unique_elements_of_list1 = []
        for element in list1:
            if element not in list2:
                unique_elements_of_list1.append(element)
        return unique_elements_of_list1

    @staticmethod
    def get_different_elements(list1, list2):  # 두 개의 리스트를 비교하여 서로 다른 요소만 모아서 리스트로 출력
        different_elements = []
        # 두 리스트 중 더 긴 리스트의 길이를 구합니다.
        max_length = max(len(list1), len(list2))
        # 범위는 더 긴 리스트의 길이로 설정합니다.
        for i in range(max_length):
            # 리스트의 인덱스가 범위 내에 있는지 확인 후 비교합니다.
            if i < len(list1) and i < len(list2):
                if list1[i] != list2[i]:
                    different_elements.append(list1[i])
            else:
                # 한 리스트는 범위를 벗어났으므로 해당 요소를 추가합니다.
                if i >= len(list1):
                    different_elements.append(list2[i])
                else:
                    different_elements.append(list1[i])
        # 위의 코드는 5 초 경과

        different_elements = []
        # set1 = set(list1)  # list to set
        # set2 = set(list2)
        # different_elements = list(set1.symmetric_difference(set2))
        # 위의 코드는 12 초 경과
        return different_elements

    @staticmethod
    def get_common_elements(list1, list2):  # 두 개의 리스트를 비교하여 서로 동일한 요소만 새로운 리스트로 출력 # 중복값 색출
        common_elements = []
        for element in list1:
            if element in list2:
                common_elements.append(element)
        return common_elements

    @staticmethod
    def add_suffix_to_string_list(string_list, suffix):
        result = []
        for string in string_list:
            result.append(string + suffix)
        return result

    @staticmethod
    def add_prefix_to_string_list(string_list, prefix):
        result = []
        for string in string_list:
            result.append(prefix + string)
        return result


class SeleniumUtil:
    @staticmethod
    def get_driver_for_selenium():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        import selenium.webdriver as webdriver
        # DebuggingUtil.commentize("웹 드라이버 설정")
        options = SeleniumUtil.get_webdriver_options_customed()

        # # driver = webdriver.Chrome(options=options,executable_path=rf"{os.getcwd()}\pkg_chrome_driver\chrome-win64\chrome.exe")
        # # executable_url 를 지워야겠다, because you have installed the latest version of Selenium if you have selenium above the 4.6.0
        # # you don't need to add executable_url and in the latest version of Selenium you don't need to download webdriver.
        # # stackoverflow 이렇다고 한다. chromedriver의 추가 설치가 불필요해졌다

        driver = webdriver.Chrome(options=options)
        driver.get('about:blank')
        driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")  # hide plugin 0EA
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")  # hide own lanuages
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        driver.execute_script("const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")  # hide own gpu # WebGL렌더러를 Nvidia회사와 GTX980Ti엔진인 ‘척’ 하는 방법입니다.
        return driver

    @staticmethod
    def get_webdriver_options_customed():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        import selenium.webdriver as webdriver
        options = webdriver.ChromeOptions()

        # 백그라운드 실행 설정
        # headless 옵션은 브라우저를 화면에 표시하지 않고 백그라운드에서 실행하는 모드 설정
        options.add_argument('headless')

        # options.add_argument('window-size=1920x1080')
        options.add_argument('window-size=3440x1440')  # size 하드코딩 되어 있는 부분을 pyautogui 에서 size() 로 대체하는 것이 좋겠다.
        options.add_argument("lang=ko_KR")  # 한국어!
        options.add_argument("disable-gpu")  # 문제 있을 수 있음, 아래는 그 대안코드
        # options.add_argument("--disable-gpu")
        # hide headless, UserAgent headless 탐지 방지
        # UserAgent 값 얻는 방법, 일반 크롬으로 https://www.whatismybrowser.com/detect/what-is-my-user-agent/ 에 접속해서 얻어온다
        user_agent_value = "Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        options.add_argument(f"user-agent={user_agent_value}")
        # options.add_argument("proxy-server=localhost:8080")
        return options


class BusinessLogicUtil:

    @staticmethod
    def get_none_count_of_list(list):
        count = sum(element is None for element in list)
        return count

    @staticmethod
    def get_validated(target: any):
        if target == None:
            target = "논값"
        if target == "":
            target = "공백"
        if type(target) == str:
            if BusinessLogicUtil.is_regex_in_contents(target=target, regex=r'[^a-zA-Z0-9가-힣\s]'):  # 특수문자 패턴 정의( 알파벳, 숫자, 한글, 공백을 제외한 모든 문자)
                target = BusinessLogicUtil.get_str_replaced_special_characters(target, "$특수문자$")
            return target
        else:
            return target

    @staticmethod
    def is_validated(target: any):
        if target == None:
            return False
        if target == "":
            return False
        if BusinessLogicUtil.is_regex_in_contents(target=target, regex=r'[^a-zA-Z0-9가-힣\s]'):  # 특수문자 패턴 정의( 알파벳, 숫자, 한글, 공백을 제외한 모든 문자)
            return False
        else:
            return True

    @staticmethod
    # def guide_user_input_intended_by_developer(user_input: str):
    def is_user_input_sanitized(user_input: str):
        # 수정 필요.
        user_input = user_input.strip()
        if TextToSpeechUtil.is_only_no(user_input):
            user_input = int(user_input)
        else:
            TextToSpeechUtil.speak_ments("you can input only number, please input only number again", sleep_after_play=0.65)
            return None
        return user_input

    @staticmethod
    def validate_and_return(value: str):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        try:
            print(rf'value : {value}')
            print(rf'type(value) : {type(value)}')
            print(rf'len(value) : {len(value)}')
        except:
            pass
        if value == None:
            print(rf'벨리데이션 테스트 결과 : None')
            return False
        if value == "":
            print(rf'벨리데이션 테스트 결과 : 공백')
            return False
        # if 전화번호만 같아 보이는지
        # if 특수문자만 같아 보이는지
        return value

    @staticmethod
    def get_biological_age(birth_day):
        # 2023-1994=29(생일후)
        # 2024-1994=30(생일후)
        # 만나이 == 생물학적나이
        # 생일 전 만나이
        # 생일 후 만나이
        pass

    # @staticmethod
    # def should_i_do(ment: str, function: Callable = None, is_void_mode: bool = True, auto_click_negative_btn_after_seconds: int = None, auto_click_positive_btn_after_seconds: int = None):
    #     DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
    #     # function() 이 void 함수 일때 시도, is_void_mode= True 설정인 경우, is_void_mode 파라미터 제거 대기
    #     if is_void_mode != True:
    #         if auto_click_negative_btn_after_seconds == None and auto_click_positive_btn_after_seconds == None:
    #             auto_click_negative_btn_after_seconds = 30
    #         while True:
    #             # ??? = input()# input() 으로 대체 해야한다.
    #             DebuggingUtil.print_ment_magenta(ment=ment, btns=[MentsUtil.YES, MentsUtil.NO], auto_click_negative_btn_after_seconds=auto_click_negative_btn_after_seconds, auto_click_positive_btn_after_seconds=auto_click_positive_btn_after_seconds)
    #
    #             if dialog.btn_text_clicked == MentsUtil.YES:
    #                 if function != None:
    #                     function()
    #             else:
    #                 break
    #             break

    @staticmethod
    def do_random_schedules():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        int_random = random.randint(0, 7)
        # Park4139Park4139.Tts.speak(f'랜덤숫자 {int_random} 나왔습니다')
        # mkmk
        if int_random == 0:
            pass
        elif int_random == 1:
            pass
        elif int_random == 2:
            pass
        elif int_random == 3:
            BusinessLogicUtil.change_console_color()
        elif int_random == 4:
            pass
        elif int_random == 5:
            pass
        elif int_random == 6:
            pass
        elif int_random == 7:
            pass

    @staticmethod
    def sleep(milliseconds=None, sec=None, min=None, hour=None, printing_mode=True):
        # DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        params_list = [milliseconds, sec, min, hour]
        # 리스트 내 요소가 3개만 None 인지 확인
        if BusinessLogicUtil.get_none_count_of_list(params_list) == 3:
            # milliseconds = None, sec = None, min = None, hour = None, 이 중 하나만 None 이 아니면 동작
            time_to_sleep = None
            if milliseconds is not None:
                seconds = milliseconds / 1000
                if printing_mode:
                    DebuggingUtil.print_ment_via_colorama(f"{inspect.currentframe().f_code.co_name}(ms={milliseconds})", colorama_color=ColoramaColorUtil.WHITE)
                time_to_sleep = seconds
            elif sec is not None:
                if printing_mode:
                    DebuggingUtil.print_ment_via_colorama(f"{inspect.currentframe().f_code.co_name}(seconds={sec})", colorama_color=ColoramaColorUtil.WHITE)
                time_to_sleep = sec
            elif min is not None:
                if printing_mode:
                    DebuggingUtil.print_ment_via_colorama(f"{inspect.currentframe().f_code.co_name}(minutes={min})", colorama_color=ColoramaColorUtil.WHITE)
                time_to_sleep = 60 * min
            elif hour is not None:
                if printing_mode:
                    DebuggingUtil.print_ment_via_colorama(f"{inspect.currentframe().f_code.co_name}(hours={hour})", colorama_color=ColoramaColorUtil.WHITE)
                time_to_sleep = 60 * 60 * hour
            if time_to_sleep is not None:
                time.sleep(time_to_sleep)
        else:
            DebuggingUtil.print_ment_via_colorama(f'sleep() 메소드는 milliseconds, sec, min, hour 중 하나만 단위만 설정할 수 있습니다', colorama_color=ColoramaColorUtil.RED)

            # raise Error() 위의 코드말고 이런식으로 처리할까 싶은데

    @staticmethod
    def get_os_sys_environment_variable(environment_variable_name: str):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        DebuggingUtil.commentize("모든 시스템 환경변수 출력")
        for i in os.environ:
            DebuggingUtil.print_ment_magenta(i)
        return os.environ.get(environment_variable_name)

    @staticmethod
    def update_os_sys_environment_variable(environment_variable_name: str, new_path: str):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        """시스템 환경변수 path 업데이트"""
        DebuggingUtil.commentize("테스트가 필요한 함수를 적용하였습니다")
        DebuggingUtil.commentize("기대한 결과가 나오지 않을 수 있습니다")
        DebuggingUtil.commentize("업데이트 전 시스템 환경변수")
        for i in sys.path:
            DebuggingUtil.print_ment_magenta(i)
        sys.path.insert(0, new_path)
        sys.path.append(new_path)
        DebuggingUtil.commentize("업데이트 전 시스템 환경변수")
        for i in sys.path:
            DebuggingUtil.print_ment_magenta(i)

    @staticmethod
    def get_name_space():  # name space # namespace # 파이썬 네임스페이스
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        dir()
        return dir()

    @staticmethod
    def back_up_target(target_abspath):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        try:
            while True:
                # 전처리
                target_abspath = target_abspath.replace("\n", "")
                target_abspath = target_abspath.replace("\"", "")

                if target_abspath.strip() == "":
                    TextToSpeechUtil.speak_ments(ment="빽업할 대상이 입력되지 않았습니다", sleep_after_play=0.65)
                    break

                target_dirname = os.path.dirname(target_abspath)
                target_dirname_dirname = os.path.dirname(target_dirname)
                target_basename = os.path.basename(target_abspath).split(".")[0]
                target_zip = rf'{target_dirname}\$zip_{target_basename}.zip'
                target_yyyy_mm_dd_hh_mm_ss_zip_basename = rf'{target_basename} - {BusinessLogicUtil.get_time_as_("%Y %m %d %H %M %S")}.zip'
                DebuggingUtil.print_ment_magenta(f"target_abspath : {target_abspath}")
                DebuggingUtil.print_ment_magenta(f"target_dirname : {target_dirname}")
                DebuggingUtil.print_ment_magenta(f"target_dirname_dirname : {target_dirname_dirname}")
                DebuggingUtil.print_ment_magenta(f"target_basename : {target_basename}")
                DebuggingUtil.print_ment_magenta(f"target_zip : {target_zip}")
                DebuggingUtil.print_ment_magenta(f"target_yyyy_mm_dd_HH_MM_SS_zip_basename : {target_yyyy_mm_dd_hh_mm_ss_zip_basename}")

                DebuggingUtil.commentize(f"{target_zip} 로 빽업")
                cmd = f'bz.exe c "{target_zip}" "{target_abspath}"'
                FileSystemUtil.get_cmd_output(cmd)

                DebuggingUtil.commentize(rf'{target_yyyy_mm_dd_hh_mm_ss_zip_basename} 로 이름변경')
                cmd = rf'ren "{target_zip}" "{target_yyyy_mm_dd_hh_mm_ss_zip_basename}"'
                FileSystemUtil.get_cmd_output(cmd)

                # DebuggingUtil.commentize('현재 프로그램 pid 출력')
                # # os.system(rf'powershell (Get-WmiObject Win32_Process -Filter ProcessId=$PID).ParentProcessId')

                DebuggingUtil.commentize(rf'현재 디렉토리에서 zip 확장자 파일만 문자열 리스트로 출력')
                # 파일이 위치한 드라이브로 이동
                drives = [
                    "C",
                    "D",
                    "E",
                    "F",
                    "G",
                ]
                drive_where_target_is_located = target_abspath.split(":")[0].upper()
                for drive in drives:
                    if (drive_where_target_is_located == drive):
                        os.system(rf"cd {drive}:")
                DebuggingUtil.commentize("target_dirname 로 이동")
                try:
                    os.chdir(target_dirname)
                except:
                    TextToSpeechUtil.speak_ments(ment="경로를 이해할 수 없습니다", sleep_after_play=0.65)
                    os.chdir(StateManagementUtil.PROJECT_DIRECTORY)
                    break
                lines = FileSystemUtil.get_cmd_output('dir /b /a-d *.zip')
                for line in lines:
                    if line != "":
                        if os.getcwd() != line:  # 여기 os.getcwd() 이게 들어가네... 나중에 수정하자
                            # 2023-12-04 월 12:14 SyntaxWarning: invalid escape sequence '\d'
                            # r 을 사용 Raw String(원시 문자열),  \를 모두 제거
                            # 정규식은 r 쓰면 안된다. \ 써야한다?.
                            # 2023-12-12 화 14:23 SyntaxWarning: invalid escape sequence '\d'
                            # 가상환경 재설치 후 또 문제가 나타남,
                            # regex = 'd{4} d{2} d{2} d{2} d{2} d{2}'
                            # regex = r'\d{4} \d{2} \d{2} \d{2} \d{2} \d{2}'
                            regex = r'd{4} d{2} d{2} d{2} d{2} d{2}'
                            # Park4139.debug_as_cli(line)
                            if BusinessLogicUtil.is_regex_in_contents(line, regex):
                                DebuggingUtil.commentize(f"zip 파일 목록에 대하여 {regex} 타임스탬프 정규식 테스트를 통과했습니다")
                                # Park4139.debug_as_cli(line)
                                # 2023-12-03 일 20:03 trouble shooting 성공
                                # 빽업 시 타임스탬프에 언더바 넣도록 변경했는데 regex 는 변경 하지 않아서 난 실수 있었음.
                                time_to_backed_up = re.findall(regex, line)
                                time_to_backed_up_ = time_to_backed_up[0][0:10].replace(" ", "-") + " " + time_to_backed_up[0][11:16].replace(" ", ":") + ".00"
                                time_to_backed_up__ = datetime.strptime(str(time_to_backed_up_), '%Y-%m-%d %H:%M.%S')
                                time_current = datetime.now()
                                try:
                                    target_dirname_old = rf'{target_dirname}\$cache_zip'
                                    if not os.path.exists(target_dirname_old):
                                        os.makedirs(target_dirname_old)
                                except Exception:
                                    DebuggingUtil.trouble_shoot("%%%FOO%%%")
                                    os.chdir(StateManagementUtil.PROJECT_DIRECTORY)
                                    break
                                # 지금부터 7일 이전의 파일만
                                # diff = time_to_backed_up__ - time_current
                                # if diff.days <-7:
                                # Park4139.debug_as_cli(f"line : {line}")

                                # DebuggingUtil.commentize(f"1분(60 seconds) 이전의 파일자동정리 시도...")
                                DebuggingUtil.commentize(f"파일자동정리 시도...")
                                change_min = time_current - timedelta(seconds=60)
                                diff = time_to_backed_up__ - change_min
                                if 60 < diff.seconds:
                                    try:
                                        file_with_time_stamp_zip = os.path.abspath(line.strip())
                                        file_dirname_old_abspath = os.path.abspath(target_dirname_old)
                                        DebuggingUtil.print_ment_magenta(rf'move "{file_with_time_stamp_zip}" "{file_dirname_old_abspath}"')
                                        shutil.move(file_with_time_stamp_zip, file_dirname_old_abspath)
                                    except Exception:
                                        DebuggingUtil.trouble_shoot("%%%FOO%%%")
                                        os.chdir(StateManagementUtil.PROJECT_DIRECTORY)
                                        break
                os.chdir(StateManagementUtil.PROJECT_DIRECTORY)
                DebuggingUtil.print_ment_magenta(ment=f"약속된 백업이 성공되었습니다\n{target_abspath}")
                break
        except:
            DebuggingUtil.trouble_shoot("%%%FOO%%%")
            os.chdir(StateManagementUtil.PROJECT_DIRECTORY)

    @staticmethod
    def monitor_target_edited_and_back_up(target_abspath: str):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        try:
            if os.path.isfile(target_abspath):
                if FileSystemUtil.is_file_changed(target_abspath):
                    BusinessLogicUtil.back_up_target(target_abspath)
            elif os.path.isdir(target_abspath):
                if FileSystemUtil.is_directory_changed(target_abspath):
                    BusinessLogicUtil.back_up_target(target_abspath)
        except:
            DebuggingUtil.trouble_shoot("%%%FOO%%%")

    @staticmethod
    def monitor_target_edited_and_sync(target_abspath: str):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        try:
            if os.path.isfile(target_abspath):
                if FileSystemUtil.is_file_changed(target_abspath):
                    FileSystemUtil.sync_directory_local(target_abspath)
            elif os.path.isdir(target_abspath):
                FileSystemUtil.sync_directory_local(target_abspath)
        except:
            DebuggingUtil.trouble_shoot("%%%FOO%%%")

    @staticmethod
    def print_and_open_py_pkg_global_path():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        for path in sys.path:
            DebuggingUtil.print_ment_magenta(path)
            if BusinessLogicUtil.is_regex_in_contents(target=path, regex='site-packages') == True:
                DebuggingUtil.print_ment_magenta(rf'echo "{path}"')
                FileSystemUtil.explorer(path)

    @staticmethod
    def taskkill(program_img_name):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        program_img_name = program_img_name.replace("\'", "")
        program_img_name = program_img_name.replace("\"", "")
        FileSystemUtil.get_cmd_output(f'taskkill /f /im "{program_img_name}"')
        FileSystemUtil.get_cmd_output(f'wmic process where name="{program_img_name}" delete ')

    # 2023-12-07 목요일 16:51 최신화 함수
    @staticmethod
    def afterpause(function):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")

        def wrapper(*args, **kwargs):
            DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
            function(*args, **kwargs)
            TestUtil.pause()
            pass

        return wrapper

    @staticmethod
    def get_time_as_(pattern: str):
        #  %Y-%m-%d %H:%M:%S 의 형태도 모두 쓸 수 있고, 특정해둔 키워드도 쓸 수 있다
        # 어느날 보니 이 함수가 의도한대로 동작이 안됬다, 테스트를 해서 고쳤는데, for 문이 다른 값을 반환하는 것이 문제였다.
        # 테스트를 하지 않고 넘어 갔던 것이 문제였다. 꼭 함수를 만들었을 때는 함수에 대한 기능 테스트 하자
        # time 은 ms 지원않한다. 즉 %f 사용불가...
        # datetime 은 ms 지원!.  즉 %f 가능
        import time
        now = time
        localtime = now.localtime()
        from datetime import datetime
        time_styles = {
            'now': str(now.time()),
            'yyyy': str(localtime.tm_year),
            'MM': str(localtime.tm_mon),
            'dd': str(localtime.tm_mday),
            'HH': str(localtime.tm_hour),
            'mm': str(localtime.tm_min),
            'ss': str(localtime.tm_sec),
            'weekday': str(localtime.tm_wday),
            'elapsed_days_from_jan_01': str(localtime.tm_yday),  # 이거 테스트해보자 네이밍으로는 금년 1월 1일 부터 오늘까지 몇일이 지났는가를 출력하는 것 같아 보인다
        }
        for key, value in time_styles.items():
            if key == pattern:
                return time_styles[pattern]
        return str(datetime.now().strftime(pattern))

    @staticmethod
    def parse_youtube_video_id(url):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        """
        code written by stack overflow (none regex way)
        파이썬에 내장 url 구문 분석 기능
        this method return String or None
        Strng 을 리턴했다면 유튜브 비디오 아이디로 기대할 수 있다
        """
        query = urllib_parser.urlparse(url=url)
        if query.hostname == 'youtu.be':
            # DebuggingUtil.print_ment_magenta()(f"query.path[1:] : {query.path[1:]}")
            return query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            # Park4139.debug_as_cli(query.scheme)
            # Park4139.debug_as_cli(query.netloc)
            # Park4139.debug_as_cli(query.hostname)
            # Park4139.debug_as_cli(query.port)
            # Park4139.debug_as_cli(query._replace(fragment="").geturl())
            # Park4139.debug_as_cli(query)
            # Park4139.debug_as_cli(query["v"][0])
            if query.path == '/watch':
                p = urllib_parser.parse_qs(query.query)
                # DebuggingUtil.print_ment_magenta()(f"p['v'][0] : {p['v'][0]}")
                return p['v'][0]
            if query.path[:7] == '/embed/':
                # DebuggingUtil.print_ment_magenta()(f"query.path.split('/')[2] : {query.path.split('/')[2]}")
                return query.path.split('/')[2]
            if query.path[:3] == '/v/':
                # DebuggingUtil.print_ment_magenta()(f"query.path.split('/')[2] : {query.path.split('/')[2]}")
                return query.path.split('/')[2]

    @staticmethod
    def download_clip(url: str):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        while True:
            if url.strip() == "":
                DebuggingUtil.print_ment_magenta(rf"다운로드할 url이 아닙니다 {url}")
                break
            # 다운로드가 안되면 주석 풀어 시도
            # os.system(rf'{StateManagementUtil.YT_DLP_CMD} -U')

            # Park4139.raise_error('의도적으로 에러를 발생 중...')
            # if
            #     Park4139.debug_as_cli(rf'다운로드가 된 url 입니다 {url}')
            #

            print('다운로드 옵션 파싱 중...')
            video_id = ''
            # lines = subprocess.check_output(rf'{StateManagementUtil.YT_DLP_CMD} -F {url}', shell=True).decode('utf-8').split("\n")

            cmd = rf'{StateManagementUtil.YT_DLP_CMD} -F {url}'
            lines = FileSystemUtil.get_cmd_output(cmd=cmd)
            # 순서는 우선순위에 입각해 설정되었다. 순서를 바꾸어서는 안된다.
            video_ids_allowed = [
                '616',
                '315',
                '313',
                '303',
                '302',
                '308',
                '616',
                '248',
                '247',
                '244',
                '137',
                '136',
            ]
            audio_ids_allowed = [
                '250',
                '251',
            ]
            audio_id = ""
            for line in lines:  # mkmk
                if 'video only' in line or 'audio only' in line:
                    DebuggingUtil.print_ment_magenta(line)
                    # video_id 설정
                    for id in video_ids_allowed:
                        if id in line:
                            video_id = id
                            if video_id.strip() == "":
                                DebuggingUtil.print_ment_magenta(rf"다운로드 할 수 있는 video_id가 아닙니다 {video_id.strip()}")
                                break
                    # audio_id 설정
                    for id in audio_ids_allowed:
                        if id in line:
                            audio_id = id
                            if audio_id.strip() == "":
                                DebuggingUtil.print_ment_magenta(rf"다운로드 할 수 있는 audio_id가 아닙니다 {audio_id.strip()}")
                                break

            # 다운로드 가능 옵션 ID 설정
            # if video_id not in video_ids and audio_id not in audio_ids:
            #     video_id = str(input('video option:'))
            #     audio_id = str(input('audio option:'))
            #     speak(rf'다운로드 옵션이 선택되었습니다')
            #     Park4139.debug_as_cli(rf'video option: {video_id}  audio option: {audio_id}')
            #     speak(rf'video option: {video_id}  audio option: {audio_id}')
            # else:
            #     pass

            # directories = ["storage"]
            # for directory in directories:
            #     if not os.path.isdir(rf'{os.getcwd()}\{directory}'):
            #         print(rf'storage 디렉토리 생성 중...')
            #         os.makedirs(rf'{directory}')

            # 2023년 12월 12일 (화) 16:02:06
            # 다운로드의 최고 품질이 아닐 수 있다. 그래도
            # 차선책으로 두는 것이 낫겠다
            # cmd = rf'{StateManagementUtil.YT_DLP_CMD} -f best "{url}"'

            # cmd = rf'{StateManagementUtil.YT_DLP_CMD} -f {video_id}+{audio_id} {url}' # 초기에 만든 선택적인 방식
            # cmd = rf'{StateManagementUtil.YT_DLP_CMD} -f "best[ext=webm]" {url}' # 마음에 안드는 결과
            cmd = rf'{StateManagementUtil.YT_DLP_CMD} -f "bestvideo[ext=webm]+bestaudio[ext=webm]" {url}'  # 지금 가장 마음에 드는 방법
            # cmd = rf'{StateManagementUtil.YT_DLP_CMD} -f "bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]/best" {url}' # 아직 시도하지 않은 방법
            if video_id == "" or audio_id == "" == 1:
                # text = "다운로드를 진행할 수 없습니다\n다운로드용 video_id 와 audio_id를 설정 후\nurl을 다시 붙여넣어 다운로드를 다시 시도하세요\n{url}"
                print("불완전한 다운로드 명령어가 감지되었습니다....")
                TextToSpeechUtil.speak_ments(ment="불완전한 다운로드 명령어가 감지되었습니다", sleep_after_play=0.65)
                DebuggingUtil.print_ment_magenta(ment=f"에러코드[E004]\n아래의 비디오 아이디를 저장하고 에러코드를 관리자에게 문의해주세요\nvideo id: {url}")

                print(cmd)
                break

            try:
                lines = FileSystemUtil.get_cmd_output(cmd=cmd)
            except:
                print(cmd)

            # storage = rf'{os.path.dirname(StateManagementUtil.PROJECT_DIRECTORY)}\storage'
            storage = rf"D:\[noe] [8TB] [ext]\`"

            if not os.path.exists(storage):
                os.makedirs(storage)

            print("다운로드 파일 이동 시도 중...")
            file = ""
            try:
                clip_id = BusinessLogicUtil.parse_youtube_video_id(url)
                if clip_id == None:
                    clip_id = url

                lines = os.listdir()
                for line in lines:
                    if BusinessLogicUtil.is_regex_in_contents(str(line), str(clip_id)):
                        file = line

                src = os.path.abspath(file)
                src_renamed = rf"{storage}\{os.path.basename(file)}"

                DebuggingUtil.print_ment_magenta(f'src_renamed : {src_renamed}')
                if src == os.getcwd():  # 여기 또 os.getcwd() 있는 부분 수정하자..
                    # E001 : 실행불가능한 명령어입력 감지
                    # S001 : 다운로드 가능한 video_id 와 audio_id 를 가용목록에 추가해주세요.
                    DebuggingUtil.print_ment_magenta(ment=f"에러코드[E001]\n아래의 비디오 아이디를 저장하고 에러코드를 관리자에게 문의해주세요\nvideo id: {url}")

                    DebuggingUtil.print_ment_magenta("cmd")
                    DebuggingUtil.print_ment_magenta(cmd)
                    break
                # shutil.move(src, storage)
                if src != os.getcwd():  # 여기 또 os.getcwd() 있는 부분 수정하자..
                    FileSystemUtil.move_target_without_overwrite(src, src_renamed)

            except:
                DebuggingUtil.trouble_shoot("202312030009x")
            print(rf'다운로드 결과 확인 중...')
            try:
                src_moved = rf'{storage}\{file}'

                # 4 줄 주석처리
                # DebuggingUtil.print_ment_magenta()(ment="다운로드된 영상을 재생할까요?", btns=["재생하기", "재생하지 않기"], auto_click_negative_btn_after_seconds=3)
                #
                # if dialog.btn_text_clicked == "재생하기":
                #     FileSystemUtil.explorer(target_abspath=src_moved)

                # DebuggingUtil.print_ment_magenta( ment=f"다운로드가 성공되었습니다\n{src_moved}", auto_click_positive_btn_after_seconds=2) # 성공 뜨는게 귀찮아서 주석처리함,mkrmkrmkrmkrmkr

            except Exception:
                DebuggingUtil.trouble_shoot("202312030013")

            # 다운로드 로깅 처리
            # cmd = f'echo "{url}" >> success_yt_dlp.log'
            # FileSystemUtil.get_cmd_output(cmd=cmd)
            break

    @staticmethod
    def download_clip_alt(url: str):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        while True:
            if url.strip() == "":
                DebuggingUtil.print_ment_magenta(rf"다운로드할 url이 아닙니다 {url}")
                break

            print('다운로드 옵션 파싱 중...')
            video_id = ''
            cmd = rf'{StateManagementUtil.YT_DLP_CMD} -F {url}'
            lines = FileSystemUtil.get_cmd_output(cmd=cmd)
            video_ids_allowed = [
                '315',
                '313',
                '303',
                '302',
                '308',
                '616',
                '248',
                '247',
                '244',
                '137',
                '136',
            ]
            audio_ids_allowed = [
                '250',
                '251',
            ]
            audio_id = ""
            for line in lines:
                if 'video only' in line or 'audio only' in line:
                    DebuggingUtil.print_ment_magenta(line)
                    # video_id 설정
                    for id in video_ids_allowed:
                        if id in line:
                            video_id = id
                            if video_id.strip() == "":
                                DebuggingUtil.print_ment_magenta(rf"다운로드 할 수 있는 video_id가 아닙니다 {video_id.strip()}")
                                break
                    # audio_id 설정
                    for id in audio_ids_allowed:
                        if id in line:
                            audio_id = id
                            if audio_id.strip() == "":
                                DebuggingUtil.print_ment_magenta(rf"다운로드 할 수 있는 audio_id가 아닙니다 {audio_id.strip()}")
                                break
            cmd = rf'{StateManagementUtil.YT_DLP_CMD} -f {video_id}+{audio_id} {url}'  # 초기에 만든 선택적인 방식
            if video_id == "" or audio_id == "" == 1:
                print("불완전한 다운로드 명령어가 감지되었습니다....")
                TextToSpeechUtil.speak_ments(ment="불완전한 다운로드 명령어가 감지되었습니다", sleep_after_play=0.65)
                DebuggingUtil.print_ment_magenta(ment=f"에러코드[E000]\n불완전한 다운로드 명령어가 감지되었습니다. 에러코드를 관리자에게 문의해주세요")
                DebuggingUtil.print_ment_magenta(cmd)
                break

            print(rf'명령어 실행 중...')
            FileSystemUtil.get_cmd_output(cmd=cmd)

            print(rf'storage 생성 중...')
            storage = rf'{os.path.dirname(StateManagementUtil.PROJECT_DIRECTORY)}\storage'

            if not os.path.exists(storage):
                os.makedirs(storage)

            print("다운로드 파일 이동 시도 중...")
            file = ""
            try:
                clip_id = BusinessLogicUtil.parse_youtube_video_id(url)
                if clip_id == None:
                    clip_id = url

                lines = os.listdir()
                for line in lines:
                    if BusinessLogicUtil.is_regex_in_contents(str(line), str(clip_id)):
                        file = line

                src = os.path.abspath(file)
                src_renamed = rf"{storage}\{os.path.basename(file)}"
                DebuggingUtil.print_ment_magenta(f'src : {src}')
                DebuggingUtil.print_ment_magenta(f'src_renamed : {src_renamed}')
                if src == os.getcwd():  # 여기 또 os.getcwd() 있는 부분 수정하자..
                    print("실행불가능한 명령어가 실행되어 다운로드 할 수 없었습니다")
                    TextToSpeechUtil.speak_ments(ment="실행불가능한 명령어가 실행되어 다운로드 할 수 없었습니다", sleep_after_play=0.65)
                    DebuggingUtil.print_ment_magenta(ment=f"에러코드[E003]\n아래의 비디오 아이디를 저장하고 에러코드를 관리자에게 문의해주세요\nvideo id: {url}")

                    DebuggingUtil.print_ment_magenta(f"{StateManagementUtil.LINE_LENGTH_PROMISED}다운로드 가능한 video_id 와 audio_id 를 가용목록에 추가해주세요")
                    DebuggingUtil.print_ment_magenta(cmd)
                    break

                if src != os.getcwd():  # 여기 또 os.getcwd() 있는 부분 수정하자..
                    FileSystemUtil.move_target_without_overwrite(src, src_renamed)

            except:
                DebuggingUtil.trouble_shoot("202312030009")

            print(rf'다운로드 결과 확인 중...')
            try:
                src_moved = rf'{storage}\{file}'
                DebuggingUtil.print_ment_magenta(ment=f"{src_moved} 가 다운로드 되었습니다")
                # 다운로드된 영상을 재생할까요?
                # Park4139Park4139.Tts.speak(ment = "다운로드된 영상을 재생합니다", sleep_after_play=0.65)
                # cmd = rf'explorer "{src_moved}"'
                # FileSystemUtil.get_cmd_output(cmd=cmd)
            except Exception:
                DebuggingUtil.trouble_shoot("202312030013")

            print(rf'다운로드 결과 로깅 중...')
            cmd = f'echo "{url}" >> success_yt_dlp.log'
            FileSystemUtil.get_cmd_output(cmd=cmd)
            break

    @staticmethod
    def download_from_youtube_to_webm(urls):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        while True:
            urls = str(urls).strip()
            if urls == None:
                TextToSpeechUtil.speak_ments(ment="다운로드할 대상 목록에 아무것도 입력되지 않았습니다", sleep_after_play=0.65)
                break
            if urls == "None":
                TextToSpeechUtil.speak_ments(ment="다운로드할 대상 목록에 이상한 것이 입력되었습니다", sleep_after_play=0.65)
                break

            if "\n" in urls:
                urls = urls.split("\n")
            else:
                urls = [urls]

            urls = [x for x in urls if x.strip("\n")]  # 리스트 요소 "" 제거,  from ["", A] to [A]       [""] to []
            DebuggingUtil.print_ment_magenta(ment=f"{len(urls)} 개의 url이 입력되었습니다")

            try:
                urls.append(sys.argv[1])
            except IndexError:
                pass
            except Exception:
                DebuggingUtil.trouble_shoot("202312071455")
                pass

            # urls = list(set(urls)) # urls 중복제거(orderless way)    # remove duplicated elements of list ( orderless way ) # 파이썬 3.7 부터는 ordered 라는 것 같은데 명시적인 방법이 아닌것 같다..

            # urls 중복제거(ordered way) # remove duplicated elements of list ( ordered way )
            urls_removed_duplicated_element: [str] = []
            for url in urls:
                if url not in urls_removed_duplicated_element:
                    if url is not None:
                        # if url is not "None":
                        urls_removed_duplicated_element.append(url)
            urls = urls_removed_duplicated_element
            DebuggingUtil.print_ment_magenta(f"len(urls) : {len(urls)}")
            for i in urls:
                DebuggingUtil.print_ment_magenta(i)

            # DebuggingUtil.commentize('다운로드 할게 없으면 LOOP break')
            if len(urls) == 0:
                DebuggingUtil.print_ment_magenta(ment=f"다운로드할 대상이 없습니다")
                # TtsUtil.speak_ments(ment="다운로드할 대상이 없습니다", sleep_after_play=0.65)
                break
            if len(urls) != 1:
                TextToSpeechUtil.speak_ments(f"{str(len(urls))}개의 다운로드 대상이 확인되었습니다", sleep_after_play=0.65)
            for url in urls:
                url = url.strip()  # url에 공백이 있어도 다운로드 가능하도록 설정
                if '&list=' in url:
                    DebuggingUtil.commentize(' clips mode')
                    clips = Playlist(url)  # 이걸로도 parsing 기능 수행 생각 중
                    DebuggingUtil.print_ment_magenta(f"predicted clips cnt : {len(clips.video_urls)}")
                    TextToSpeechUtil.speak_ments(ment=f"{len(clips.video_urls)}개의 다운로드 목록이 확인되었습니다", sleep_after_play=0.65)
                    # os.system(f'echo "여기서부터 비디오 리스트 시작 {url}" >> success_yt_dlp.log')
                    for clip in clips.video_urls:
                        try:
                            BusinessLogicUtil.download_clip(clip)
                        except Exception:
                            DebuggingUtil.trouble_shoot("%%%FOO%%%")
                            continue
                    # os.system(f'echo "여기서부터 비디오 리스트 종료 {url}" >> success_yt_dlp.log')
                else:
                    if BusinessLogicUtil.parse_youtube_video_id(url) != None:
                        DebuggingUtil.commentize('{StateManagementUtil.LINE_LENGTH_PROMISED}__________ youtube video id parsing mode')
                        try:
                            BusinessLogicUtil.download_clip(f'https://www.youtube.com/watch?v={BusinessLogicUtil.parse_youtube_video_id(url)}')
                        except Exception:
                            DebuggingUtil.trouble_shoot("%%%FOO%%%")
                            continue
                    else:
                        DebuggingUtil.commentize('{StateManagementUtil.LINE_LENGTH_PROMISED}__________ experimental mode')
                        print("???????????????????")
                        try:
                            url_parts_useless = [
                                "https://youtu.be/",
                                "https://www.youtube.com/shorts/",
                            ]
                            try:
                                for index, useless_str in enumerate(url_parts_useless):
                                    if useless_str in url:
                                        print(rf'url.split(useless_str)[1] : {url.split(useless_str)[1]}')
                                        BusinessLogicUtil.download_clip(url=url.split(useless_str)[1])
                            except Exception:
                                BusinessLogicUtil.download_clip(url)
                                DebuggingUtil.trouble_shoot("%%%FOO%%%")
                        except Exception:
                            DebuggingUtil.trouble_shoot("%%%FOO%%%")
                        continue
            break

    # deprecated method by Park4139
    # def print_police_line(police_line_ment):

    #     police_line = ''
    #     for i in range(0, 255 // len(police_line_ment)):
    #         police_line = police_line + f'{police_line_ment} '
    #     Park4139.debug_as_cli(f'{police_line.upper()}')
    @staticmethod
    def is_regex_in_contents(target, regex):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        pattern = re.compile(regex)
        m = pattern.search(target)
        if m:
            # DebuggingUtil.commentize("function name   here here here")
            # Park4139.debug_as_cli(rf"contents: {contents}")
            # Park4139.debug_as_cli(rf"regex: {regex}")
            # Park4139.debug_as_cli(rf"True")
            return True
        else:
            # Park4139.debug_as_cli(rf"contents: {contents}")
            # Park4139.debug_as_cli(rf"regex: {regex}")
            # Park4139.debug_as_cli(rf"False")
            return False

    @staticmethod
    def is_regex_in_contents_with_case_ignored(contents, regex):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        pattern = re.compile(regex, re.IGNORECASE)
        m = pattern.search(contents)
        if m:
            return True
        else:
            return False

    @staticmethod
    def toogle_console_color(color_bg, colors_texts):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        to_right_nbsp = ''
        to_right_nbsp_cnt = 150
        for i in range(0, to_right_nbsp_cnt):
            to_right_nbsp = to_right_nbsp + ' '
        for color_text in colors_texts:
            if color_bg != color_text:
                os.system(f"color {color_bg}{color_text}")

    @staticmethod
    def make_matrix_console():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        os.system('color 0A')
        os.system('color 02')
        while True:
            lines = subprocess.check_output('dir /b /s /o /a-d', shell=True).decode('utf-8').split("\n")
            for line in lines:
                if "" != line:
                    if os.getcwd() != line:
                        DebuggingUtil.print_ment_magenta(lines)
            time.sleep(60)

    @staticmethod
    def make_party_console():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        commands = [
            'color 03',
            'color 09',
            'color 4F',
            'color cF',
            'color bf',
            'color 10',
            'color 1f',
            'color 08',
            'color f0',
            'color f8',
            'color 4c',
            'color c4',
            'color 09',
            'color 0a',
            'color d4',
            'color a4',
            'color 4a',
            'color 51',
            'color 48',
            'color 4c',
            'color 5d',
            'color 3b',
            'color e6',
            'color 07',
            'color 3F',
            'color 13',
            'color a2',
            'color 2a',
            'color 01',
            'color 02',
            'color 03',
            'color 04',
            'color 05',
            'color 06',
            'color 8f',
            'color 9b',
            'color 4a',
            'color da',
            'color ad',
            'color a4',
            'color b2',
            'color 0c',
            'color 0d',
            'color e3',
            'color eb',
            'color e7',
            'color 0f',
        ]
        while (True):
            for command in commands:
                os.system(f'{command}')
                # os.system('echo "202312031429" && pause')

    @staticmethod
    # 이 메소드를 만들면서 권한을 얻는 여러가지 방법을 stack over flow 를 따라 시도해보았으나 적다한 해결책을 찾지 못함. pyautogui 로 시도 방법은 남아있으나
    # 일단은 regacy 한 방법으로 임시로 해결해두었다.
    def update_global_pkg_park4139():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        local_pkg = rf"{StateManagementUtil.PROJECT_DIRECTORY}\pkg_park4139"
        global_pkg = rf"C:\Python312\Lib\site-packages\pkg_park4139"
        updateignore_txt = rf"{StateManagementUtil.PROJECT_DIRECTORY}\pkg_park4139\updateignore.txt"
        try:
            if os.path.exists(global_pkg):
                # 삭제시도
                # shutil.rmtree(global_pkg)

                # 삭제시도
                # for file in os.scandir(global_pkg):
                # os.remove(file.path)

                # 덮어쓰기
                # src= local_pkg
                # dst =os.path.dirname(global_pkg)
                # os.system(f"echo y | copy {src} {dst}")
                # shutil.copytree(local_pkg, os.path.dirname(global_pkg))
                cmd = f'echo y | xcopy "{local_pkg}" "{global_pkg}" /k /e /h /exclude:{updateignore_txt} >nul'
                os.system(cmd)

                # 디버깅
                # Park4139TestUtil.pause()
                DebuggingUtil.print_ment_magenta(f'{cmd}')
                DebuggingUtil.print_ment_magenta(f"{StateManagementUtil.LINE_LENGTH_PROMISED}")
                return "REPLACED global pkg_Park4139 AS local_pkg"
            else:
                return "pkg_Park4139 NOT FOUND AT GLOBAL LOCATION"

        except Exception as e:
            DebuggingUtil.trouble_shoot("202312030016")

    @staticmethod
    def merge_video_and_sound(file_v_abspath, file_a_abspath):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        DebuggingUtil.commentize('다운로드 디렉토리 생성')
        directories = ["storage"]
        for directory in directories:
            if not os.path.isdir(rf'./{directory}'):
                os.makedirs(rf'{directory}')

        DebuggingUtil.commentize(rf'yotube 에서 고해상도 음성 없는 영상과 음성을 받아 하나의 영상으로 merge')
        DebuggingUtil.commentize('비디오 파일, 음성 파일 절대주소 get')
        dst = rf'{StateManagementUtil.PROJECT_DIRECTORY}\storage'
        paths = [os.path.abspath(dst), os.path.basename(file_v_abspath)]
        file_va = os.path.join(*paths)
        DebuggingUtil.print_ment_magenta(rf'file_v_abspath : {file_v_abspath}')
        DebuggingUtil.print_ment_magenta(rf'file_a_abspath : {file_a_abspath}')
        DebuggingUtil.print_ment_magenta(rf'file_va : {file_va}')

        DebuggingUtil.commentize('ffmpeg.exe 위치 설정')
        location_ffmpeg = rf"{StateManagementUtil.USERPROFILE}\Desktop\`workspace\tool\LosslessCut-win-x64\resources\ffmpeg.exe"
        trouble_characters = ['Ä']
        trouble_characters_alternatives = {'Ä': 'A'}
        for trouble_character in trouble_characters:
            file_v_abspath = file_v_abspath.replace(trouble_character, trouble_characters_alternatives[trouble_character])
            file_a_abspath = file_a_abspath.replace(trouble_character, trouble_characters_alternatives[trouble_character])
            file_va = file_va.replace(trouble_character, trouble_characters_alternatives[trouble_character])
            DebuggingUtil.commentize('파일명 변경 시도')
            try:
                if trouble_character in file_va:
                    os.rename(file_v_abspath,
                              file_v_abspath.replace(trouble_character, trouble_characters_alternatives[trouble_character]))
                    os.rename(file_a_abspath,
                              file_a_abspath.replace(trouble_character, trouble_characters_alternatives[trouble_character]))
            except Exception as e:
                DebuggingUtil.trouble_shoot("202312030017")

        DebuggingUtil.commentize(' 파일머지 시도')
        try:
            DebuggingUtil.print_ment_magenta(rf'echo y | "{location_ffmpeg}" -i "{file_v_abspath}" -i "{file_a_abspath}" -c copy "{file_va}"')
            lines = subprocess.check_output(
                rf'echo y | "{location_ffmpeg}" -i "{file_v_abspath}" -i "{file_a_abspath}" -c copy "{file_va}"', shell=True).decode(
                'utf-8').split("\n")
            for line in lines:
                DebuggingUtil.print_ment_magenta(line)
        except Exception as e:
            DebuggingUtil.trouble_shoot("202312030018")

        DebuggingUtil.print_ment_magenta(rf'다운로드 및 merge 결과 확인 시도')
        try:
            DebuggingUtil.print_ment_magenta(rf'explorer "{file_va}"')
            subprocess.check_output(rf'explorer "{file_va}"', shell=True).decode('utf-8').split("\n")
        except Exception as e:
            DebuggingUtil.trouble_shoot("202312030019a")

        DebuggingUtil.commentize(' 불필요 리소스 삭제 시도')
        try:
            if os.path.exists(file_va):
                subprocess.check_output(rf'echo y | del /f "{file_v_abspath}"', shell=True).decode('utf-8').split("\n")
                lines = subprocess.check_output(rf'echo y | del /f "{file_a_abspath}"', shell=True).decode('utf-8').split("\n")
                for line in lines:
                    DebuggingUtil.print_ment_magenta(line)
        except Exception as e:
            DebuggingUtil.trouble_shoot("202312030020")

    # @staticmethod
    # def elapsed(function):

    #     def wrapper(*args, **kwargs):

    #         import time
    #         time_s = time.time()
    #         function(*args, **kwargs)
    #         time_e = time.time()
    #         mesured_time = time_e - time_s
    #         Park4139.debug_as_cli(f'측정시간은 {mesured_time} 입니다')
    #         DebuggingUtil.commentize(f'측정시간은 {mesured_time} 입니다')
    #     return wrapper

    @staticmethod
    def cls():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        import os
        os.system('cls')

    @staticmethod
    def replace_with_auto_no(contents: str, unique_word: str, auto_cnt_starting_no=0):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        """

        input   = "-----1-----1----1------"
        Output  = "-----1-----2----3------"

        input
        --------
        -----1--
        ---1----
        ---1----
        --------
         ouput
        --------
        -----1--
        ---2----
        ---3----
        --------

        """
        tmp = []
        for index, element in enumerate(contents.split(unique_word)):
            if index != len(contents.split(unique_word)) - 1:
                tmp.append(element + str(auto_cnt_starting_no))
                auto_cnt_starting_no = auto_cnt_starting_no + 1
            else:
                tmp.append(element)
        lines_new_as_str = "".join(tmp)
        return lines_new_as_str

    @staticmethod
    def replace_with_auto_no_orderless(contents: str, unique_word: str, auto_cnt_starting_no=0):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        # DebuggingUtil.commentize("항상 필요했던 부분인데 만들었다. 편하게 개발하자. //웹 서비스 형태로 아무때서나 접근이되면 더 좋을 것 같다.  웹 개발툴 을 만들어 보자")
        before = unique_word
        after = 0 + auto_cnt_starting_no
        contents_new = []
        # lines = contents.split("\n")
        lines = contents.strip().split("\n")  # 문제 없긴 했는데,  어떻게 되나 실험해보자 안되면 위의 코드로 주석 스와핑할것.
        for line in lines:
            # Park4139.debug_as_cli(line)
            # Park4139.debug_as_cli(before)
            # Park4139.debug_as_cli(str(after))
            after = after + 1

            line_new = re.sub(str(before), str(after), str(line))
            # Park4139.debug_as_cli(line_new)
            contents_new.append(line_new)

        # DebuggingUtil.commentize("str list to str")
        delimiter = "\n"
        contents_new_as_str = delimiter.join(contents_new)
        return contents_new_as_str

    # @staticmethod
    # def move_with_overwrite(src: str, dst: str):
    #     DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
    #     try:
    #         # 목적지에 있는 중복타겟 삭제
    #         os.remove(dst)
    #     except FileNotFoundError as e:
    #         pass
    #     except Exception:
    #         DebuggingUtil.trouble_shoot("%%%FOO%%%")
    #     try:
    #         # 목적지로 타겟 이동
    #         os.rename(src, dst)
    #     except Exception:
    #         DebuggingUtil.trouble_shoot("%%%FOO%%%")

    @staticmethod
    def raise_error(str: str):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        raise shutil.Error(str)

    @staticmethod
    def git_push_by_auto():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        GIT_HUB_ADDRESS = StateManagementUtil.GIT_HUB_ADDRESS
        GIT_HUB_REPOSITORY_URL = rf"{GIT_HUB_ADDRESS}/archive_py"
        while True:
            try:
                lines = FileSystemUtil.get_cmd_output(cmd='git add * ')
                if lines == subprocess.CalledProcessError:
                    DebuggingUtil.print_ment_magenta(ment="혹시 여기 발생됩니까? 안되길 바랍니다. - 2023 01 28 -")
                    break
                if "" in lines:
                    DebuggingUtil.print_ment_success(f"add success")
                    commit_ment = f"refer to README.md ( pushed at {BusinessLogicUtil.get_time_as_('%Y-%m-%d %H:%M:%S')}"
                    lines = FileSystemUtil.get_cmd_output(cmd=rf'git commit -m "{commit_ment}"')
                    lines = FileSystemUtil.get_cmd_output(cmd='git status | findstr "nothing to commit, working tree clean"')
                    if "nothing to commit, working tree clean" in lines:
                        DebuggingUtil.print_ment_success(f"commit success")
                        lines = FileSystemUtil.get_cmd_output(cmd='git push -u origin main')
                        if "Everything up-to-date" or "branch 'main' set up to track 'origin/main'." in lines:
                            # os.system('color df')  # OPERATION
                            DebuggingUtil.print_ment_success(f"push success")
                            if int('08') <= int(BusinessLogicUtil.get_time_as_('%H')) <= int('23'):  # 자는데 하도 시끄러워서 추가한 코드
                                # TextToSpeechUtil.speak_ments("깃허브에 프로젝트 푸쉬를 성공했습니다", sleep_after_play=0.65)
                                DebuggingUtil.print_ment_magenta(ment="깃허브에 프로젝트 푸쉬를 성공했습니다")
                                break
                            break
                        else:
                            DebuggingUtil.print_ment_fail(f"push fail")
                    else:
                        DebuggingUtil.print_ment_fail(f"commit fail")
                else:
                    DebuggingUtil.print_ment_fail(f"add fail")
            except:
                DebuggingUtil.print_ment_magenta(ment="깃허브에 프로젝트 푸쉬를 시도 중 에러가 발생하였습니다'")
                break

    @staticmethod
    def save_all_list():  # 수정 필요, 모든 파일 디렉토리 말고, 특정디렉토리로 수정한는 것도 할것
        """모든 파일 디렉토리에 대한 정보를 텍스트 파일로 저장하는 함수"""
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        # os.system('chcp 65001 >nul')
        os.system('export LANG=en_US.UTF-8 >nul')
        opening_directory = os.getcwd()
        proper_tree_txt = rf"{StateManagementUtil.PROJECT_DIRECTORY}\$cache_all_tree\proper_tree.txt"
        all_tree_txt = rf"{StateManagementUtil.PROJECT_DIRECTORY}\$cache_all_tree\all_tree.txt"
        if not os.path.exists(os.path.dirname(all_tree_txt)):
            os.makedirs(os.path.dirname(all_tree_txt))
            # os.system(f'echo. >> "{all_tree_txt}"')
            os.system(f'echo. >> "{all_tree_txt}" >nul')
            os.system(f'echo. >> "{proper_tree_txt}" >nul')
        with open(all_tree_txt, 'w', encoding="utf-8") as f:
            f.write(" ")
        with open(proper_tree_txt, 'w', encoding="utf-8") as f:
            f.write(" ")

        drives = "foo"

        file_cnt = 0
        f = open(StateManagementUtil.PROJECT_DIRECTORY + '\\all_list.txt', 'a', encoding="utf-8")  # >>  a    > w   각각 대응됨.
        for drive in drives:
            os.chdir(drive)
            for dirpath, subdirs, files in os.walk(os.getcwd()):  # 여기 또 os.getcwd() 있는 부분 수정하자..
                for file in files:
                    file_cnt = file_cnt + 1
                    f.write(str(file_cnt) + " " + os.path.join(dirpath, file) + "\n")
        f.close()  # close() 를 사용하지 않으려면 with 문을 사용하는 방법도 있다.
        DebuggingUtil.print_ment_magenta(f"{StateManagementUtil.LINE_LENGTH_PROMISED}{StateManagementUtil.LINE_LENGTH_PROMISED} all_list.txt writing e")
        DebuggingUtil.print_ment_magenta(f"{StateManagementUtil.LINE_LENGTH_PROMISED}{StateManagementUtil.LINE_LENGTH_PROMISED} all_list_proper.txt rewriting s")
        texts_black = [
            "C:\\$WinREAgent",
            "C:\\mingw64",
            "C:\\PerfLogs",
            "C:\\Program Files (x86)",
            "C:\\Program Files",
            "C:\\ProgramData",
            "C:\\Temp",
            "C:\\Users\\All Users",
            "C:\\Windows\\servicing",
            "C:\\Windows\\SystemResources",
            "C:\\Windows\\WinSxS",
            "C:\\Users\\Default",
            "C:\\Users\\Public",
            "C:\\Windows.old",
            "C:\\Windows",
            "C:\\$Recycle.Bin",
            "D:\\$RECYCLE.BIN",
            "E:\\$RECYCLE.BIN",
            "E:\\$Recycle.Bin",
            "F:\\$RECYCLE.BIN",
            rf"{StateManagementUtil.USERPROFILE}\\AppData",
        ]
        texts_white = [
            ".mkv",
        ]
        f = open(rf'{StateManagementUtil.PROJECT_DIRECTORY}\all_list.txt', 'r+', encoding="utf-8")
        f2 = open(rf'{StateManagementUtil.PROJECT_DIRECTORY}\all_list_proper.txt', 'a', encoding="utf-8")
        lines_cnt = 0
        while True:
            line = f.readline()
            if not line:
                break
            lines_cnt = lines_cnt + 1
            if any(text_black not in line for text_black in texts_black):
                # Park4139.debug_as_cli(line)
                if any(text_white in line for text_white in texts_white):
                    # Park4139.debug_as_cli(line.split("\n")[0] + " o")
                    f2.write(line.split("\n")[0] + " o " + "\n")
                    # Park4139.debug_as_cli('o')
                    pass
                else:
                    # Park4139.debug_as_cli(line.split("\n")[0] + " x")
                    # f2.write(line.split("\n")[0] + " x "+"\n")
                    # Park4139.debug_as_cli('x')
                    pass
        f.close()
        f2.close()
        DebuggingUtil.print_ment_magenta(f"{StateManagementUtil.LINE_LENGTH_PROMISED}{StateManagementUtil.LINE_LENGTH_PROMISED} all_list_proper.txt rewriting e")

        DebuggingUtil.print_ment_magenta(f"{StateManagementUtil.LINE_LENGTH_PROMISED}{StateManagementUtil.LINE_LENGTH_PROMISED} files opening s")
        os.chdir(os.getcwd())
        os.system('export LANG=en_US.UTF-8 >nul')

        # os.system("type all_list.txt")
        # os.system("explorer all_list.txt")
        os.system("explorer all_list_proper.txt")
        DebuggingUtil.print_ment_magenta(f"{StateManagementUtil.LINE_LENGTH_PROMISED}{StateManagementUtil.LINE_LENGTH_PROMISED} files opening e")

        # os.system('del "'+os.getcwd()+'\\all_list.txt"')
        # mk("all_list.txt")
        DebuggingUtil.print_ment_magenta(f"{StateManagementUtil.LINE_LENGTH_PROMISED}{StateManagementUtil.LINE_LENGTH_PROMISED} e")

    @staticmethod
    def get_line_cnt_of_file(target_abspath: str):
        try:
            DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
            line_cnt = 0
            # 파일 변경 감지 이슈: linecache 모듈은 파일의 변경을 감지하지 못합니다.
            # 파일이 변경되었을 때에도 이전에 캐시된 내용을 반환하여 오래된 정보를 사용할 수 있습니다.
            # 실시간으로 파일의 변경을 감지해야 하는 경우에는 정확한 결과를 얻기 어려울 수 있습니다.
            # line_cnt = len(linecache.getlines(target_abspath))
            # Park4139.debug_as_cli(f'line_cnt:{line_cnt}')  캐시된 내용을 반환하기 때문에. 실시간 정보가 아니다

            # 이 코드는 실시간으로 파일의 변경을 감지 처리 되도록 수정, 단, 파일이 크면 성능저하 이슈 있을 수 있다.
            with open(target_abspath, 'r', encoding="UTF-8") as file:
                # whole_contents = file.readlines()
                # Park4139.debug_as_cli(whole_contents)
                # line_cnt = len(whole_contents)
                # line_cnt = list(en umerate(file))[-1][0] + 1
                line_cnt = file.read().count("\n") + 1
            return line_cnt
        except FileNotFoundError:
            DebuggingUtil.print_ment_magenta("파일을 찾을 수 없었습니다")
            pass
        except Exception:
            DebuggingUtil.trouble_shoot("%%%FOO%%%")

    @staticmethod
    def back_up_by_manual(target_abspath):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        starting_directory = os.getcwd()
        try:
            target_dirname = os.path.dirname(target_abspath)
            target_dirname_dirname = os.path.dirname(target_dirname)
            target_basename = os.path.basename(target_abspath).split(".")[0]
            target_zip = rf'$zip_{target_basename}.zip'
            target_yyyy_mm_dd_HH_MM_SS_zip = rf'{target_basename} - {BusinessLogicUtil.get_time_as_("%Y %m %d %H %M %S")}.zip'
            # DebuggingUtil.commentize(rf'# target_dirname_dirname 로 이동')
            os.chdir(target_dirname_dirname)
            # DebuggingUtil.commentize(rf'부모디렉토리로 빽업')
            cmd = f'bandizip.exe c "{target_zip}" "{target_abspath}"'
            FileSystemUtil.get_cmd_output(cmd)
            # DebuggingUtil.commentize(rf'이름변경')
            cmd = f'ren "{target_zip}" "{target_yyyy_mm_dd_HH_MM_SS_zip}"'
            FileSystemUtil.get_cmd_output(cmd)
            # DebuggingUtil.commentize(rf'부모디렉토리에서 빽업될 디렉토리로 이동')
            cmd = f'move "{target_yyyy_mm_dd_HH_MM_SS_zip}" "{target_dirname}"'
            FileSystemUtil.get_cmd_output(cmd)
            # DebuggingUtil.commentize(rf'빽업될 디렉토리로 이동')
            # os.chdir(target_dirname)
            os.chdir(starting_directory)
            # DebuggingUtil.commentize("os.getcwd()")
            # Park4139.debug_as_cli(os.getcwd())

        except:
            DebuggingUtil.trouble_shoot("202312030000d")
        finally:
            DebuggingUtil.commentize(rf'프로젝트 디렉토리로 이동')
            os.chdir(starting_directory)

    @staticmethod  # move_target_recycle_bin()
    def empty_recycle_bin():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        DebuggingUtil.commentize("휴지통 을 비우는 중...")
        FileSystemUtil.get_cmd_output('PowerShell.exe -NoProfile -Command Clear-RecycleBin -Confirm:$false')
        # 휴지통 삭제 (외장하드까지)
        # for %%a in (cdefghijk L mnopqrstuvwxyz) do (
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        # 존재하는 경우 %%a:\$RECYCLE.BIN for /f "tokens=* usebackq" %%b in (`"dir /a:d/b %%a:\$RECYCLE.BIN\"`) do rd / q/s "%%a:\$RECYCLE.BIN\%%~b"
        # 존재하는 경우 %%a:\RECYCLER for /f "tokens=* usebackq" %%b in (`"dir /a:d/b %%a:\RECYCLER\"`) do rd /q/s "%% a:\RECYCLER\%%~b"
        # )
        TextToSpeechUtil.speak_ments(f'휴지통을 비웠습니다', sleep_after_play=0.65, thread_join_mode=True)

        # 가끔 휴지통을 열어볼까요?
        # DebuggingUtil.commentize("숨김 휴지통 열기")
        # cmd = 'explorer c:\$RECYCLE.BIN'
        # Park4139.get_cmd_output(cmd=cmd)
        # 외장하드 숨김 휴지통 을 보여드릴까요
        # explorer c:\$RECYCLE.BIN
        # explorer d:\$RECYCLE.BIN
        # explorer e:\$RECYCLE.BIN
        # explorer f:\$RECYCLE.BIN

    @staticmethod
    def debug(context: str, is_app_instance_mode=False, input_text_default="", auto_click_positive_btn_after_seconds=3):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        """
        이 함수는 특별한 사용요구사항이 있습니다
        pyside6 앱 내에서 해당 함수를 호출할때는 is_app_instance_mode 를 파라미터에 넣지 않고 쓰는 것을 default 로 디자인했습니다.
        pyside6 앱 밖에서 해당 함수를 호출할때는 is_app_instance_mode 를 True 로 설정하고 쓰십시오.

        사용 요구사항이 생기게 된 이유는 다음과 같습니다
        pyside6 는 app을 singletone으로 instance를 구현합니다. 즉, instance는 반드시 pyside6 app 내에서 하나여야 합니다.
        pyside6의 QApplication()이 앱 내/외에서도 호출이 될 수 있도록 디자인했습니다.
        앱 내에서 호출 시에는 is_app_instance_mode 파라미터를 따로 설정하지 않아도 되도록 디자인되어 있습니다.
        앱 외에서 호출 시에는 is_app_instance_mode 파라미터를 True 로 설정해야 동작하도록 디자인되어 있습니다.
        """
        # app_foo: QApplication = None
        # if is_app_instance_mode == True:
        #     app_foo: QApplication = QApplication()
        # if input_text_default == "":
        #     DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        #     is_input_text_box = False
        # else:
        #     is_input_text_box = True
        # DebuggingUtil.print_ment_magenta()(ment=f"{context}", buttons=["확인"], is_input_box=is_input_text_box, input_box_text_default=input_text_default)
        # DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        #
        # btn_text_clicked = dialog.btn_text_clicked
        # if btn_text_clicked == "":
        #     DebuggingUtil.print_ment_magenta()(f'누르신 버튼은 {btn_text_clicked} 입니다')
        # if is_app_instance_mode == True:
        #     if isinstance(app_foo, QApplication):
        #         app_foo.exec()
        # if is_app_instance_mode == True:
        #     # app_foo.quit()# QApplication 인스턴스 제거시도 : fail
        #     # app_foo.deleteLater()# QApplication 인스턴스 파괴시도 : fail
        #     # del app_foo # QApplication 인스턴스 파괴시도 : fail
        #     # app_foo = None # QApplication 인스턴스 파괴시도 : fail
        #     app_foo.shutdown()  # QApplication 인스턴스 파괴시도 : success  # 성공요인은 app.shutdown()이 호출이 되면서 메모리를 해제까지 수행해주기 때문
        #     # sys.exit()
        # # return app_foo
        DebuggingUtil.print_ment_via_colorama(traceback.print_exc(), colorama_color=ColoramaColorUtil.RED)
        # traceback.print_exc(file=sys.stdout)
        DebuggingUtil.print_ment_magenta(ment=context)

    @staticmethod
    def ask_to_google(question: str):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        while True:
            question_ = question.replace(" ", "+")
            cmd = f'explorer "https://www.google.com/search?q={question_}"  >nul'
            FileSystemUtil.get_cmd_output(cmd)
            break

    @staticmethod
    def connect_remote_rdp1():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        FileSystemUtil.get_cmd_output(cmd=rf"{StateManagementUtil.RDP_82106_BAT}")

    @staticmethod
    def download_from_youtube_to_webm_alt(urls_from_prompt):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        while True:
            urls = []
            urls_from_prompt = str(urls_from_prompt).strip()
            if urls_from_prompt == None:
                TextToSpeechUtil.speak_ments(ment="아무것도 입력되지 않았습니다", sleep_after_play=0.65)
                break
            if urls_from_prompt == "None":
                TextToSpeechUtil.speak_ments(ment="이상한 것이 입력되었습니다", sleep_after_play=0.65)
                break
            try:
                urls_from_prompt_as_list = urls_from_prompt.split("\n")
            except AttributeError:
                traceback.print_exc(file=sys.stdout)
                urls_from_prompt_as_list = urls_from_prompt
            if len(urls_from_prompt_as_list) != 0:
                for i in urls_from_prompt_as_list:
                    if i != "":
                        urls.append(str(i).strip())
            DebuggingUtil.commentize('{StateManagementUtil.LINE_LENGTH_PROMISED}__________ 프롬프트로 입력된 Urls')
            DebuggingUtil.print_ment_magenta(f"len(urls_from_prompt_as_list) : {len(urls_from_prompt_as_list)}")
            DebuggingUtil.print_ment_magenta(urls_from_prompt_as_list)
            for i in urls_from_prompt_as_list:
                DebuggingUtil.print_ment_magenta(i)
            try:
                urls.append(sys.argv[1])
            except IndexError:
                pass
            except Exception:
                DebuggingUtil.trouble_shoot("202312071455")
                pass
            DebuggingUtil.commentize('{StateManagementUtil.LINE_LENGTH_PROMISED}__________ urls 중복제거(ordered way)')
            urls_not_duplicatated_as_ordered = []
            for url in urls:
                if url not in urls_not_duplicatated_as_ordered:
                    if url is not None:
                        urls_not_duplicatated_as_ordered.append(url)
            urls = urls_not_duplicatated_as_ordered
            DebuggingUtil.print_ment_magenta(f"len(urls) : {len(urls)}")
            for i in urls:
                DebuggingUtil.print_ment_magenta(i)

            # DebuggingUtil.commentize('다운로드 할게 없으면 LOOP break')
            if len(urls) == 0:
                DebuggingUtil.print_ment_magenta(f"{StateManagementUtil.LINE_LENGTH_PROMISED}다운로드할 대상이 없습니다")
                TextToSpeechUtil.speak_ments(ment="다운로드할 대상이 없습니다", sleep_after_play=0.65)
                break
            DbTomlUtil.update_db_toml(key="yt_dlp_tried_urls", value=urls)

            if len(urls) != 1:
                TextToSpeechUtil.speak_ments(ment=f"{str(len(urls))}개의 다운로드 대상이 확인되었습니다", sleep_after_play=0.65)
            for url in urls:
                url = url.strip()
                if '&list=' in url:
                    DebuggingUtil.commentize(' clips mode')
                    clips = Playlist(url)  # 이걸로도 parsing 기능 수행할 수 있을 것 같은데
                    DebuggingUtil.print_ment_magenta(f"predicted clips cnt : {len(clips.video_urls)}")
                    os.system(f'echo "여기서부터 비디오 리스트 시작 {url}" >> success_yt_dlp.log')
                    for clip in clips.video_urls:
                        try:
                            BusinessLogicUtil.download_clip_alt(clip)
                        except Exception:
                            DebuggingUtil.trouble_shoot("%%%FOO%%%")
                    os.system(f'echo "여기서부터 비디오 리스트 종료 {url}" >> success_yt_dlp.log')
                else:
                    if BusinessLogicUtil.parse_youtube_video_id(url) != None:
                        DebuggingUtil.commentize('{StateManagementUtil.LINE_LENGTH_PROMISED}__________ youtube video id parsing mode')
                        try:
                            BusinessLogicUtil.download_clip_alt(f'https://www.youtube.com/watch?v={BusinessLogicUtil.parse_youtube_video_id(url)}')
                        except Exception:
                            DebuggingUtil.trouble_shoot("%%%FOO%%%")
                    else:
                        DebuggingUtil.commentize('{StateManagementUtil.LINE_LENGTH_PROMISED}__________ experimental mode')
                        print("???????????????????2")
                        try:
                            url_parts_useless = [
                                "https://youtu.be/",
                                "https://www.youtube.com/shorts/",
                            ]
                            try:
                                for index, useless_str in enumerate(url_parts_useless):
                                    if useless_str in url:
                                        # BusinessLogicUtil.download_clip(url=url.split(useless_str)[1])
                                        BusinessLogicUtil.download_clip_alt(url=url.split(useless_str)[1])
                            except Exception:
                                BusinessLogicUtil.download_clip(url)
                                DebuggingUtil.trouble_shoot("%%%FOO%%%")
                        except Exception:
                            DebuggingUtil.trouble_shoot("%%%FOO%%%")
                        continue

    @staticmethod
    def speak_that_service_is_in_preparing():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        TextToSpeechUtil.speak_ments(ment="아직 준비되지 않은 서비스 입니다", sleep_after_play=0.65)

    @staticmethod
    def is_void_function(func):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        """
            함수가 void 함수인지 아닌지 판단하는 함수입니다.

            Args:
              function: 함수

            Returns:
              함수가 void 함수이면 True, 아니면 False
        """
        function_code = func.__code__
        return function_code.co_argcount == 0 and function_code.co_flags & 0x20 == 0

    @staticmethod
    def get_count_args(func):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        return func.__code__.co_argcount

    @staticmethod
    def get_list_replaced_from_list_that_have_special_characters(target: [str], replacement: str):  # from [str] to [str]
        return [re.sub(pattern=r'[^a-zA-Z0-9가-힣\s]', repl='', string=string) for string in target]

    @staticmethod
    def get_str_replaced_special_characters(target: str, replacement: str):  # str to str
        target_replaced = re.sub(pattern=r'[^a-zA-Z0-9가-힣\s]', repl=replacement, string=target)  # 정규표현식을 사용하여 특수문자(알파벳, 숫자, 한글, 공백을 제외한 모든 문자) 제거
        return target_replaced

    @staticmethod
    def get_process_name_by_pid(pid):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        try:
            data = FileSystemUtil.get_cmd_output(cmd=f'tasklist | findstr "{pid}"')
            return data[0].split(" ")[0]
        except:
            return 0

    @staticmethod
    def move_window_to_front_by_pid(pid):  # deprecated
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        pass

    @staticmethod
    def get_target_pid_by_process_name(target_process_name: str):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        while True:
            pids = FileSystemUtil.get_cmd_output(f"tasklist | findstr {target_process_name}")
            # Park4139.debug_as_gui(f"pids:\n\n{pids}")
            cnts: [int] = []
            for i in pids:
                cnts.append(i.count(" "))  # str 내의 특정문자의 개수를 cnts에 저장
            try:
                max_cnt = max(cnts)
            except ValueError:
                # Park4139.debug_as_cli(traceback.format_exc())
                DebuggingUtil.print_ment_magenta(f"{target_process_name}에 대한 현재 실행중인 pid 가 없는 것 같습니다")
                break
            for i in range(0, max_cnt):  # max(cnts):  pids 요소별 가장 " " 가 많이 든 요소의 개수
                pids: [str] = [i.replace("  ", " ") for i in pids]  # 공백 제거

            pids_ = []
            for i in pids:
                if i.strip() != "\"":
                    if i.strip() != "":
                        # pids_.append(i.split(" "))  # 리스트 요소 내 "" 인 경우 제거, \" 인 경우 제거
                        pids_.append(list(map(str, i.split(" "))))  # 리스트 요소 내 "" 인 경우 제거, \" 인 경우 제거
            pids = pids_

            pid_and_size = {}
            for i in pids:
                pid_and_size[i[1]] = i[4]  # pid 와 size 를 튜플로 나눠 담았는데 이부분 생략하고 처음부터 남아 담아도 되었을 것 같은데

            pids = []
            sizes = []
            for pid, size in pid_and_size.items():
                pids.append(pid)
                sizes.append(size)

            for pid, size in pid_and_size.items():  # 프로세스명이 중복일 때 size 가 큰 프로세스의 pid를 리턴
                if size == max(sizes):
                    DebuggingUtil.print_ment_magenta(f"pid : {pid}")
                    return int(pid)

    @staticmethod
    def print_today_time_info():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        yyyy = BusinessLogicUtil.get_time_as_('%Y')
        MM = BusinessLogicUtil.get_time_as_('%m')
        dd = BusinessLogicUtil.get_time_as_('%d')
        HH = BusinessLogicUtil.get_time_as_('%H')
        mm = BusinessLogicUtil.get_time_as_('%M')
        week_name = BusinessLogicUtil.return_korean_week_name()
        DebuggingUtil.print_ment_magenta(f'현재 시각 {int(yyyy)}년 {int(MM)}월 {int(dd)}일 {week_name}요일 {int(HH)}시 {int(mm)}분')

    @staticmethod
    def connect_to_remote_computer_via_chrome_desktop():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        url = 'https://remotedesktop.google.com/access'
        FileSystemUtil.get_cmd_output(cmd=f'explorer "{url}"')

    @staticmethod
    def translate_eng_to_kor_via_googletrans(text: str):  # 수정할것 update 되었다는데 googletrans 업데이트 해보자
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        # from googletrans import Translator
        # translater = Translator()
        # text_translated = translater.translate([text_eng.split(".")], dest='ko')
        # for translation in text_translated:
        #     print(translation.origin, ' -> ', translation.text)
        # Park4139.debug_as_gui(context=text_translated, is_app_instance_mode=True)

        # from papago_translate import Translator
        # naver papago api 서비스는 2024 년 종료가 된다...
        # translator = Translator(service_urls=['translate.google.com', 'translate.google.co.kr'],user_agent='Mozilla/5.0 (Windows NT 10.0;  x64; Win64)', timeout=random.randint(0, 99) / 10)
        # tmp = translator.translate(text, src="ko", dest="en")
        # print(rf'tmp : {tmp}')
        # print(rf'type(tmp) : {type(tmp)}')
        # print(rf'len(tmp) : {len(tmp)}')
        # Park4139TestUtil.pause()

        # 한수훈 씨가 만든 모듈 같다. 무료이다. 단, 안정성 보장은 안되며, google 로 부터 ip가 차단이 될 수 있다.
        # 단일 텍스트의 최대 글자수 제한은 15k입니다. 이거 로직으로 제한 해야 한다.
        # 약간 시간적인 트릭도 넣을 것
        # <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
        # translator.translate('안녕하세요.', dest='ja')
        # <Translated src=ko dest=ja text=こんにちは。 pronunciation=Kon'nichiwa.>
        # translator.translate('veritas lux mea', src='la')
        # <Translated src=la dest=en text=The truth is my light pronunciation=The truth is my light>
        # 2023 12 31 01 11 현재시각기준 안된다

        # from googletrans import Translator
        # translator = Translator()
        # translator.detect('이 문장은 한글로 쓰여졌습니다.')
        # # <Detected lang=ko confidence=0.27041003>
        # translator.detect('この文章は日本語で書かれました。')
        # # <Detected lang=ja confidence=0.64889508>
        # translator.detect('This sentence is written in English.')
        # # <Detected lang=en confidence=0.22348526>
        # translator.detect('Tiu frazo estas skribita en Esperanto.')
        # # <Detected lang=eo confidence=0.10538048>

    @staticmethod
    def translate_kor_to_eng_foo(request: str):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        translator = Translator()
        text_translated = translator.translate(str(request), src='ko', dest='en')
        BusinessLogicUtil.debug(context=text_translated, is_app_instance_mode=True)

    @staticmethod
    def return_korean_week_name():
        weekday: str
        weekday = BusinessLogicUtil.get_time_as_('weekday')
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        if weekday == "0":
            return "월"
        elif weekday == "1":
            return "화"
        elif weekday == "2":
            return "수"
        elif weekday == "3":
            return "목"
        elif weekday == "4":
            return "금"
        elif weekday == "5":
            return "토"
        elif weekday == "6":
            return "일"
        else:
            return None

    @staticmethod
    def get_comprehensive_weather_information_from_web():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        try:
            while 1:
                ment_about_naver_weather = ""
                results_about_naver_weather = ""
                title = ""
                results_about_nationwide_ultrafine_dust = ""
                ment_about_geo = ""
                results_about_geo = ""
                ment_about_pm_ranking = ""
                results_about_pm_ranking = ""

                # answer = "tate no"
                # DebuggingUtil.commentize(f"{btn_text_clicked} 입력되었습니다")
                # Park4139.debug_as_cli(btn_text_clicked)
                # special_prefixes = " ".join(["subsplease", "1080"]) + " "
                # special_prefixes = " "
                # query = urllib.parse.quote(f"{special_prefixes}{btn_text_clicked}")
                # if query == "":
                #     Park4139Park4139.Tts.speak(  ment = "아무것도 입력되지 않았습니다")
                #     break
                # url = f'https://nyaa.si/?f=0&c=0_0&q={query}'

                # selenium way
                # DebuggingUtil.commentize("페이지 소스 중간 분석결과")
                # page_src = driver.page_source
                # soup = BeautifulSoup(page_src, "lxml")
                # selenium 으로 하면 선택은 깔끔한데, html 구조를 보는 방법을 아직 모르겠다. #selenium 자체 파서를 사용하는 방법이지 않을까 싶다
                # results = driver.find_element(By.XPATH, '//*[@id="body_main"]/table[2]')
                # Park4139.debug_as_cli(results.text)

                async def crawl_pm_ranking():
                    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
                    driver = None
                    try:
                        driver = SeleniumUtil.get_driver_for_selenium()
                        # 미세먼지랭킹 bs4 way
                        DebuggingUtil.commentize("페이지 TARGET URL RAW 소스 분석중")
                        ment = '미세먼지랭킹 웹사이트 크롤링 결과'
                        global ment_about_pm_ranking
                        ment_about_pm_ranking = ment
                        target_url = f'https://www.dustrank.com/air/air_dong_detail.php?addcode=41173103'
                        DebuggingUtil.print_ment_magenta(target_url)
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
                        global results_about_pm_ranking
                        results_about_pm_ranking = results
                        DebuggingUtil.print_ment_magenta(f"async def {inspect.currentframe().f_code.co_name}() is done...")
                        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
                    except:
                        DebuggingUtil.trouble_shoot("%%%FOO%%%")
                        # driver.close()
                        driver.quit()

                async def crawl_nationwide_ultrafine_dust():
                    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
                    driver = SeleniumUtil.get_driver_for_selenium()

                    # # '전국초미세먼지'(bs4 way)
                    DebuggingUtil.commentize("페이지 TARGET URL RAW 소스 분석중")
                    ment = '전국초미세먼지  크롤링 결과'
                    global title
                    title = ment
                    target_url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&qvt=0&query=전국초미세먼지'
                    DebuggingUtil.print_ment_magenta(target_url)
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
                    global results_about_nationwide_ultrafine_dust
                    results_about_nationwide_ultrafine_dust = results___
                    DebuggingUtil.print_ment_magenta(f"async def {inspect.currentframe().f_code.co_name}() is done...")
                    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")

                async def crawl_naver_weather():
                    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
                    driver = SeleniumUtil.get_driver_for_selenium()
                    # '동안구 관양동 날씨 정보'(bs4 way)
                    DebuggingUtil.commentize("페이지 TARGET URL RAW 소스 분석중")
                    ment = '네이버 동안구 관양동 날씨 크롤링 결과'

                    global ment_about_naver_weather
                    ment_about_naver_weather = ment
                    target_url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=동안구+관양동+날씨'
                    DebuggingUtil.print_ment_magenta(target_url)
                    driver.get(target_url)
                    page_src = driver.page_source
                    soup = BeautifulSoup(page_src, "lxml")
                    results: ResultSet = soup.find_all("div", class_="status_wrap")
                    results: str = results[0].text
                    # 리스트 요소 변경
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

                    # results: [str] = str(results_)  # dict to str (개행을 시키지 않은)

                    results: str = "\n".join([f"{key}: {value}" for key, value in results_refactored.items()])  # dict to str (개행을 시킨)

                    global results_about_naver_weather
                    results_about_naver_weather = results
                    DebuggingUtil.print_ment_magenta(f"async def {inspect.currentframe().f_code.co_name}() is done...")
                    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")

                async def crawl_geo_info():
                    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
                    # '지역 정보'(bs4 way)
                    driver = SeleniumUtil.get_driver_for_selenium()
                    DebuggingUtil.commentize("페이지 TARGET URL RAW 소스 분석중")
                    ment = '지역정보 크롤링 결과'
                    global ment_about_geo
                    ment_about_geo = ment
                    # target_url = 'https://map.naver.com/p'
                    target_url = 'https://www.google.com/search?q=현재위치'
                    DebuggingUtil.print_ment_magenta(target_url)
                    driver.get(target_url)
                    page_src = driver.page_source
                    soup = BeautifulSoup(page_src, "lxml")
                    results: any
                    # results = soup.find_all("body")
                    results: ResultSet = soup.find_all("span", class_="BBwThe")  # 지역정보 한글주소
                    # results: ResultSet = soup.find_all("span", class_="fMYBhe") # 지역정보 영어주소
                    results: str = results[0].text
                    global results_about_geo
                    results_about_geo = results
                    DebuggingUtil.print_ment_magenta(f"async def {inspect.currentframe().f_code.co_name}() is done...")
                    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")

                def run_async_loop1():
                    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
                    try:
                        # Park4139.debug_as_cli(f"def {inspect.currentframe().f_code.co_name}() is running...")
                        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.run_until_complete(crawl_pm_ranking())
                    except:
                        DebuggingUtil.trouble_shoot("%%%FOO%%%")

                def run_async_loop2():
                    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
                    # Park4139.debug_as_cli(f"def {inspect.currentframe().f_code.co_name}() is running...")
                    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(crawl_nationwide_ultrafine_dust())

                def run_async_loop3():
                    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
                    # Park4139.debug_as_cli(f"def {inspect.currentframe().f_code.co_name}() is running...")
                    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(crawl_naver_weather())

                def run_async_loop4():
                    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
                    # Park4139.debug_as_cli(f"def {inspect.currentframe().f_code.co_name}() is running...")
                    DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(crawl_geo_info())

                thread1 = threading.Thread(target=run_async_loop1)
                thread1.start()

                thread2 = threading.Thread(target=run_async_loop2)
                thread2.start()

                thread3 = threading.Thread(target=run_async_loop3)
                thread3.start()

                thread4 = threading.Thread(target=run_async_loop4)
                thread4.start()

                # 모든 쓰레드 끝날때 까지 대기
                thread1.join()
                thread2.join()
                thread3.join()
                thread4.join()

                TextToSpeechUtil.speak_ments(ment='날씨에 대한 웹크롤링 및 데이터 분석이 성공되었습니다', sleep_after_play=0.65)
                # 함수가 break 로 끝이 나면 창들이 창을 닫아야 dialog 들이 사라지도록 dialog 를 global 처리를 해두었음.
                DebuggingUtil.print_ment_light_yellow(f"{StateManagementUtil.LINE_LENGTH_PROMISED} {ment_about_naver_weather}")
                DebuggingUtil.print_ment_light_yellow(f"{results_about_naver_weather}")
                DebuggingUtil.print_ment_light_yellow(f"{StateManagementUtil.LINE_LENGTH_PROMISED} {title}")
                DebuggingUtil.print_ment_light_yellow(f"{results_about_nationwide_ultrafine_dust}")
                DebuggingUtil.print_ment_light_yellow(f"{StateManagementUtil.LINE_LENGTH_PROMISED} {ment_about_geo}")
                DebuggingUtil.print_ment_light_yellow(f"{results_about_geo}")
                DebuggingUtil.print_ment_light_yellow(f"{StateManagementUtil.LINE_LENGTH_PROMISED} {ment_about_pm_ranking}")
                DebuggingUtil.print_ment_light_yellow(f"{results_about_pm_ranking}")
                break
        except:
            DebuggingUtil.trouble_shoot("%%%FOO%%%")

    @staticmethod
    def back_up_biggest_targets():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        DebuggingUtil.commentize(f"biggest_targets에 대한 빽업을 시도합니다")
        for biggest_target in StateManagementUtil.biggest_targets:
            BusinessLogicUtil.back_up_target(f'{biggest_target}')

    @staticmethod
    def back_up_smallest_targets():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        DebuggingUtil.commentize(f"smallest_targets에 대한 빽업을 시도합니다")
        for target in StateManagementUtil.smallest_targets:
            BusinessLogicUtil.back_up_target(f'{target}')

    @staticmethod
    def classify_targets_between_smallest_targets_biggest_targets():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        DebuggingUtil.commentize('빽업할 파일들의 크기를 분류합니다.')
        targets = [
            rf"{StateManagementUtil.USERPROFILE}\Desktop\services\helper-from-youtube-url-to-webm",
            rf"{StateManagementUtil.USERPROFILE}\Desktop\services",
        ]
        DebuggingUtil.commentize('biggest_targets(300 메가 초과), smallest_targets(300 메가 이하) 분류 시도')
        for target in targets:
            target_size_megabite = FileSystemUtil.get_target_megabite(target.strip())
            print(target_size_megabite)
            if target_size_megabite <= 300:
                StateManagementUtil.smallest_targets.append(target.strip())

            elif 300 < target_size_megabite:
                StateManagementUtil.biggest_targets.append(target.strip())
            else:
                DebuggingUtil.print_ment_magenta(f'{target.strip()}pass')

        DebuggingUtil.commentize('smallest_target 출력')
        # targets 에서 biggest_targets 과 일치하는 것을 소거 시도
        smallest_targets = [i for i in targets if i not in StateManagementUtil.biggest_targets]
        for target in StateManagementUtil.smallest_targets:
            print(target)

        DebuggingUtil.commentize('biggest_target 출력')
        for target in StateManagementUtil.biggest_targets:
            print(target)
        pass

    @staticmethod
    def gather_storages():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        starting_directory = os.getcwd()
        dst = rf"{StateManagementUtil.USERPROFILE}\Desktop\services\storage"  # 이거 변경하자.
        services = os.path.dirname(dst)
        os.chdir(services)
        storages = []
        cmd = rf'dir /b /s "{StateManagementUtil.USERPROFILE}\Downloads"'
        lines = FileSystemUtil.get_cmd_output(cmd)
        for line in lines:
            if line.strip() != "":
                storages.append(line.strip())

        DebuggingUtil.commentize(rf'archive_py 는 storage 목록 에서 제외')
        withouts = ['archive_py']
        for storage in storages:
            for without in withouts:
                if BusinessLogicUtil.is_regex_in_contents(target=storage, regex=without):
                    storages.remove(storage)
        for storage in storages:
            print(storage)

        DebuggingUtil.commentize(rf'이동할 storage 목록 중간점검 출력 시도')
        for storage in storages:
            print(os.path.abspath(storage))

        if not storages:
            DebuggingUtil.commentize(rf'이동할 storage 목록 이 없어 storage 이동을 할 수 없습니다')
        else:
            DebuggingUtil.commentize(rf'이동할 storage 목록 출력 시도')
            for storage in storages:
                print(os.path.abspath(storage))
            DebuggingUtil.commentize(rf'목적지 생성 시도')
            if not os.path.exists(dst):
                os.makedirs(dst)
            for storage in storages:
                # print(src)
                try:
                    DebuggingUtil.commentize(rf'storage 이동 시도')
                    FileSystemUtil.move_target_without_overwrite(storage, dst)
                except FileNotFoundError:
                    DebuggingUtil.trouble_shoot('202312071430')

                except Exception as e:
                    DebuggingUtil.trouble_shoot('20231205095308')

        os.chdir(starting_directory)

    @staticmethod
    def run_targets_promised():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        try:
            targets = [
                # Park4139.MUSIC_FOR_WORK,
                StateManagementUtil.PYCHARM64_EXE,
                StateManagementUtil.PROJECT_DIRECTORY,
                StateManagementUtil.SERVICE_DIRECTORY,
            ]
            for target in targets:
                FileSystemUtil.explorer(target)
        except:
            DebuggingUtil.trouble_shoot("%%%FOO%%%")

    @staticmethod
    def change_console_color():
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        TextToSpeechUtil.speak_ments(ment="테스트 콘솔의 색상을 바꿔볼게요", sleep_after_play=0.65)
        BusinessLogicUtil.toogle_console_color(color_bg='0', colors_texts=['7', 'f'])

    @staticmethod
    def taskkill_useless_programs():
        targets = [
            # "python.exe", # 프로그램 스스로를 종료시켜는 방법
            "alsong.exe",
            "cortana.exe",
            "mysqld.exe",
            "KakaoTalk.exe",
            "OfficeClickToRun.exe",
            "TEWebP.exe",
            "TEWeb64.exe",
            "TEWebP64.exe",
            "AnySign4PC.exe",
        ]
        for target in targets:
            BusinessLogicUtil.taskkill(target)

    @staticmethod
    def is_christmas():
        import datetime
        today = datetime.datetime.now()
        christmas = datetime.datetime(year=today.year, month=12, day=25)
        if today == christmas:
            return True
        else:
            return False

    @staticmethod
    def is_same_time(time1, time2):
        time2.strftime(rf'%Y-%m-%d %H:%M:%S')
        # print(rf'time1 : {time1} , time2 : {time2}')
        if time1 == time2:
            return True
        else:
            return False

    @staticmethod
    def is_midnight():
        import datetime
        now = datetime.datetime.now()
        if now.hour == 0 and now.minute == 0 and now.second == 0:
            return True
        else:
            return False

    @staticmethod
    def back_up_project_and_change_to_power_saving_mode():
        BusinessLogicUtil.back_up_target(target_abspath=StateManagementUtil.PROJECT_DIRECTORY)
        FileSystemUtil.enter_power_saving_mode()

    @staticmethod
    @TestUtil.measure_seconds_performance_once  #
    def crawl_html_href(url: str):
        DebuggingUtil.print_ment_via_colorama(f"{StateManagementUtil.LINE_LENGTH_PROMISED} {inspect.currentframe().f_code.co_name}", colorama_color=ColoramaColorUtil.BLUE)
        # 최하단으로 스크롤 이동 처리를 추가로 해야함. 그렇지 않으면 기대하는 모든 영상을 크롤링 할 수 없음..귀찮..지만 처리했다.

        # url 전처리
        url = url.strip()

        # driver 설정
        DebuggingUtil.print_ment_via_colorama(f"SeleniumUtil.get_driver_for_selenium() 수행 중...", colorama_color=ColoramaColorUtil.BLUE)
        driver = SeleniumUtil.get_driver_for_selenium()

        DebuggingUtil.print_ment_via_colorama(f"driver.get(target_url) 수행 중...", colorama_color=ColoramaColorUtil.BLUE)
        target_url = url
        driver.get(target_url)

        # 자동제어 브라우저 화면 초기 로딩 random.randint(1,n) 초만큼 명시적 대기
        n = 2
        seconds = random.randint(1, n)
        DebuggingUtil.print_ment_via_colorama(f"자동제어 브라우저 화면 초기 로딩 중... {seconds} seconds", colorama_color=ColoramaColorUtil.BLUE)
        driver.implicitly_wait(seconds)  # 처음페이지 로딩이 끝날 때까지 약 random.randint(1,n)초 대기

        # 최하단으로 자동 스크롤, 페이지 최하단에서 더이상 로딩될 dom 객체가 없을 때 까지
        DebuggingUtil.print_ment_via_colorama("스크롤 최하단으로 이동 중...", colorama_color=ColoramaColorUtil.BLUE)
        scroll_cnt = 0
        previous_scroll_h = None
        current_scroll_h = None
        scroll_maxs_monitored = []
        while True:
            if current_scroll_h is not None and previous_scroll_h is not None:
                if previous_scroll_h == current_scroll_h:
                    scroll_maxs_monitored.append(True)
                    # break

            # 로딩타이밍 제어가 어려워 추가한 코드. n번 모니터링.
            n = 6  # success
            if len(scroll_maxs_monitored) == n:
                if all(scroll_maxs_monitored) == True:  # [bool] bool list 내 요소가 모두 true 인지 확인
                    DebuggingUtil.print_ment_via_colorama(ment="스크롤 최하단으로 이동되었습니다", colorama_color=ColoramaColorUtil.BLUE)
                    break

            # previous_scroll_h 업데이트
            # previous_scroll_h = driver.execute_script("return document.body.scrollHeight")
            previous_scroll_h = driver.execute_script("return document.documentElement.scrollHeight")

            # 가능한만큼 스크롤 최하단으로 이동
            # driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)  # page_down 을 누르는 방법, success
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")# JavaScript 로 스크롤 최하단으로 이동, 네이버용 코드?
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")  # JavaScript 로 스크롤 최하단으로 이동, 유튜브용 코드?
            # time.sleep(2)  # 스크롤에 의한 추가적인 dom 객체 로딩 대기, 여러가지 예제를 보니, 일반적으로 2 초 정도 두는 것 같음. 2초 내에 로딩이 되지 않을 때도 있는데.
            BusinessLogicUtil.sleep(milliseconds=500, printing_mode=False)  # 스크롤에 의한 추가적인 dom 객체 로딩 대기, success, 지금껏 문제 없었음.

            # previous_scroll_h = driver.execute_script("return document.body.scrollHeight")
            current_scroll_h = driver.execute_script("return document.documentElement.scrollHeight")

            scroll_cnt = scroll_cnt + 1

            DebuggingUtil.print_ment_via_colorama(f'{scroll_cnt}번 째 스크롤 성공 previous_scroll_h : {previous_scroll_h} current_scroll_h : {current_scroll_h}   previous_scroll_h==current_scroll_h : {previous_scroll_h == current_scroll_h}', colorama_color=ColoramaColorUtil.BLUE)

        page_src = driver.page_source
        soup = BeautifulSoup(page_src, "lxml")
        driver.close()

        # 모든 태그 가져오기
        # tags = soup.find_all()
        # for tag in tags:
        #     print(tag)

        # body 리소스 확인 : success
        # bodys = soup.find_all("body")
        # for body in bodys:
        #     print(f"body:{body}")

        # 이미지 태그 크롤링
        # images = soup.find_all("img")
        # for img in images:
        #     img_url = img.get("src")
        #     print("Image URL:", img_url)
        #
        # 스크립트 태그 크롤링
        # scripts = soup.find_all("script")
        # for script in scripts:
        #     script_url = script.get("src")
        #     print("Script URL:", script_url)
        #
        # # 스타일시트 크롤링
        # stylesheets = soup.find_all("link", rel="stylesheet")
        # for stylesheet in stylesheets:
        #     stylesheet_url = stylesheet.get("href")
        #     print("Stylesheet URL:", stylesheet_url)

        # 특정 태그의 class 가 "어쩌구" 인
        # div_tags = soup.find_all("div", class_="어쩌구")

        # a 태그 크롤링
        # a_tags = soup.find_all("a")
        # results = ""
        # for a_tag in a_tags:
        #     hrefs = a_tag.get("href")
        #     if hrefs != None and hrefs != "":
        #         # print("href", hrefs)
        #         results = f"{results}{hrefs}\n"

        # 변수에 저장 via selector
        # name = soup.select('a#video-title')
        # video_url = soup.select('a#video-title')
        # view = soup.select('a#video-title')

        # name, video_url 에 저장 via tag_name and id
        name = soup.find_all("a", id="video-title")
        video_url = soup.find_all("a", id="video-title")

        # 유튜브 주소 크롤링 및 진행률 표시 via tqdm, 14 초나 걸리는데. 성능이 필요할때는 여러개의 thread 로 처리해보자.
        a_tags = soup.find_all("a")

        # success
        # BusinessLogicUtil.debug_as_gui(f"{len(a_tags)}")

        # results를 str으로 처리
        # results = ""
        # a_tags_cnt  = 0
        # with tqdm(total=total_percent,ncols = 79 , desc= "웹 크롤링 진행률") as process_bar:
        #     for a_tag in a_tags:
        #         hrefs = a_tag.get("href")
        #         if hrefs != None and hrefs != "" and "/watch?v=" in hrefs :
        #             if hrefs not in results:
        #                 results = f"{results}{hrefs}\n"
        #                 a_tags_cnt = a_tags_cnt + 1
        #         time.sleep(0.06)
        #         process_bar.update(total_percent/len(a_tags))

        # fail
        # if process_bar.total == 90:
        #     TextToSpeechUtil.speak_ments(ment='웹 크롤링이 90퍼센트 진행되었습니다. 잠시만 기다려주세요', sleep_after_play=0.65)

        # results를 list 으로 처리, list 으로만 처리하고 str 으로 변형하는 처리를 추가했는데 3초나 빨라졌다. 항상 list 로 처리를 하자.
        results = []
        a_tags_cnt = 0
        for a_tag in a_tags:
            hrefs = a_tag.get("href")
            if hrefs != None and hrefs != "" and "/watch?v=" in hrefs:
                if hrefs not in results:
                    results.append(hrefs)
                    a_tags_cnt = a_tags_cnt + 1
        results = DataStructureUtil.add_prefix_to_string_list(results, 'https://www.youtube.com')  # string list 의 요소마다 suffix 추가
        results = "\n".join(results)  # list to str

        # fail
        # DebuggingUtil.print_ment_magenta()(title=f"크롤링결과보고", ment=f"{results}", btns=[MentsUtil.YES], auto_click_positive_btn_after_seconds="")
        #

        # fail
        # DebuggingUtil.print_ment_magenta((title="크롤링결과보고", ment=f"{results}")mkrmkr

        # success
        # BusinessLogicUtil.debug_as_gui(f"{results}") # 테스트용 팝업    UiUtil 로 옮기는 게 나을 지 고민 중이다.

        # success
        # 비동기로 진행 가능

        DebuggingUtil.print_ment_magenta(ment=f"({a_tags_cnt}개 추출됨)\n\n{results}")

    @staticmethod
    def crawl_youtube_video_title_and_url(url: str):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")

        # url 전처리
        url = url.strip()

        # driver 설정
        total_percent = 100
        driver = SeleniumUtil.get_driver_for_selenium()
        with tqdm(total=total_percent, ncols=79, desc="driver 설정 진행률") as process_bar:
            global title
            title = 'html  href 크롤링 결과'
            target_url = url
            driver.get(target_url)
            page_src = driver.page_source
            soup = BeautifulSoup(page_src, "lxml")
            time.sleep(0.0001)
            process_bar.update(total_percent)
        driver.close()

        # 변수에 저장 via tag_name and id
        name = soup.find_all("a", id="video-title")
        video_url = soup.find_all("a", id="video-title")

        # list 에 저장
        name_list = []
        url_list = []
        # view_list = []
        for i in range(len(name)):
            name_list.append(name[i].text.strip())
            # view_list.append(view[i].get('aria-label').split()[-1])
        for i in video_url:
            url_list.append('{}{}'.format('https://www.youtube.com', i.get('href')))

        # dict 에 저장
        # youtubeDic = {
        #     '제목': name_list,
        #     '주소': url_list,
        #     # '조회수': view_list
        # }

        # csv 에 저장
        # import pandas as pd
        # youtubeDf = pd.DataFrame(youtubeDic)
        # youtubeDf.to_csv(f'{keyword}.csv', encoding='', index=False)

        # str 에 저장
        results_list = []
        for index, url in enumerate(url_list):
            results_list.append(f"{name_list[index]}   {url_list[index]}")
        results_str = "\n".join(results_list)  # list to str

        # fail
        # DebuggingUtil.print_ment_magenta()(title=f"크롤링결과보고", ment=f"{results}", btns=[MentsUtil.YES], auto_click_positive_btn_after_seconds="")
        #

        # fail
        # DebuggingUtil.print_ment_magenta((title="크롤링결과보고", ment=f"{results}")mkrmkr

        # success
        # BusinessLogicUtil.debug_as_gui(f"{results}") # 테스트용 팝업    UiUtil 로 옮기는 게 나을 지 고민 중이다.

        # success
        # 비동기로 진행 가능

        DebuggingUtil.print_ment_magenta(ment=f"({len(url_list)}개 url 추출됨)\n\n{results_str}")

    @staticmethod
    def crawl_youtube_playlist(url: str):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")

        # url 전처리
        url = url.strip()

        # driver 설정
        total_percent = 100
        driver = SeleniumUtil.get_driver_for_selenium()
        with tqdm(total=total_percent, ncols=79, desc="driver 설정 진행률") as process_bar:
            global title
            title = 'html  href 크롤링 결과'
            target_url = url
            driver.get(target_url)
            page_src = driver.page_source
            soup = BeautifulSoup(page_src, "lxml")
            time.sleep(0.0001)
            process_bar.update(total_percent)
        driver.close()

        # 변수에 저장 via tag_name and href
        names = soup.find_all("a", id="video-title")
        hrefs = soup.find_all("a", id="video-title")
        # hrefs = copy.deepcopy(names)

        # list 에 저장
        name_list = []
        hrefs_list = []
        # view_list = []
        for i in range(len(names)):
            name_list.append(names[i].text.strip())
            # view_list.append(view[i].get('aria-label').split()[-1])
        for i in hrefs:
            hrefs_list.append('{}{}'.format('https://www.youtube.com', i.get('href')))

        # str 에 저장
        results_list = []
        for index, url in enumerate(hrefs_list):
            # results_list.append(f"{name_list[index]}   {hrefs_list[index]}")
            results_list.append(f"{hrefs_list[index]}")  # href 만 출력
        results_str = "\n".join(results_list)  # list to str

        # fail
        # DebuggingUtil.print_ment_magenta()(title=f"크롤링결과보고", ment=f"{results}", btns=[MentsUtil.YES], auto_click_positive_btn_after_seconds="")
        #

        # fail
        # DebuggingUtil.print_ment_magenta((title="크롤링결과보고", ment=f"{results}")mkrmkr

        # success
        # BusinessLogicUtil.debug_as_gui(f"{results}") # 테스트용 팝업    UiUtil 로 옮기는 게 나을 지 고민 중이다.

        # success
        # 비동기로 진행 가능

        DebuggingUtil.print_ment_magenta(ment=f"({len(hrefs_list)}개 playlist 추출됨)\n\n{results_str}")

    @staticmethod
    def print_json_via_jq_pkg(json_str=None, json_file=None, json_list=None):
        DebuggingUtil.commentize(f"{inspect.currentframe().f_code.co_name}()")
        if BusinessLogicUtil.get_none_count_of_list([json_str, json_file, json_list]) == 2:  # 2개가 NONE이면 1나는 BINDING 된것으로 판단하는 로직
            if json_str != None:
                # lines = FileSystemUtil.get_cmd_output(cmd=rf'echo "{json_str}" | {StateManagementUtil.JQ_WIN64_EXE} "."') # 나오긴 하는데 한줄로 나온다
                # lines = FileSystemUtil.get_cmd_output(cmd=rf'echo "{json_str}" | python -mjson.tool ')# 나오긴 하는데 한줄로 나온다
                # [DebuggingUtil.print_as_success(line) for line in lines]
                json_str = json.dumps(json_str, indent=4)  # json.dumps() 함수는 JSON 데이터를 문자열로 변환하는 함수이며, indent 매개변수를 사용하여 들여쓰기를 설정하여 json 형태의 dict 를 예쁘게 출력할 수 있습니다.
                DebuggingUtil.print_ment_light_white(json_str)
            if json_file != None:
                lines = FileSystemUtil.get_cmd_output(cmd=rf"type {json_file} | {StateManagementUtil.JQ_WIN64_EXE} ")
                [DebuggingUtil.print_ment_light_white(line) for line in lines]
            if json_list != None:
                lines = FileSystemUtil.get_cmd_output(cmd=rf'echo "{json_list}" | "{StateManagementUtil.JQ_WIN64_EXE}" ')
                [DebuggingUtil.print_ment_light_white(line) for line in lines]
        else:
            DebuggingUtil.print_ment_fail(ment=rf"{inspect.currentframe().f_code.co_name}() 를 사용하려면 json_str/json_file/json_list 파라미터들 중 둘 중 하나만 데이터바인딩이 되어야합니다")

    @staticmethod
    def get_random_alphabet():
        return random.choice(string.ascii_letters)

    @staticmethod
    def get_random_int():
        pass


class FastapiServerUtil:
    # def import_pkg_park4139():  # 명령어 자체가 안되는데 /mir 은 되는데 /move 안된다
    # try:
    # 파이썬 프로젝트 외부 패키지 import 시키는 방법 : 일반적으로는 불가능하다.
    # services_directory_abspath = os.path.dirname(os.path.dirname(__file__))
    # external_pkg_abspath = rf'{services_directory_abspath}\archive_py\pkg_park4139'
    # print(rf'external_pkg_abspath : {external_pkg_abspath}')
    # os.environ['PKG_PARK4139_ABSPATH'] = rf'{external_pkg_abspath}'
    # sys.path.append(external_pkg_abspath)
    # print(rf'sys.path : {sys.path}')
    # from ..archive_py.pkg_park4139 import FileSystemUtil, StateManagementUtil, TestUtil
    # except:
    #     pass
    # try:
    # 대안 global pkg 로 복사하고 쓰고 실행후에는 프로젝트 내에서 패키지를 삭제한다 > 자동화할것
    # 의존성을 추가하기 위해서, pkg_park4139의 .venv 도 따라 복사한다.
    # CURRENT_PROJECT_DIRECTORY= os.path.dirname(__file__)
    # SERVICES_DIRECTORY = os.path.dirname(CURRENT_PROJECT_DIRECTORY)
    # EXTERNAL_PKG_ABSPATH = rf'{SERVICES_DIRECTORY}\archive_py\pkg_park4139'
    # # VIRTUAL_PKG_ABSPATH = rf'{CURRENT_PROJECT_DIRECTORY}\.venv\Lib\site-packages'
    # INTERNAL_PKG_ABSPATH = rf'{CURRENT_PROJECT_DIRECTORY}\pkg_park4139'
    # print(rf'VIRTUAL_PKG_ABSPATH : {INTERNAL_PKG_ABSPATH}')
    # os.system(rf'chcp 65001')
    # os.system(rf'robocopy "{EXTERNAL_PKG_ABSPATH}" "{INTERNAL_PKG_ABSPATH}" /MIR')
    # # os.system("pause")
    # print("파이썬 프로젝트 외부 패키지 import 시도에 성공하였습니다")
    # except Exception:
    #     print("파이썬 프로젝트 외부 패키지 import 시도에 실패하였습니다")
    #     sys.exit()
    # try:
    # 그냥 pkg 내에 집어 넣었다. 가상환경도 동일하게 개발한다.
    # except:
    #     pass
    # pass

    @staticmethod
    def convert_file_from_cp_949_to_utf_8(file_abspath):
        # import codecs
        # file_abspath_converted = rf"{FileSystemUtil.get_target_as_pn(file_abspath)}_utf_8{FileSystemUtil.get_target_as_x(file_abspath)}"
        # print(file_abspath_converted)
        # # 기존 파일을 'utf-8'로 읽어오고, 새로운 파일에 'utf-8'로 저장
        # with codecs.open(file_abspath, 'r', encoding='cp949') as file_previous:
        #     contents = file_previous.read()
        #     with codecs.open(file_abspath_converted, 'w', encoding='utf-8') as new_file:
        #         new_file.write(contents)
        pass

    @staticmethod
    def get_max_id_from_database():
        # db.json 파일을 UTF-8 인코딩으로 읽어옴
        with open(StateManagementUtil.DB_JSON, 'r', encoding='utf-8') as file:
            data = json.load(file)
            boards = data.get('boards', [])
        if boards:
            # boards 객체가 존재하는 경우 최대 ID를 조회
            max_id = max(board['id'] for board in boards)
            return max_id
        else:
            # boards 객체가 없는 경우 None 반환
            return None

    @staticmethod
    def fill_increment_id_auto():
        # 데이터베이스에서 현재의 최대 ID 조회
        max_id: int = int(FastapiServerUtil.get_max_id_from_database())  # 데이터베이스에서 최대 ID를 조회하는 함수로 구현되어야 합니다.

        if max_id is not None:
            # 최대 ID가 존재하는 경우 다음 ID를 생성하여 반환
            next_id = max_id + 1
        else:
            # 최대 ID가 없는 경우 1부터 시작
            next_id = 1
        return next_id

    @staticmethod
    def init_cors_policy_allowed(app):
        # add_middleware()를 통한 CORS 설정
        origins = [
            # DEV
            # "*", # host 0.0.0.0 이랑 같이 설정 안되는? 설마
            "https://e-magazine-jung-hoon-parks-projects.vercel.app",
            "https://e-magazine-jung-hoon-parks-projects.vercel.app/page-next-js",
            #     "http://localhost.tiangolo.com",
            #     "https://localhost.tiangolo.com",
            #     "http://localhost",
            #     "http://localhost:8080",
            # "http://localhost:3000",  # client 의 설정     "127.0.0.1:11430" next.js 이렇게 실행되는데?
            #
            # OP
            #
        ]
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,  # cookie 포함 여부를 설정. 기본은 False
            allow_methods=["*"],  # 허용할 method를 설정할 수 있으며, 기본값은 'GET'이다. OPTIONS request ?
            allow_headers=["*"],  # 허용할 http header 목록을 설정할 수 있으며 Content-Type, Accept, Accept-Language, Content-Language은 항상 허용된다.
        )

    @staticmethod
    def init_Logging_via_middleware(app):
        # 미들웨어를 통한 로깅
        # @app.middleware("http")
        # async def log_requests(request: Request, call_next):
        #     logging.debug(f"요청: {request.method} {request.url}")
        #     response = await call_next(request)
        #     logging.debug(f"응답: {response.status_code}")
        #     return response
        pass

    @staticmethod
    def init_domain_address_allowed(app):
        # 접속허용도메인 주소 제한, 이 서버의 api 를 특정 도메인에서만 호출 가능하도록 설정
        # @app.middleware("http")
        # async def domain_middleware(request: Request, call_next):
        #     allowed_domains = ["example.com", "subdomain.example.com"]
        #     client_host = request.client.host
        #     client_domain = client_host.split(":")[0]  # 도메인 추출
        #     if client_domain not in allowed_domains:
        #         raise HTTPException(status_code=403, detail="Forbidden")
        #     response = await call_next(request)
        #     return response
        pass

    @staticmethod
    def init_ip_address_allowed(app):
        # 접속허용IP 주소 제한
        # @app.middleware("http")
        # async def ip_middleware(request: Request, call_next):
        #     allowed_ips = [
        #         "127.0.0.1",
        #         "10.0.0.1",
        #     ]
        #     client_ip = request.client.host
        #     if client_ip not in allowed_ips:
        #         raise HTTPException(status_code=403, detail="Forbidden")
        #     response = await call_next(request)
        #     return response
        pass

    @staticmethod
    async def do_preprocess_before_request(request):
        DebuggingUtil.commentize(f"{str(request.url)} 로 라우팅 시도 중...")

    @staticmethod
    async def do_preprocess_after_request(request, response):
        # DebuggingUtil.commentize(f"{str(request.url)} 로 라우팅 되었습니다")
        pass

    class Settings:
        protocol_type = "http",
        # protocol_type =  "https",
        # :: PRODUCTION MODE SETTING (http:*:*)
        # :: DEVELOPMENT MODE SETTING (http:*:8080)
        # host =  "0.0.0.0",
        # host =  "0.0.0.0",
        host = "127.0.0.1",  # localhost
        # port =  80,
        port = 8080,
        # port = 9002,

    @staticmethod
    def init_and_update_json_file(JSON_FILE, objects=None):
        if objects is None:
            objects = []
        try:
            FileSystemUtil.make_leaf_file(file_abspath=JSON_FILE)
            if os.path.exists(JSON_FILE):
                if FileSystemUtil.is_letters_cnt_zero(file_abspath=JSON_FILE) == True:
                    FileSystemUtil.add_text_to_file(file_abspath=JSON_FILE, text="[]\n")  # 이러한 형태로 객체를 받을 수 있도록 작성해 두어야 받을 수 있음.
                else:
                    if not os.path.isfile(JSON_FILE):
                        with open(JSON_FILE, "w", encoding='utf-8') as f:
                            json.dump(objects, f, ensure_ascii=False)  # ensure_ascii=False 는 encoding 을 그대로 유지하는 것 같다. ascii 로 변환하는게 안전할 지도 모르겠다.
                    else:
                        with open(JSON_FILE, "r", encoding='utf-8') as f:
                            # DebuggingUtil.print_ment_via_colorama(f"{BOOKS_FILE} 업로드 되었습니다", colorama_color=ColoramaColorUtil.LIGHTWHITE_EX)
                            objects = json.load(f)
                        return objects
        except IOError as e:
            print("파일 작업 중 오류가 발생했습니다:", str(e))


class DataObjectUtil:
    class NavItem(BaseModel):
        index: str
        title: str
        href: str
        description: str

    class Board(BaseModel):
        id: int = Field(default_factory=lambda: FastapiServerUtil.fill_increment_id_auto(), alias="_id")
        title: str
        content: str

        class Config:
            populate_by_name = True

    @staticmethod
    def is_board_validated(board: Board) -> bool:
        # Board(게시물)의 유효성을 검사하는 커스텀 비지니스 로직을 구현, create/update 의 경우에 사용
        if not board.title:
            return False
        if not board.content:
            return False
        return True

    # BaseModel 를 상속받은 Book 은 일반적인 객체가 아니다. type 을 출력해봐도 pydantic 의 하위 객체를 상속한 것으로 보인다
    class Book(BaseModel):
        book_id: Optional[str] = uuid4().hex  # Optional 을 설정하면 nullable 되는 거야?
        name: str
        genre: Literal["러브코메디", "러브픽션", "액션"]  # string literal validation 설정, 이 중 하나만 들어갈 수 있음
        # price: float
        price: int

    class TodoItem(BaseModel):
        id: str
        title: str
        completed: bool

    class Member(BaseModel):  # 여기에 validation 해두면 docs에서 post request 시 default 값 지정해 둘 수 있음.
        id: str = uuid4().hex + BusinessLogicUtil.get_time_as_('%Y%m%d%H%M%S%f') + BusinessLogicUtil.get_random_alphabet()
        pw: str
        name: constr(max_length=30)
        date_join: str = BusinessLogicUtil.get_time_as_('%Y-%m-%d %H:%M %S%f')
        date_logout_last: str
        address_house: str
        address_e_mail: str
        number_phone: str

        @classmethod  # class 간 종속 관계가 있을 때 하위 class 에 붙여 줘야하나?, cls, 파라미터와 함께? , instance를 생성하지 않고 호출 가능해?
        @field_validator('date_join')
        def validate_date_join(cls, date_join):
            # datetime.strptime(date_join, '%Y-%m-%d %H:%M %S%f')
            if len(date_join) != 18:
                raise HTTPException(status_code=400, detail="유효한 날짜가 아닙니다")
            return date_join

        @classmethod
        @field_validator('address_e_mail')
        def validate_address_e_mail(cls, address_e_mail):
            # if not address_e_mail.endswith('@kakao.com'):
            #     raise HTTPException(status_code=400, detail="유효한 카카오 이메일이 아닙니다.")
            # return address_e_mail
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(pattern, address_e_mail):
                raise HTTPException(status_code=400, detail="유효한 이메일 주소가 아닙니다.")
            return address_e_mail

        @classmethod
        @field_validator('pw')
        def validate_pw(cls, pw):
            if len(pw) != 18:
                raise HTTPException(status_code=400, detail="유효한 이메일 주소가 아닙니다.")
            return pw

        # 전화번호는 커스텀으로 따로 만들어야 함
        # constr(pattern=r'^\d{3}-\d{3,4}-\d{4}$')
        # constr(pattern=r'^\d{2}-\d{3,4}-\d{4}$') 둘다 .
