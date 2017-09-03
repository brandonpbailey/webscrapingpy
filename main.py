import crawl_site
from link_crawler import link_crawler


domain = 'http://example.webscraping.com/'
url = domain + 'places/default/sitemap.xml'

#crawl_site('http://example.webscraping.com/places/default/view/-')
link_crawler('http://example.webscraping.com/places/default','/places/default/(index|view)/', user_agent='BadCrawler')