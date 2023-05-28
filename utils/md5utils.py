import hashlib


def get_md5_from_str(data_str):
    """
    获取字符串的md5值
    :param data_str:
    :return:
    """

    return hashlib.md5(data_str.encode(encoding='utf-8')).hexdigest()  # 返回摘要，作为十六进制数据字符串值
