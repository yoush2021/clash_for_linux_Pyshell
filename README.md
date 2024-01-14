# clash_for_linux_Pyshell
One click deployment of clash core in Linux

获取脚本 get shell
```
wget https://github.com/yoush2021/clash_for_linux_Pyshell/blob/master/clash_config.py
```	

赋权
```shell
chmod +x clash_config.py
```

添加订阅链接
```
./clash_config.py -f 订阅链接
```

替换clash版本(默认内置ARM版链接可跳过该步骤)
```
./clash_config.py -c clash下载链接（默认下载ClashPremium ARM https://downloads.clash.wiki/ClashPremium/）
```

启动 start
```
./clash_config.py 
```

恢复内置clash程序下载链接
```
./clash_config.py default

卸载 remove
```
./clash_config.py remove 
```

帮助 help
```
./clash_config.py -h
```



