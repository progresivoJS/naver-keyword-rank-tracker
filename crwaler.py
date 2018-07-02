import os.path
import urllib
import requests
import time
from bs4 import BeautifulSoup

SITE_URL = "http://www.xn--od1bu1t7pcgwb.net/"
BLOG_ID = 'inja0391'
DELAY = 2

BLOG_KEYWORD_PRINT_FORMAT = """------------------------------------
{} 키워드 - 블로그검색
------------------------------------"""

INTEGRATED_KEYWORD_PRINT_FORMAT = """------------------------------------
{} 키워드 - 통합검색
------------------------------------"""

BLOG_RESULT_PRINT_FORMAT = """
RANK : {}등
제목 : {}
"""

SITE_RESULT_PRINT_FORMAT = """
RANK : {}등
제목 : {} - 사이트
"""


THERE_IS_NO_RESULT = "1페이지 내에 결과 값이 없습니다."


def blog_search(blog_id, query):
    ret = ""
    search_url = "https://m.search.naver.com/search.naver?where=m_blog&sm=mtb_jum&query={}".format(
        query)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Android; Mobile; rv:13.0) Gecko/13.0 Firefox/13.0'}
    response = requests.get(search_url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    blogs = soup.find(class_='lst_total').find_all('a')
    titles = soup.find(class_='lst_total').find_all(class_='total_tit')

    ret += BLOG_KEYWORD_PRINT_FORMAT.format(query)
    count = 0
    for index, blog in enumerate(blogs):
        if blog_id in blog['href']:
            count += 1
            ret += BLOG_RESULT_PRINT_FORMAT.format(index+1, titles[index].text)
    if count == 0:
        ret += THERE_IS_NO_RESULT
    return ret


def integrated_search(site_url, blog_id, query):
    ret = ""
    
    search_url = "https://m.search.naver.com/search.naver?query={}&where=m&sm=mtp_hty".format(
        query)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Android; Mobile; rv:13.0) Gecko/13.0 Firefox/13.0'}
    response = requests.get(search_url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find(class_='sp_ntotal').find(
        'ul', class_='lst_total').find_all('a', class_='api_txt_lines total_tit')

    count = 0
    ret += INTEGRATED_KEYWORD_PRINT_FORMAT.format(query)
    for index, result in enumerate(results):
        if site_url in result['href']:
            title = result.text
            ret += SITE_RESULT_PRINT_FORMAT.format(index+1, title)
            count += 1
        if blog_id in result['href']:
            title = result.text
            ret += BLOG_RESULT_PRINT_FORMAT.format(index+1, title)
            count += 1
    if count == 0:
        ret += THERE_IS_NO_RESULT
    
    return ret


query_list = [
    '양산누수',
    '김해누수',
    '부산누수',
    '기장누수'
]

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'result.txt')

with open(filename, 'w') as f:
    for query in query_list:
        f.write(integrated_search(SITE_URL, BLOG_ID, query))
        f.write(blog_search(BLOG_ID, query))
        f.write('\n\n')
        time.sleep(DELAY)