import random
import time

from config import getConfig
from log import Logger
from login import exercise_sign_in, exercise_sign_out, login_selenium_firefox
from mail import send_email

if __name__ == "__main__":
    log = Logger("log/ipahw.log")
    username = getConfig("USER", "USERNAME")  # 学工号
    password = getConfig("USER", "PASSWORD")  # 密码
    token, gsessionid = login_selenium_firefox(username, password)

    if token and gsessionid:
        time.sleep(random.randint(2, 4))  # 随机等待几秒，避免被识别为爬虫
        is_success, msg = exercise_sign_in(token, gsessionid)
        if is_success:
            log.logger.info(f"签到成功，is_success: {is_success}, msg: {msg}")
        else:
            log.logger.warning(
                f"签到失败！！！is_success: {is_success}, msg: {msg}, username: {username}, password: {password}"
            )
            send_email(
                subject="体育签到", content=f"签到失败！！！is_success: {is_success}, msg: {msg}"
            )

        time.sleep(random.randint(1888, 3600))  # 锻炼 ing，之后再签退
        token, gsessionid = login_selenium_firefox(
            username, password
        )  # 刷新 token 和 gsessionid
        time.sleep(random.randint(2, 4))
        is_success, msg = exercise_sign_out(token, gsessionid)
        if is_success:
            log.logger.info(f"签退成功，is_success: {is_success}, msg: {msg}")
        else:
            log.logger.warning(
                f"签退失败！！！is_success: {is_success}, msg: {msg}, username: {username}, password: {password}"
            )
            send_email(
                subject="体育签到", content=f"签退失败！！！is_success: {is_success}, msg: {msg}"
            )

    else:
        log.logger.warning(f"登录失败！！！token: {token}, gsessionid: {gsessionid}")
        send_email(subject="体育签到", content=f"登录失败！！！")
