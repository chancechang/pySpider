from bs4 import BeautifulSoup
import requests


def get_proxies_abuyun():
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"
    # 代理隧道验证信息
    proxyUser = 'HR3LY43V4QOU249D'
    proxyPass = 'F89DAEA7A6C85E23'

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies


url='https://music.163.com/weapi/v1/resource/comments/R_SO_4_1313354324?csrf_token='
url='https://music.163.com/weapi/v1/resource/comments/R_SO_4_1313354324?csrf_token='
params: 6n1k3idxu0bOc4/FYOOw0cRcZVFTBsJwQoMh4UljjzCJ9jEuoOuGwIqgqhKhtoCCCrNycFyF502njKg2ADdojGwjLgRAGcQtkClKnaCCN5uNWbkCzVKXlmD7szG7LGG3iVIKcJmh65IWmc4b0X6P/gSDlMaZFWeO2w/zUARjSLSm67lFnew/X60ZwoNCjs5c
encSecKey: 05fea08e299b5681b25772022d7b63467ce2d01bc4b0e56f69eb98370c4c7b12288a6dbd316d0b3ea9ad0d60ea32b346f17bee8e0b4ae1ce95ba5664212b433542a5e04a2d3fe3026f06568da23f72d3e707578da007c0f4220b77a8538056f74b23e3a14f7078ff0d2ad8d0e12f88144151bb12fabf0452ec8e2bcf77868378

params: AKP0bgqlIFVQ9hbWWr4MdsztYa+rRbCmokMv4DbKqzJnGmV5lEQUPyvG8omKfkbl49ZfdghUd8UhyR4/W5iXRsR9N7GamXYKZYo7ckrHo0oaFe1K3H7wVOhWOw8P9i/us4x0TSQRLhwHuqxNAjbz4M1OxAp+pysGc/kjKYNjD1WbS4CCWur1hPAQa+i0Hjqp
encSecKey: 0e326c946dbe7b0b8c0c0bee0e590de9f624bf0437db85fcc869575becbc4450175256165d4234aac6b7dd4897fc53c232279520a154defecc707de81c828983b02d3a3fd1486c8a14881019df83bd00d86b761b10d5d073c76180b994f564c01988b552b81026ee6fa5e277d16f4c42ebe5fdb03678c143f398ec745cb2395b