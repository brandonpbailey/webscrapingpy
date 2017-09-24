import requests
from requests.utils import get_encodings_from_content
from codecs import StreamRecoder
import codecs

def download(url, user_agent='wswp', num_retries=2, proxies=None):
    print('Downloading:', url)
    headers = {'User-Agent': user_agent, 'content-encoding':'utf-8'}
    try:
        resp = requests.get(url, headers=headers, proxies=proxies)
        html = resp.text
        #print(get_encodings_from_content(html))
        if resp.status_code >= 400:
            print('Download error:', resp.text)
            html = None
            if num_retries and 500 <= resp.status_code < 600:
                return download(url, num_retries - 1)
        return html
    except requests.exceptions.RequestException as e:
        print('Download error:', e.reason)
        html = None


