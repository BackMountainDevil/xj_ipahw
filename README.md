# xjtu 自动打卡

注：此方法仅供学习研究之用，经不严谨测试表明，该方法目前已失效，因此予以公开。

目地：自动打卡签到、到时间自动签退。

## 原理

抓包发现定位在前端做，那么可以模拟定位在自动打卡，或者修改签到的数据。

抓包显示每次请求内容都一样，登录类型、用户名、密码密文、验证码。密码密文从代码看是 AES.ECB 加密，就是说公钥都写出来了 '0725@pwdorgopenp'， 验证码是 jcaptcha 生成的数字，页面加载时就生成了，但不一定显示让用户进行输入，目前尝试次数多了就会有，逻辑是登录前发请求（getIsShowJcaptchaCode）检验该用户要不要输入验证码，要的话返回字段的 data 就为真，不需要则为 false

登录逻辑这里用 selenium 实现，其实 refer 有 request 的实现方式

## 运行

安装依赖包

### 简约版

此版本修改 main 函数里面的用户名和密码，然后运行（`python login.py`）即可签到、签退

### 邮件版

此版本在简约版基础上添加日志功能、发邮件功能。创建 `.env` 文件，写入以下内容然后修改

```env
[SMTP]
SENDER = zhangsan@qq.cn
PASSWORD = passWord
RECEIVER = lisi@qq.com
SMTP_SERVER = stmp.qq.cn

[USER]
USERNAME = 2177124317
PASSWORD = passWord

[LOG]
FILENAME = /home/zhangsan/Documents/ipahw/ipahw.log
```

运行方式（`python main.py`）。推荐将此脚本设置为[每日定时任务](https://backmountaindevil.github.io/#/os/de/timeJobScheduler)

# QA
## might not be compatible

具体情况，实测如下所示

```bash
$ python main.py
Problem reading geckodriver versions: error sending request for url (https://raw.githubusercontent.com/SeleniumHQ/selenium/trunk/common/geckodriver/geckodriver-support.json): operation timed out. Using latest geckodriver version
The geckodriver version (0.34.0) detected in PATH at /usr/bin/geckodriver might not be compatible with the detected firefox version (129.0.1); currently, geckodriver 0.35.0 is recommended for firefox 129.*, so it is advised to delete the driver in PATH and retry
```

第一行 error 是连接超时，原因是因为长城防火墙，需要点魔法，但不太影响运行。

第二行的检测版本不匹配，我这里的原因是系统滚动更新浏览器，而浏览器驱动还没更新，更新一下就好了

# refer

[How can you fake geolocation in Firefox? 2017.1.3](https://security.stackexchange.com/questions/147166/how-can-you-fake-geolocation-in-firefox):在火狐浏览器里设置，geo.provider.network.url 默认是 `https://www.googleapis.com/geolocation/v1/geolocate?key=%GOOGLE_LOCATION_SERVICE_API_KEY%`，没找到怎么新加一个 geo.provider.testing to true

[geoclue-mock](https://github.com/inzanity/geoclue-mock):update at 2016

## blog

[创新港体育场馆自动预定 2023-11-10 kezhi](https://kezhi.tech/66f3a0f6.html)

[selenium的webdriver来自动填报每日健康日报 2020-06-01](https://gwyxjtu.github.io/2020/06/01/selenium%E7%9A%84webdriver%E6%9D%A5%E8%87%AA%E5%8A%A8%E5%A1%AB%E6%8A%A5%E6%AF%8F%E6%97%A5%E5%81%A5%E5%BA%B7%E6%97%A5%E6%8A%A5/)

[xjtuportal](https://github.com/openana/xjtuportal):最后更新于 2022 年,A web portal authentication manager for XJTU iHarbor campus network 

[xjtu_lib_bot](https://github.com/gwyxjtu/xjtu_lib_bot):最后更新于 2021 年，西安交通大学图书馆预约抢座位脚本。登录逻辑挖的很好，验证码因为一般不处理所以代码没做处理。吐槽下公钥至少三年没变了 

## 验证码

[cnocr](https://github.com/breezedeus/cnocr)：识别数字验证码

[captcha-tensorflow](https://github.com/JackonYang/captcha-tensorflow):最后更新于 2022 年，4位字符，TensorFlow 2.1

[captcha-recognition](https://github.com/zipzou/captcha-recognition)：最后更新于 2021 年，针对 EasyCaptcha、Kaptcha，PyTorch 1.4.0

[KNN_recognize_captcha](https://github.com/HELL-TO-HEAVEN/KNN_recognize_captcha)：最后更新于 2019 年

[JCaptcha-Solver](https://github.com/ali-sajjad-rizavi/JCaptcha-Solver)：最后更新于 2018 年，使用贝叶斯

[captcha_recognize](https://github.com/PatrickLib/captcha_recognize)：最后更新于 2017 年，针对 EasyCaptcha、Kaptcha，TensorFlow 1.1
