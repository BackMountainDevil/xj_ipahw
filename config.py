import configparser


def getConfig(section, option, configFile=".env"):
    # use configparser read config from .env
    cfg = configparser.RawConfigParser()  # 创建配置文件对象
    cfg.optionxform = lambda option: option  # 重载键值存储时不重置为小写
    cfg.read(configFile, encoding="utf-8")  # 读取配置文件，没有就创建
    if not cfg.has_section(section):
        cfg.add_section(section)
        with open(configFile, "w") as configfile:
            cfg.write(configfile)
    if cfg.has_option(section, option):
        return cfg.get(section, option)
    return None


if __name__ == "__main__":
    print(getConfig("SMTP", "RECEIVER"))
    print(getConfig("LOG", "FILENAME"))
