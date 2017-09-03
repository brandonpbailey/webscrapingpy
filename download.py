import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError

def download(url, user_agent='wswp', num_retries=2, charset='utf-8'): # We had to update the character encoding to utilize regular expressions with the website response.
    print('Downloading:', url)
    request = urllib.request.Request(url)
    request.add_header('User-agent', user_agent)
    try:
        resp = urllib.request.urlopen(request)
        cs = resp.headers.get_content_charset()
        print (cs)
        if not cs:
            cs = charset
        html = resp.read().decode(cs)
    except (URLError, HTTPError,ContentTooShortError) as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                print (num_retries)
                return download(url,num_retries - 1)

    return html