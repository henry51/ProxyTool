# -*- coding: utf-8 -*-
'''
Required
- requests 
Info
- author : "huangfs"
- email  : "huangfs@bupt.edu.cn"
- date   : "2016.4.2"
'''

import base64
import requests
import hashlib
import random
import time

class Proxy(object):
    def __init__(self, max_page=1):
        self.max_page = max_page
        self.proxies = []
        self.session = requests.Session()
        self.headers = {
            'Host': 'proxy.peuland.com',
            'Origin': 'https://proxy.peuland.com',
            'Referer': 'https://proxy.peuland.com/proxy_list_by_category.htm',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2692.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            
        }
        self.hostUrl = 'https://proxy.peuland.com'
        self.url = 'https://proxy.peuland.com/proxy/search_proxy.php'
        self.checkUrl = 'http://www.baidu.com'

    def _get_cookies(self):
        response = self.session.get(self.hostUrl,headers = self.headers)
        return self.session.cookies.get_dict()

    def _parse_proxy(self):
        peuland_id = self._get_cookies()['peuland_id']
        m = hashlib.md5()
        m.update(str.encode(peuland_id))
        peuland_md5 = m.hexdigest()
        for i in range(1,self.max_page +1):
            payload = {
                'type': '',
                'country_code': 'CN',
                'is_clusters': '',
                'is_https': '',
                'level_type': 'anonymous',
                'search_type': 'all',
                'page': str(i),
            }
            try:
                r = self.session.post(self.url, data=payload,headers = self.headers, timeout = 10, cookies = {'peuland_md5':peuland_md5,'w_h':'', 'w_w':'', 'w_cd':'', 'w_a_h':'', 'w_a_w':''})
                data = r.json()['data']
                for line in data:
                    rate = int(base64.b64decode(line['time_downloadspeed']))
                    #是否選擇根據自己對代理速度的要求
                    if rate <= 7:
                        continue
                    proxy_type = base64.b64decode(line['type']).decode()
                    ip = base64.b64decode(line['ip']).decode()
                    port = base64.b64decode(line['port']).decode()
                    yield {proxy_type: '{}://{}:{}'.format(proxy_type,ip,port)}

                time.sleep(random.random())
            except Exception as e:
                print (e)
            

    def _check_proxy(self, proxy):
        try:
            r = requests.get(self.checkUrl, proxies =  proxy)
            return r.status_code
        except:
            return 0

    def get_proxy(self):
        for proxy in self._parse_proxy():
            if self._check_proxy(proxy) == 200:
                self.proxies.append(proxy)
        return self.proxies



if __name__ == '__main__':
    ins = Proxy(2)
    print (ins.get_proxy())