from locust import task, SequentialTaskSet, HttpUser, constant_pacing, events, FastHttpUser
from config.config import cfg, logger
import sys


class PurchaseFlightTicket(SequentialTaskSet): # класс с задачами (содержит основной сценарий)
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
            # debug_stream=sys.stderr
        )
        # logger.info(f"Статус ответа:{r00_01_response.status_code}, Тело ответа: {r00_01_response.text}")
        # print(f"Статус ответа:{r00_01_response.status_code}, Тело ответа: {r00_01_response.text}")

class WebToursBaseUserClass(FastHttpUser): # юзер-класс, принимающий в себя основные параметры теста
    wait_time = constant_pacing(cfg.pacing)
    host = cfg.url

    tasks = [PurchaseFlightTicket]