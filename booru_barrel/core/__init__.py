import abc
import shutil
import importlib
from PIL import Image
from booru_barrel.cfg import Config

class Runner():

    def __init__(self, source: str, tags: list, max_imgs: int, wait: float, output: str):
        self.tags = tags
        self.max_imgs = max_imgs
        self.wait = wait
        self.source = source
        self.cfg = Config().load_cfg()
        self.output = output

    def run(self):
        if self.source is None:
            self.source = self.cfg['global']['default_source']
        
        height = self.cfg['global']['max_height']
        width = self.cfg['global']['max_width']
        if width is None and height is None:
            resize = None
        else:
            resize = (width, height)

        self.source_type = '.' + self.cfg['sources'][self.source]['type']
        self.url = self.cfg['sources'][self.source]['url']
        self.params = self.cfg['sources'][self.source]['params']
        self.core = importlib.import_module(self.source_type, 'booru_barrel.core')
        page = self.core.PageClass(self.url, self.params, self.tags, self.max_imgs, self.wait, resize, self.output)
        while page.next():
            pass

class Page(abc.ABC):
    
    def __init__(self):
        self.logger = Config().logger
        self.count = 0

    @abc.abstractclassmethod
    def next(self) -> list:
        pass

class Post(abc.ABC):
    
    def __init__(self):
        self.logger = Config().logger
        self.resizer = Resizer()

    @abc.abstractmethod
    def download(self, resize: tuple =None):
        pass

class Resizer():

    @staticmethod
    def get_sizes(sizes: tuple, img_sizes: tuple) -> tuple:
        if sizes[0] is not None:
            ratio_w = sizes[0] / img_sizes[0]
        else:
            ratio_w = 1.0
        if sizes[1] is not None:
            ratio_h = sizes[1] / img_sizes[1]
        else:
            ratio_h = 1.0
        if ratio_w >= 1 and ratio_h >= 1:
            return None
        else:
            ratio = min(ratio_h, ratio_w)
            return (round(img_sizes[0] * ratio), round(img_sizes[1] * ratio))

    @staticmethod
    def resize(img_path: str, resize: tuple):
        img = Image.open(img_path)
        resize = get_sizes(resize, img.size)
        if resize is None:
            img.close()
        else:
            img.resize(resize, Image.ANTIALIAS)
            img.save(img_path)
            img.close()
        
