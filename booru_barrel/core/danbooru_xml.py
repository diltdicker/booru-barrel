import os
import requests
import urllib.request as urlreq
from xml.etree import ElementTree
from booru_barrel.core import Page, Post

URL_TAG = 'file-url'
BATCH_LIMIT = 200 * 1000

class DanPage(Page):

    def __init__(self, url: str, params: dict, tags: list, max_imgs: int =None, 
    wait: float =None, resize: tuple =None, output: str =None):
        super().__init__()
        self.count = 0
        self.url = url
        self.tags = tags
        self.params = params
        self.max_imgs = max_imgs
        self.wait = wait
        self.resize = resize
        self.before = BATCH_LIMIT
        self.page = 1
        self.threads = 1
        if output is not None:
            self.output = os.path.abspath(output)
            os.makedirs(self.output, exist_ok=True)
        else:
            self.output = None

    @staticmethod
    def build_url(url: str, params: dict, tags: list, page:int, limit:int =1000) -> str:
        if not url.endswith('/'):
            url += '/'
        page_url = url + 'posts.xml' + '?page={}'.format(page) + '&limit={}'.format(limit)
        for param in params:
            if params[param] is not None:
                page_url += '&{0}={1}'.format(param, params[param])
        if tags != []:
            page_url += '&tags=' + '%20'.join(tags)
        return page_url  

    def get_images(self, url) -> list:
        root = ElementTree.fromstring(requests.request('GET', url).text)
        return [url.text for url in root.iter(URL_TAG)]
    
    def next(self) -> bool:
        img_set = self.get_images(self.build_url(self.url, self.params, self.tags, self.page))
        if self.max_imgs is not None:
                count_diff = self.max_imgs - self.count
                img_set = img_set[:count_diff]
        
        for url in img_set:
            self.count  += 1
            if self.output is not None:
                DanPost(url, self.output).download(self.resize)
            else:
                print(url)
        
        if img_set == [] or (self.max_imgs is not None and self.count >= self.max_imgs):
            return False
        else:
            self.page += 1
            return True


class DanPost(Post):
    def __init__(self, url: str, output: str):
        super().__init__()
        self.url = url
        self.output = output

    def download(self, resize=None):
        file_name = self.url.split('/')[-1]
        file_path = os.path.join(self.output, file_name)
        if not os.path.exists(file_path):
            urlreq.urlretrieve(self.url, file_path)

PageClass = DanPage