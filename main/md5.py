import hashlib
from config.settings import MD5_SALT


def get_md5(username, str):
    str = username + str + MD5_SALT
    md5 = hashlib.md5()
    md5.update(str.encode("utf-8"))
    return md5.hexdigest()  # 返回加密后的密文


if __name__ == '__main__':
    print(get_md5("root", "123456"))
