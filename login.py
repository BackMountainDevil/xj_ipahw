import random
import time


def login_selenium_firefox(username, password):
    """
    登录 xjtu 统一身份认证网关，返回 token 和 gsessionid。
    成功返回 token 和 gsessionid。
    登录失败返回 None,None。

    基于 selenium + firefox 实现登录，需要安装 firefox 以及 geckodriver，
    安装浏览器驱动(yay geckodriver)、安装 python 依赖包(pip install selenium)

    time.sleep(1) 是为了避免页面加载未完成，导致元素定位失败

    - [python使用脚本登录账户(基于selenium+Firefox) winycg 2023-04-05](https://blog.csdn.net/winycg/article/details/129978394)
    - [Python---利用Requests实现每日微信自动打卡 CookiePie 2020-11-14](https://blog.csdn.net/CookiePie/article/details/109698484)
    """
    import base64
    import io

    from PIL import Image
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.firefox.options import Options as FirefoxOptions

    options = FirefoxOptions()
    options.add_argument("--headless")
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    options.set_preference("general.useragent.override", user_agent)
    driver = webdriver.Firefox(options=options)
    token = None
    gsessionid = None
    try:
        driver.get("https://pahw.xjtu.edu.cn/home")  # 要登录的网址，能跳转到 xjtu 的统一身份认证网关都可以
        time.sleep(1)
        btn_login = driver.find_element(By.CLASS_NAME, "login")  # 定位 登录按钮
        btn_login.click()  # 会跳转到统一身份认证网关页面，driver 自动更新
        time.sleep(1)

        name = driver.find_element(
            By.XPATH, "/html/body/div/div[1]/div[2]/div[2]/div[1]/form/input[1]"
        )
        name.send_keys(username)
        # pwd =  driver.find_element(By.CLASS_NAME, "pwd")
        pwd = driver.find_element(
            By.XPATH, "/html/body/div/div[1]/div[2]/div[2]/div[1]/form/input[2]"
        )
        pwd.send_keys(password)
        # 验证码识别 .codeBox 不一定要求输入验证码
        codeBoxs = driver.find_elements(By.CLASS_NAME, "codeBox")
        for codeBox in codeBoxs:
            """
            css 的 display 一般是 none， 要是频繁刷登录就是 block，此时就要求输入验证码
            除了 css 判断，其实可以通过请求来判断
            PaddleOCR 效果也不是那么好，有时候识别不出来；
            tesseract 报错 Empty page!!，网上说分辨率太低了导致的，110x35确实有点小；
            cnocr 测试了一下感觉可以
            """
            display_value = codeBox.value_of_css_property("display")
            if display_value == "block":
                jcaptcha_img = driver.find_element(
                    By.CLASS_NAME, "img_span"
                )  # 验证码图片元素 bs64 编码
                # base64编码的图像数据
                base64_image_data = jcaptcha_img.get_attribute("src")
                image_data = base64_image_data.split(",")[-1]  # 分割字符串以获取纯base64数据
                image_bytes = base64.b64decode(image_data)  # 解码base64数据
                image = Image.open(io.BytesIO(image_bytes))  # 使用Pillow库将二进制数据转换为图像
                # image.save("captcha.png") # 保存图像到文件（可选）
                # 进行OCR识别
                from cnocr import CnOcr

                ocr = CnOcr(
                    det_model_name="naive_det",
                    rec_model_name="number-densenet_lite_136-fc",
                )  # 数字识别模型
                out = ocr.ocr(image)
                if out:
                    code = out[0]["text"]
                    if len(code) == 6:
                        jcaptcha = driver.find_element(By.CLASS_NAME, "text_yan")
                        jcaptcha.send_keys(code)

        btn_login = driver.find_element(By.ID, "account_login")
        time.sleep(1)
        btn_login.click()
        time.sleep(1)
        """
        F12 可知登录后 cookie 里的 JSESSIONID 发生变更，并获得 tokenKey,
        重定向后由 tokenKey 获取到 token，并将 token 存入 local storage
        """
        # get token from local storage
        local_storage = driver.execute_script("return window.localStorage")
        # token = driver.execute_script("return window.localStorage.getItem('_token')") # 浏览器里有效，确实带下划线，代码测试无效
        token = (
            local_storage["token"] if "token" in local_storage else None
        )  # 获取到的 local_storage 的字段名不带下划线
        gsessionid = (
            local_storage["gsessionId"] if "gsessionId" in local_storage else None
        )
        gsessionid = (
            gsessionid.split("_")[-1] if gsessionid else None
        )  # user_token_123-123-123-123-4321
    except Exception as e:
        print("Exception:", repr(e))
    finally:
        driver.quit()  # 关闭浏览器，释放资源
        return token, gsessionid if token and gsessionid else None


def exercise_sign_in(
    token: str,
    jsessionid: str,
    longitude: str = "108.655286",
    latitude: str = "34.238000",
    course_info_id: str = "1759468647346147329",
):
    """
    锻炼过程积分签到。使用 requests 实现 post 请求


    已知返回的 msg 有：
    签到成功！
    距离最近的指定运动地点超过100m，无法打卡
    """
    import requests

    url = "https://ipahw.xjtu.edu.cn/szjy-boot/api/v1/sportActa/signRun"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "content-type": "application/json",
        "token": token,
        "Origin": "https://ipahw.xjtu.edu.cn",
        "DNT": "1",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Referer": "https://ipahw.xjtu.edu.cn/pages/index/hdgl/hdgl_run?courseType=7&signType=1&activityAddress=&courseInfoId="
        + course_info_id,
        "Cookie": "JSESSIONID=" + jsessionid,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua": '"Google Chrome";v="118", "Chromium";v="118", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
    }
    data = {
        "sportType": 2,
        "longitude": longitude,
        "latitude": latitude,
        "courseInfoId": course_info_id,
    }
    response = requests.post(url, headers=headers, json=data)
    ret = response.json()
    if "success" in ret:
        is_success = ret["success"]
        return is_success, ret["msg"]
    return None, "Unknown error"


def exercise_sign_out(token, jsessionid, longitude="108.655286", latitude="34.238000"):
    """
    锻炼过程积分签退。使用 requests 实现 post 请求

    已知返回的 msg 有：
    签退成功！
    你已签退成功,请勿重复签退！
    """
    import requests

    url = "https://ipahw.xjtu.edu.cn/szjy-boot/api/v1/sportActa/signOutTrain"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "content-type": "application/json",
        "token": token,
        "Origin": "https://ipahw.xjtu.edu.cn",
        "DNT": "1",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Referer": "https://ipahw.xjtu.edu.cn/pages/index/hdgl/hdgl_run?courseType=7&signType=2&activityAddress=&courseInfoId=1759468647346147329",
        "Cookie": "JSESSIONID=" + jsessionid,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua": '"Google Chrome";v="118", "Chromium";v="118", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
    }
    data = {
        "longitude": longitude,
        "latitude": latitude,
    }
    response = requests.post(url, headers=headers, json=data)
    ret = response.json()
    if "success" in ret:
        is_success = ret["success"]
        print(ret["msg"])
        return is_success, ret["msg"]
    return None, "Unknown error"


if __name__ == "__main__":
    # 测试
    username = "2177124317"  # 学工号
    password = "password"  # 密码
    token, gsessionid = login_selenium_firefox(username, password)
    print("test login_selenium_firefox. token:", token, " gsessionid:", gsessionid)
    if token and gsessionid:
        time.sleep(random.randint(2, 4))  # 随机等待几秒，避免被识别为爬虫
        is_success, msg = exercise_sign_in(token, gsessionid)
        print("test exercise_sign_in. is_success:", is_success, " msg:", msg)
        time.sleep(random.randint(1888, 3600))  # 锻炼 ing，之后再签退
        token, gsessionid = login_selenium_firefox(
            username, password
        )  # 刷新 token 和 gsessionid
        time.sleep(random.randint(2, 4))
        is_success, msg = exercise_sign_out(token, gsessionid)
        print("test exercise_sign_out. is_success:", is_success, " msg:", msg)
