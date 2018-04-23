import requests

# print(requests.get('http://[FE80::1234:EDDE:1107:115D]/').text)
#
import urllib2

opener = urllib2.build_opener()
print(opener.open('http://[FE80::1234:EDDE:1107:115D]/'), )

# import sys
# import pycurl
# import time
# class Test:
#     def __init__(self):
#         self.contents = ''
#     def body_callback(self, buf):
#         self.contents = self.contents + '{}'.format(buf)
# sys.stderr.write("Testing %sn" % pycurl.version)
# start_time = time.time()
# urls = ['http://[FE80::1234:EDDE:1107:115D]/', 'http://www.baidu.com/']
# url = urls[0]
# t = Test()
# c = pycurl.Curl()
# c.setopt(c.URL, url)
# c.setopt(c.WRITEFUNCTION, t.body_callback)
# c.perform()
# end_time = time.time()
# duration = end_time - start_time
# print(c.getinfo(pycurl.HTTP_CODE), c.getinfo(pycurl.EFFECTIVE_URL))
# c.close()
# print('pycurl takes %s seconds to get %s ' % (duration, url))
# print('lenth of the content is %d' % len(t.contents))