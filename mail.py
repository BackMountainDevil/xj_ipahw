import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

from config import getConfig


def send_email(
    from_addr=getConfig("SMTP", "SENDER"),
    password=getConfig("SMTP", "PASSWORD"),
    to_addr=getConfig("SMTP", "RECEIVER"),
    subject="ip",
    content="content",
    smtp_server=getConfig("SMTP", "SMTP_SERVER"),
    smtp_port=465,
):
    """send email via smtp

    Args:
        from_addr (str): 发送方邮箱地址
        password (str): 发送方账户授权码，非邮箱密码
        to_addr (str): 收件人邮箱地址
        subject (str): 邮件主题
        content (str): 邮件内容
        smtp_server (str): 发送方smtp服务器
        smtp_port (int, optional): smtp服务端口，默认为 465

    Returns:
        Bool: send succ? True:False
    """
    ret = True
    try:
        msg = MIMEText(content, "plain", "utf-8")
        msg["From"] = formataddr(["Sender", from_addr])
        msg["To"] = formataddr(["Receiver", to_addr])
        msg["Subject"] = subject

        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(from_addr, password)
        server.sendmail(
            from_addr,
            [
                to_addr,
            ],
            msg.as_string(),
        )
        server.quit()
    except Exception:
        ret = False
    return ret


if __name__ == "__main__":
    send_email(content="send email test")
