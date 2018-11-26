import urllib3
import time
import random
import urllib.request
from lxml import etree
import datetime


class MasterProxy(object):

    def __init__(self, url, home, proxy_max=20, restart_min=5):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        }
        self.__url = url
        self.__home = home
        self.__proxy_max = proxy_max
        self.__restart_min = restart_min
        self.__http = urllib3.PoolManager(headers=self.headers)
        self.ip_pool = self.init_ip_pool()

    """
        名称：下载器
        功能：下载对应网页和子网页的内容，将信息传给解析器处理
    """
    def ip_download(self, proxy, url):
        proxy.spider_sleep()
        re = self.__http.request('GET', url)
        content = re.data.lower().decode('utf-8')
        html = etree.HTML(content)
        if proxy.ip_xpath(proxy, html):
            try:
                next_url = html.xpath('//a[@class="next_page"]/@href')[0]
            except Exception:
                next_url = None
            if next_url:
                proxy.ip_download(proxy, self.__home+next_url)
        return None

    """
        名称：解析器
        功能：接收下载器下载的页面信息，将页面中的ip、端口和类型解析出来，调用校验器验证代理ip是否有效
    """
    def ip_xpath(self, proxy, html):
        ips = html.xpath('//td[2]/text()')
        ports = html.xpath('//td[3]/text()')
        types = html.xpath('//td[6]/text()')
        for i, ip in enumerate(ips):
            if proxy.ip_pool_length() >= self.__proxy_max:
                return False
            else:
                if ip and ports[i] and types[i]:
                    proxy.ip_check(proxy, types[i] + '://' + ip + ':' + ports[i])
        return True

    """
        名称：校验器
        功能：接收解析器或定时验证发送的ip信息，确认代理ip是否可用
    """
    def ip_check(self, proxy, ip):
        url = "https://www.baidu.com"
        if ip:
            try:
                ip_detail = ip.split('://')
                proxy_ip = {ip_detail[0]: ip_detail[1]}
                proxy_support = urllib.request.ProxyHandler(proxy_ip)
                opener = urllib.request.build_opener(proxy_support)
                opener.addheaders = [("User-Agent",
                                      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                                      " Chrome/60.0.3112.113 Safari/537.36")]
                urllib.request.install_opener(opener)
                re = urllib.request.urlopen(url, timeout=3)
                if re.status >= 200 or re.status <= 300:
                    proxy.ip_proxy_saver(ip)
                else:
                    proxy.ip_proxy_deleter(ip)
            except Exception as a:
                print('[ERROR] Ip:', ip, '   ', a)
                proxy.ip_proxy_deleter(ip)

    """
        名称：主流程
        功能：1.判断ip池是否小于池容量最小值，若是则启动下载器，爬去代理ip
              2.每隔20秒校验一次ip池, 也可以自定义
    """
    def proxy_main(self, proxy, check_second=20):
        while 1:
            if proxy.ip_pool_length() <= self.__restart_min:
                print('  [INFO] Ip Proxy start : ', datetime.datetime.now())
                proxy.ip_download(proxy, self.__url)
            else:
                if datetime.datetime.now().second % check_second == 0:
                    print('  [INFO] Check Ip Pool : ', datetime.datetime.now())
                    now_ip_pool = proxy.get_ip_pool
                    for ip in now_ip_pool:
                        proxy.ip_check(proxy, ip)
                    print('  [INFO] Ip Pool length: ', len(self.ip_pool))

    '''获取ip池'''
    def get_ip_pool(self):
        return self.ip_pool.copy()

    '''获取ip池长度'''
    def ip_pool_length(self):
        return len(self.ip_pool)

    '''将ip插入线程池'''
    def ip_proxy_saver(self, ip):
        self.ip_pool.add(ip)

    '''从线程池中删除某个ip'''
    def ip_proxy_deleter(self, ip):
        self.ip_pool.discard(ip)

    #随机睡眠或按照制定秒数睡眠
    def spider_sleep(self, second=random.randint(5, 20)):
        time.sleep(second)

    #容器初始化
    def init_ip_pool(self):
        return set()


if __name__ == "__main__":
    xiciProxy = MasterProxy('http://www.xicidaili.com/nn/', 'http://www.xicidaili.com')
    xiciProxy.proxy_main(xiciProxy)


