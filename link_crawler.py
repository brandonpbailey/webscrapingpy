import re
from download import download
from urllib.parse import urljoin
from get_robot_parser import get_robot_parser

#domain = 'http://example.webscraping.com'
def link_crawler(start_url, link_regex, robots_url=None, user_agent='wswp'):
    """Crawl from the given start URL following links matched by link regex"""
    if not robots_url:
        robots_url = '{}/robots.txt'.format(start_url)
    rp = get_robot_parser(robots_url)
    crawl_queue = [start_url]
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        if rp.can_fetch(user_agent, url):
            html = download(url,user_agent=user_agent)
        else:
            print('Blocked by robots.txt')
        if html is None:
            continue
        for link in get_links(html):
            if re.match(link_regex, link):
                abs_link = urljoin(start_url,link)
                if abs_link not in seen:
                    seen.add(abs_link)
                    crawl_queue.append(abs_link)


def get_links(html):
    """Return  a list of links from the html"""
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)["']""", re.IGNORECASE)
    return webpage_regex.findall(html)
