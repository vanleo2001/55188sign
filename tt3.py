# -*- coding=gb2312 -*-

import sys
import os
import cPickle as p
import requests
import re

def login_with_cookies():
        pass

def save_cookies(cookiesFile,cookies):
        try:
                with open(cookiesFile,'w') as f:
                        p.dump(requests.utils.dict_from_cookiejar(cookies),f)
                        print 'Saved'
                        f.close()
        except:
                print 'Save cookies failed', sys.exc_info()[0]
                sys.exit(99)

def load_cookies(cookiesFile):
        try:
                with open (cookiesFile,'r') as f:
                        cookies=requests.utils.cookiejar_from_dict(p.load(f))
                        f.close()
        except:
                cookies=''
        return cookies

def login(cookiesFile,loginUrl,verfyUrl,keyWord,username,password):
        '''Login to a website with the given username and password'''
        http_headers={"Host": "www.55188.com",
        	'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            'DNT': '1',
            "Referer": "http://www.55188.com/logging.php?action=login"}
        session = requests.session()
        session.headers.update(http_headers)
        while True:
                cookies = load_cookies(cookiesFile)
                if cookies != '':
                        session.cookies.update(cookies)
                        print 'Session getted'
                        #verfy if the cookies work, if not work del it and rebuild
                        htmlVerfy = session.get(verfyUrl)
                        if re.findall(keyWord,htmlVerfy.content) != None:
                                return True
                        else:
                                return False
                else:
                        print 'Did not get cookies, begin to get and save it'
                        htmlLogin = session.post(loginUrl,data={
                        	'formhash':'aabacfd3',
                        	'referer':'http://www.55188.com/forum-68-1.html',
                        	"username":username,
                        	"password":password,
                        	'questionid':0,
                        	'answer':'',
                        	'cookietime':'315360000',
                        	'loginmode':'',
							'styleid':'',
                        	'loginsubmit':'true'})
                        save_cookies (cookiesFile,session.cookies)

if __name__ == '__main__':
        konotes_org_cookies='konotes.dat'
        konotes_org_login_info = { 'cookiesFile':konotes_org_cookies,
        'loginUrl':'http://www.55188.com/logging.php?action=login',
        'verfyUrl':'http://www.55188.com/addsign.php',
        'keyWord':'asswdee',
        'username':'your name',
        'password':'your password'
        }

        if login(konotes_org_login_info['cookiesFile'],konotes_org_login_info['loginUrl'],konotes_org_login_info['verfyUrl'],konotes_org_login_info['keyWord'],konotes_org_login_info['username'],konotes_org_login_info['password']):
                print 'Login Ok'
        else:
                print 'Login failed'
