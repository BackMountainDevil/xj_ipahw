# Problem reading geckodriver versions: error sending request for url

# 运行过程

```bash
$ cd /home/mifen/Documents/code/xj_ipahw
$ conda activate 310
(310) $ python main.py &> crontab.log
```

# 异常日志

crontab.log 内容

    Problem reading geckodriver versions: error sending request for url (https://raw.githubusercontent.com/SeleniumHQ/selenium/trunk/common/geckodriver/geckodriver-support.json): operation timed out. Using latest geckodriver version
    Exception managing firefox: error sending request for url (https://github.com/mozilla/geckodriver/releases/latest): error trying to connect: tcp connect error: Operation timed out (os error 110)
    INFO: 签到成功，is_success: True, msg: 签到成功！. File "/home/mifen/Documents/code/xj_ipahw/main.py", line:19
    INFO: 签退成功，is_success: True, msg: 签退成功！. File "/home/mifen/Documents/code/xj_ipahw/main.py", line:35
    签退成功！

前两行出现了个异常，这是之前没有观察到的。意思是从远程文件读取版本失败了，大概率是因为防火墙的缘故。好在最后代码运行是没有问题的。

# version info

- os Linux hp 6.6.27-1-lts #1 SMP PREEMPT_DYNAMIC Sat, 13 Apr 2024 11:50:59 +0000 x86_64 GNU/Linux
- firefox 125.0.1-1
- geckodriver 0.34.0-1
- Python 3.10.13
- selenium 4.19.0

# refer

[ [🐛 Bug]: 'code': 65, 'message': 'error sending request for url (https://msedgedriver.azureedge.net/LATEST_RELEASE_116_WINDOWS): error trying to connect: tls handshake eof', 'driver_path': 'browser_path':"') Unable to obtain driver for microsoftedge using selenium manager., #12610 ](https://github.com/SeleniumHQ/selenium/issues/12610)：也是网络连接问题，提问的人不继续交流，问题关闭了

[ [🐛 Bug]: ERROR error sending request for url (https://chromedriver.storage.googleapis.com/LATEST_RELEASE_108): error trying to connect: invalid peer certificate contents: invalid peer certificate: UnknownIssuer #11406 ](https://github.com/SeleniumHQ/selenium/issues/11406)：升级版本后修复
