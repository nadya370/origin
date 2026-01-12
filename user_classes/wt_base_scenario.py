from locust import task, SequentialTaskSet, HttpUser, constant_pacing, events, FastHttpUser
import sys, re, random
from config.config import logger, cfg
from utils.assertion import check_http_response
from utils.non_test_methods import open_csv_file, open_random_csv_file




class PurchaseFlightTicket(SequentialTaskSet): # класс с задачами (содержит основной сценарий)
    def on_start(self):
        self.user_data_csv_file = './test_data/user_data.csv'
        self.users_data = open_csv_file(self.user_data_csv_file)
        self.random_users_data = open_random_csv_file(self.user_data_csv_file)
        logger.info(f"____СПИСОК ПОЛЬЗОВАТЕЛЕЙ: {self.random_users_data}")

    @task()
    def uc_00_getHomePage(self):
        r00_01_WebTours = self.client.get(
            '/WebTours/',
            name="r00_01_response",
            allow_redirects=False,
            headers={
                'sec-ch-ua': '"Chromium";v="142", "YaBrowser";v="25.12", "Not_A Brand";v="99", "Yowser";v="2.5"',
                'sec-ch-ua-mobile': '?0'
            },
        #     debug_stream=sys.stderr
        )

        with self.client.get(
            '/WebTours/header.html',
            name="r00_02_header_html",
            allow_redirects=False,
            # debug_stream=sys.stderr,
            catch_response=True
        ) as r00_02_header_html:
            check_http_response(r00_02_header_html, 'images/webtours.png')


        with self.client.get(
            '/cgi-bin/welcome.pl?signOff=true',
            name="r00_03_welcome_pl",
            allow_redirects=False,
            catch_response=True
            # debug_stream=sys.stderr
        ) as r00_03_welcome_pl:
            check_http_response(r00_03_welcome_pl, 'Web Tours')

        with self.client.get(
            '/cgi-bin/nav.pl?in=home',
            name="r00_04_nav_pl",
            allow_redirects=False,
            catch_response=True
            # debug_stream=sys.stderr
        ) as r00_04_nav_pl:
            check_http_response(r00_04_nav_pl, 'Web Tours Navigation Bar')

        self.user_session = re.search(r"name=\"userSession\" value=\"(.*)\"\/", r00_04_nav_pl.text).group(1)
        
        with self.client.get(
            '/WebTours/home.html',
            name="r00_05_home_html",
            allow_redirects=False,
            catch_response=True
            # debug_stream=sys.stderr
        ) as r00_05_home_html:
            check_http_response(r00_05_home_html, 'Welcome to the Web Tours site.')
    
        # logger.info(f"Статус ответа:{r00_01_response.status_code}, Тело ответа: {r00_01_response.text}")
        # print(f"Статус ответа:{r00_01_response.status_code}, Тело ответа: {r00_01_response.text}")

    @task()
    def uc_01_Login(self):
        self.users_row = next(self.users_data)
        self.random_users_row = random.choice(self.random_users_data)
        self.login = self.random_users_row["username"]
        self.password = self.random_users_row["password"]
        
        self.body_r01_login_pl = f'userSession={self.user_session}&username={self.login}&password={self.password}&login.x=46&login.y=9&JSFormSubmit=off'
        print(f"________BODY LOGIN: {self.body_r01_login_pl}")
        logger.info(f"________BODY LOGIN: {self.body_r01_login_pl}")

        with self.client.post(
            '/cgi-bin/login.pl',
            name="r01_01_login_pl",
            allow_redirects=False,
            catch_response=True,
            headers={
                'content-type': 'application/x-www-form-urlencoded'
                },
            data=self.body_r01_login_pl
            # debug_stream=sys.stderr
        ) as r00_05_home_html:
            check_http_response(r00_05_home_html, 'Web Tours')


class WebToursBaseUserClass(FastHttpUser): # юзер-класс, принимающий в себя основные параметры теста
    wait_time = constant_pacing(cfg.pacing)
    host = cfg.url

    tasks = [PurchaseFlightTicket]