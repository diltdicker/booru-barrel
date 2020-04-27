import os
import shutil
import json
import logging
from os import path
from pathlib import Path

CFG_DIR = '.barrel'
CFG = 'settings.json'
KIVY = '1.11.1'


class Config():

    def __init__(self):
        self.home = path.expanduser('~')
        self.cfg_dir = path.join(self.home, CFG_DIR)
        self.cfg_file = path.join(self.cfg_dir, CFG)
        self.logger = logging.getLogger('booru_barrel')
        if not path.exists(self.cfg_dir) and not path.exists(self.cfg_file):
            os.makedirs(self.cfg_dir)
            shutil.copyfile(path.join(Path(__file__).parent, 'default.json'), self.cfg_file)

    def wizard(self):
        src_cfg = self.load_cfg()
        print('-- global settings --')
        src_cfg.update({'global': self.global_wizard(src_cfg['global'])})
        print('-- source settings --')
        src_cfg.update({'sources': self.source_wizard(src_cfg['sources'])})
        
        json.dump(src_cfg, open(self.cfg_file, 'w'))

    def list_sources(self) -> list:
        return [src for src in self.load_cfg()['sources']]

    def load_cfg(self) -> dict:
        return json.load(open(self.cfg_file), encoding='utf-8')

    def global_wizard(self, src_cfg: dict) -> dict:
        
        def max_size() -> dict:
            print('max height and size for images. '\
            'images downloaded will be scaled down to fit criteria')
            max_height = input('max height (deafult: no max height): ')
            try:
                max_height = int(str(max_height).strip())
            except:
                max_height = None
            max_width = input('max width (deafult: no max width): ')
            try:
                max_width = int(str(max_width).strip())
            except:
                max_width = None
            
            return {
                'max_height': max_height,
                'max_width': max_width
            }

        def default_src(src):
            new_src = str(input('set the default source (default: {}): '.format(src))).strip()
            if new_src == '':
                return {'default_source': src}
            else:
                return {'default_source': new_src}

        src_cfg.update(max_size())
        src_cfg.update(default_src(src_cfg['default_source']))

        return src_cfg

    def source_wizard(self, src_cfg: dict) -> dict:

        def add_param() -> dict:
            param_key = input('enter param key: ')
            param_value = input('enter param value: ')
            return {param_key: param_value}

        def mod_params(params: dict) -> dict:
            print(params)
            print('to delete param input DELETE')
            for param in params:
                new_param_val = str(input('change value of {0} (default: {1}): '.format(param, params[param]))).strip()
                if new_param_val == 'DELETE':
                    params.pop(param)
                elif new_param_val != '':
                    params.update({param: new_param_val})

            while True:
                add_yn = input('add query param to searches (y/N): ')
                if add_yn == 'y':
                    params.update(add_param())
                else:
                    break
            return params

        def mod_src(src: dict):
            for item in src:
                
                if item == 'params':
                    src.update({'params': mod_params(src['params'])})

                else:
                    new_item = input('update {0} (default: {1}): '.format(item, src[item]))
                    if new_item != '':
                        src.update({item: new_item})
            return src

        def add_source() -> dict:
            source_key = input('name of source: ')
            source_url = input('url of source: ')
            source_type = input('backend type of source (for searches): ')

            params = {}
            while True:
                add_yn = input('add query param to searches (y/N): ')
                if add_yn == 'y':
                    params.update(add_param())
                else:
                    break
            new_src = {
                source_key: {
                    'url': source_url,
                    'type': source_type,
                    'params': params
                }
            }
            return new_src

        for source in src_cfg:
            print('-- {} --'.format(source))
            src_cfg.update({source: mod_src(src_cfg[source])})

        while True:
            source_add_yn = input('add a new source (y/N):')
            if source_add_yn == 'y':
                src_cfg.update(add_source())
            else:
                break

        return src_cfg

    
