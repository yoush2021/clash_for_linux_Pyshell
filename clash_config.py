#!/usr/bin/env python3
# encoding：utf-8
#@author: yoush
#@contact: yoush2021@163.com
#@file：clash_config.py
#@time: 2024.01.14
#@desc: 私用脚本，不可商业


import os,time,shutil,json,sys


str_time = time.strftime("%Y%m%d%H%M%S",time.localtime()) # time string
CLASH_LINK = 'https://downloads.clash.wiki/ClashPremium/clash-linux-arm64-2023.08.17.gz'

# 链接配置文件生产及查询函数
def config_json(action_type,clash_link=CLASH_LINK,config_link='url'):
	if "set" == action_type :
		data = {'clash':clash_link,'config':config_link}
		with open(user_path()+'/.config/clash/links_config.json','w',encoding='utf-8') as f:
			f.write(json.dumps(data,sort_keys=True,indent=1))
	elif "get" == action_type :
		try:
			with open(user_path()+"/.config/clash/links_config.json",'r',encoding='utf-8') as f:
				return json.loads(f.read())
		except FileNotFoundError:
			data = {'clash':CLASH_LINK,'config':'url'}
			return data

# 获取配置文件 需要传入下载链接
def down_file(f_type,link):
	try:
		if f_type == "clash" : # 下载clash核心
			clash_down = "wget {} -P /tmp/clash/".format(link)
			os.system(clash_down)
			for i in os.listdir('/tmp/clash/'):
				if 'tar.gz' in i and 'clash' in i or 'Clash' in i:
					str_temp = "tar zxf {} ".format("/tmp/clash/"+i) 
					str_temp2 = "ls /tmp/clash | grep clash-linux | grep -v 'tar.gz' | xargs -I {} mv /tmp/clash/{} /usr/bin/clash"
					os.system(str_temp)
					os.system(str_temp2)
				elif '.gz' in i and 'clash' in i or 'Clash' in i:
					str_temp = "gunzip {} ".format("/tmp/clash/"+i) 
					str_temp2 = "ls /tmp/clash | grep clash-linux | grep -v '.gz' | xargs -I {} mv /tmp/clash/{} /usr/bin/clash"
					os.system(str_temp)
					os.system(str_temp2)
				elif '.zip' in i and 'clash' in i or 'Clash' in i:
					str_temp = "unzip {} ".format("/tmp/clash/"+i) 
					str_temp2 = "ls /tmp/clash | grep clash-linux | grep -v '.zip' | xargs -I {} mv /tmp/clash/{} /usr/bin/clash"
					os.system(str_temp)
					os.system(str_temp2)

				os.chmod("/usr/bin/clash",73) # 赋权
				shutil.rmtree('/tmp/clash') # 删除临时文件夹
		elif f_type == "config" : # 下载订阅文件
			config_down = "wget {} -O ~/.config/clash/config_{}.yaml".format(link,str_time) # create download link
			os.system(config_down) #download file
	except:
		print('下载出错，请检查网络和下载链接如无问题请重试！\nDownload error, please check the network and download link. If there are no issues, please try again!')
		exit()

def update_yaml(file,k,v):
	update_str = "sed -i 's#{}:.*#{}: {}#g' {}".format(k,k,v,file)
	os.system(update_str)

def user_path():
	path = os.popen('cd ~ && pwd ').read().strip()
	return path

def check_dir():
	path = user_path()
	if not os.path.exists(path+"/.config/clash/"):
		os.mkdir(path+"/.config/clash/")
	if not os.path.exists('/tmp/clash/'):
		os.mkdir('/tmp/clash/')

def check_file():
	path = user_path()
	check_dir()
	if not os.path.exists('/usr/bin/clash'):
		down_file('clash',config_json('get')['clash'])

def del_file(file_dir,file_list):
	for i in file_list:
		if i != "config_{}.yaml".format(str_time):
			del_f = 'rm -rf {}{}'.format(file_dir,i)
			os.system(del_f)
def enable_clash():
	flag = 0 # =0 不操作自启 =1 开启自启动
	if not os.path.exists("/usr/lib/systemd/system/clash.service"):	
		os.system("touch /usr/lib/systemd/system/clash.service")
		flag = 1
	with open('/usr/lib/systemd/system/clash.service','w',encoding='utf-8') as f:
		str_temp = "[Unit] \n\
Description=clash server \n\
After=network.target \n\
\n\
[Service] \n\
ExecStart=/usr/bin/clash -f {}/.config/clash/config_{}.yaml \n\
\n\
[Install] \n\
WantedBy=multi-user.target \n\
\n".format(user_path(),str_time)
		f.write(str_temp)
	if flag == 1 :
		os.system('sudo systemctl enable /usr/lib/systemd/system/clash.service')
	os.system('systemctl daemon-reload')
	os.system('systemctl start clash.service')	
	print('请打开url http://clash.razord.top 输入服务器地址即可')

def start_clash():
	# 先关闭旧的线程
	str_kill = "ps -ef | grep '/usr/bin/clash' | grep -v grep | awk '{print $2}' | xargs kill > /dev/null 2>&1 &"
	os.system(str_kill)
	# 启动clash
	enable_clash()

def argv():
	path = user_path()
	check_dir()
	if sys.argv[1] == '-h' or sys.argv[1] == '-H':
		print('./config_clash 订阅链接(Subscription link) 或 \n./config_clash 订阅链接 clash核心程序下载链接')
		exit()
	if sys.argv[1] == '-f' or sys.argv[1] == '-F':
		try:
			config_json('set',config_link=sys.argv[2],clash_link=config_json('get')['clash'])
			print('订阅链接更新成功！ Subscription link updated successfully!')
		except IndexError:
			print('未检测到订阅链接，程序退出！  Subscription link not detected, program exits!')
		exit()

	if sys.argv[1] == '-c' or sys.argv[1] == '-c':
		try:
			if sys.argv[2] == 'default' :
				config_json('set',config_link=config_json('get')['config'])
				print('核心程序链接以恢复默认!  The core program link has been restored to default!')
				exit()
			config_json('set',clash_link=sys.argv[2],config_link=config_json('get')['config'])
			print('核心程序链接更新成功!  Core program link updated successfully!')
		except IndexError:
			print('未检测到核心程序链接，程序退出！  No core program link detected, program exits!')
		exit()
	if sys.argv[1] == 'remove' or sys.argv[1] == 'REMOVE':
		os.system("rm /usr/bin/clash /usr/lib/systemd/system/clash.service {}/.config/clash/ -rf".format(path))
		os.system("sudo systemctl stop clash.service && sudo systemctl disable clash.service && sudo systemctl daemon-reload ")
		print('卸载完成！ Uninstall Complete!')
		exit()
def main():
	f_list = []
	check_file() # 检测关键文件是否存在
	config_link = config_json('get')
	if config_json('get')['config'] == "url" :
		print('请先配置订阅链接!  Please configure the subscription link first!')
		exit()
	else:
		print('正在更新下载配置文件！')
		down_file('config',config_json('get')['config']) # 更新config
	f_dir = user_path() + '/.config/clash/config_{}.yaml'.format(str_time)
	update_yaml(f_dir,'allow-lan',True) # 开启局域网代理
	for f in sorted(os.listdir(user_path()+"/.config/clash/")): #config文件排序后将其加入列表，除最新的外将旧的删除
		if 'config_' in f:
			f_list.append(f)
	del_file(user_path()  + '/.config/clash/',f_list) # 调用删除旧配置文件
	start_clash()

if (__name__ == '__main__'):
	if len(sys.argv) != 1 :
		argv()
	main()
