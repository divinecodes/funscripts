# -*- coding: utf-8 -*-

"""
dead_bot.py
~~~~~~~~~~~~

Simple model to find dead links in a website

:copyright: (c) 2019 by Divine Sedem Tettey 
:license: Apache2, see LICENSE for more details.
"""

import sys, urllib, time, json
from urllib import request, parse
from urllib.parse import urlparse, urljoin
from urllib.request import Request
from html.parser import HTMLParser
from collections import deque

search_attrs = set(['href','src'])

agents = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

class DeadLinks(HTMLParser): 
    def __init__(self, home): 
        super().__init__()
        self.home = home
        self.checked_links = set()
        self.pages_to_check = deque()
        self.pages_to_check.appendleft(home)
        self.dead_links = {}
        self.crawler()

    def crawler(self): 
        """ function to crawl the pages """
        #while there are still pages to crawl
        while self.pages_to_check: 
            page = self.pages_to_check.pop()

            # send the request using this header
            req = Request(page, headers={'User-Agent': agents})
            try: 
                res = request.urlopen(req)
            except: 
                continue 

            # check to make sure its html that we are bout to parse
            if 'html' in res.headers['content-type']: 
                with res as f: 
                    #reading the html using UTF-8 as encoding 
                    body = f.read().decode('utf-8', errors='ignore')
                    self.feed(body)

        #get current time to name file
        file_name = time.strftime("%Y%m%d%H%M%S")+".json"
        
        #write to json file 
        self.write_result_to_json(file_name, self.dead_links)

    
    def handle_starttag(self, tag, attrs):
        """would handle the start tags in html body"""
        for attr in attrs: 
            if(attr[0] in search_attrs and attr[1] not in self.checked_links): 
                self.checked_links.add(attr[1])
                self.handle_link(attr[1])

    def handle_link(self, link): 
        """ would handle the links """ 
        #check for relative link 
        if not bool(urlparse(link).netloc): 
            #lets fix this, we cant send a request 
            link = urljoin(self.home, link)

            #now lets attempt to send a request,watching out for the http status code 
            try: 
                req = Request(link , headers={'User-Agent': agents})
                status = request.urlopen(req).getcode()
            except urllib.error.HTTPError as err: 
                self.dead_links[link] = err.code
                print(f"HTTPError: {err.code} -  {link}")
            except urllib.error.URLError as err: 
                #self.dead_links[link] = err.reason
                print(f"URLError: {err.reason} -  {link}")
            except: 
                print("Unexpected Error: ", sys.exc_info()[0])
            else: 
                print(f'{status} -{link}')

        if self.home in link: 
            self.pages_to_check.appendleft(link)

    def write_result_to_json(self, file_name, result): 
        f = open(file_name, 'w')
        json_file = json.dumps(result)
        print(f"creating file: {file_name}...")
        print("writing to file...")
        f.write(json_file)
        print('...write to file complete')
        f.close()

DeadLinks(sys.argv[1])
