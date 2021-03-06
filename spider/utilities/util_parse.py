# _*_ coding: utf-8 _*_

"""
util_parse.py by xianhu
"""

import re
import urllib.parse

__all__ = [
    "get_string_num",
    "get_string_strip",
    "get_url_legal",
    "get_url_params",
]


def get_string_num(string, base=None, only_num=True):
    """
    get a float number from a string, if base isn't None, K means (base * B), M means (base * K), ...
    """
    string_temp = get_string_strip(string.upper().replace(",", ""), replace_char="")
    string_re = re.search(r"(?P<num>\d+(\.\d+)?)(?P<param>.*?)$", string_temp, flags=re.IGNORECASE)
    if not string_re:
        return 0.0
    num, param = float(string_re.group("num")), string_re.group("param")
    if only_num:
        return num
    if param.find("兆") >= 0:
        num *= 10000000000000
    if param.find("亿") >= 0:
        num *= 100000000
    if param.find("万") >= 0:
        num *= 10000
    if param.find("千") >= 0:
        num *= 1000
    if param.find("百") >= 0:
        num *= 100
    if param.find("十") >= 0:
        num *= 10
    if param.find("%") >= 0:
        num /= 100
    if base:
        if param.find("K") >= 0:
            num *= base
        if param.find("M") >= 0:
            num *= base * base
        if param.find("G") >= 0:
            num *= base * base * base
        if param.find("T") >= 0:
            num *= base * base * base * base
    return num


def get_string_strip(string, replace_char=" "):
    """
    get a string which striped \t, \r, \n from a string, also change None to ""
    """
    return re.sub(r"\s+", replace_char, string, flags=re.IGNORECASE).strip() if string else ""


def get_url_legal(url, base_url, encoding=None):
    """
    get a legal url from a url, based on base_url
    """
    url_join = urllib.parse.urljoin(base_url, url, allow_fragments=True)
    return urllib.parse.quote(url_join, safe="%/:=&?~#+!$,;'@()*[]|", encoding=encoding)


def get_url_params(url, keep_blank_value=False, encoding="utf-8"):
    """
    get main_part(a string) and query_part(a dictionary) from a url
    """
    url_frags = urllib.parse.urlparse(url, allow_fragments=True)
    main_part = urllib.parse.urlunparse((url_frags.scheme, url_frags.netloc, url_frags.path, url_frags.params, "", ""))
    query_part = urllib.parse.parse_qs(url_frags.query, keep_blank_values=keep_blank_value, encoding=encoding)
    return main_part, query_part
