#!env python
#coding=utf-8
# 
# Author:       liaoxinxi@nsfocus.com
# 
# Created Time: Thu 14 May 2015 04:26:57 AM EDT
# 
# FileName:     is_proxy_ok.py
# 
# Description:  
# 
# ChangeLog:
import sys
import urllib2
import optparse
import re

def get_proxys(file_name):
    """这里的文件内容可以是从cn-proxy.com复制过来的数据"""
    proxys = []
    ip_reg = re.compile(r'^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', re.I)
    try:
        with open(file_name, 'r') as fd_proxy:
            for line in fd_proxy:
                if line and line.strip():
                    print 'line',line.strip()
                    if ip_reg.match(line.strip()):
                        ip, port = line.strip().split()[0], line.strip().split()[1]
                        proxy = '%s:%s' %(ip, port)
                        print 'proxy',proxy
                        if test_connection(proxy):
                            proxys.append(proxy)
    except Exception,e:
        print 'error',e

    return proxys

def test_connection(proxy):
    url = 'http://www.baidu.com'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent':user_agent}
    host_type = 'http'
    if '443' in proxy:
        host_type = 'https'
    try:
        req = urllib2.Request(url,headers=headers)
        req.set_proxy(proxy, host_type)
        response = urllib2.urlopen(req)
        if response and response.getcode() == 200:
            return True
        else:
            return False
    except Exception,e:
        print 'get proxy:',proxy,e
        return False


def write_file(src, dst):
    proxys = get_proxys(src)
    print 'proxys',proxys
    if proxys:
        try:
            with open(dst, 'w') as fd:
                for line in proxys:
                    fd.write(line+"\n")
        except Exception,e:
            print 'no permission',e

def usage():
    print "示例:python is_proxy_ok.py -s src_file -d dst_file src_file代表要读取的proxy文件，\
            同时src_file中ip和端口以空格分开,dst_file表示要有效proxy存入的文件名"
def main():
    parse = optparse.OptionParser()
    parse.add_option('-s', '--src', dest='src_file', help='要测试的文件')
    parse.add_option('-d', '--dst', dest='dst_file', help='存取结果文件',default='proxy_ok.txt')
#    parse.add_option('-h', '--help', dest='help', help='示例:python is_proxy_ok.py -s src_file -d dst_file')
    (options, args) = parse.parse_args()
    if not options.src_file :
        usage()
        sys.exit()
    write_file(options.src_file, options.dst_file)

if __name__ == '__main__':
    main()
