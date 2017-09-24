from urllib.parse import urlparse
import time

class Throttle:
    """Add a delay between downloads to the same domain"""
    def __init__(self, delay):
        self.delay = delay # Amount of delay between doanlods for each domain
        self.domain = {} #timestamp of when a domain was last accessed

    def wait(self, url):
        domain = urlparse(url).netloc #netloc gets the domain name
        last_accessed = self.domain.get(domain) #.get checks against the self.domain to see if there it has been set.

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (time.time()-last_accessed)
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domain[domain] = time.time()
