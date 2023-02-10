### 初学Django时碰到的一个需求，因为公司中很多员工在修改密码之后，有一些关联的客户端或网页中的旧密码没有更新，导致密码在尝试多次之后账号被锁，为了减少这种让人头疼的重置解锁密码的操蛋工作，自己做了一个自助修改小平台。  
### 代码结构不咋样，但是能用，有需要的可以直接拿去用。
#### 场景说明：
因为本公司AD是早期已经在用，用户的个人信息不是十分全面，例如:用户手机号。  
钉钉是后来才开始使用，钉钉默认是使用手机号登录。
用户自行重置密码时如果通过手机号来进行钉钉与AD之间的验证就行不通了。 


### 逻辑：
>已经与之前不同，现在改成内嵌小应用，不再支持直接通过网页开始，之前的扫码方式有点多此一举的味道。

 ## <u>_**所能接受的账号规则**_ </u>
无论是钉钉、微信，均是通过提取用户邮箱的前缀部分来作为关联AD的账号，所以目前的识别逻辑就需要保证邮箱的前缀和AD的登录账号是一致的。
如果您的场景不是这样，请按自己的需求修改源代码适配。


### 提示：
```
AD必须使用SSL才能修改密码（这里被坑了N久...）
自行部署下AD的证书服务，并颁发CA证书，重启服务器生效。
具体教程百度一下，有很多。
```

### 本次升级、修复，请使用最新版：
+ 升级Python版本为3.8
+ 升级Django到3.2
+ 修复用户名中使用\被转义的问题
+ 重写了dingding模块，因为dingding开发者平台接口鉴权的一些变动，之前的一些接口不能再使用，本次重写。
+ 重写了ad模块，修改账号的一些判断逻辑。
+ 重写了用户账号的格式兼容，现在用户账号可以兼容：username、DOMAIN\username、username@abc.com这三种格式。
+ 优化了整体的代码逻辑，去掉一些冗余重复的代码。


### 2022/12/16 -- 更新：
+ 修改钉钉、企业微信直接通过企业内部免密登录授权或验证的方式实现用户信息的获取，直接通过软件内部工作平台打开，废弃扫码方式（由于API接口的权限问题，一些关键数据已经不再支持通过扫码获取）

### 2023/01/15 -- 更新：
+ 兼容PC与移动端的显示（使用Layui）
+ 修复一些BUG
+ 移除auto-install.sh中的redis部署步骤
+ 抽出应用中的授权验证跳转的代码，单独做成一个auth页面，可实现选择首页是进入修改密码，还是自动跳转重置页面。
+ 调整部分文件说明
+ 添加日志装饰器记录请求日志
+ 优化ad_ops中异常的处理


### 2023/02/10 -- 更新：
+ 修复一些BUG
+ auto-install.sh 重写，支持Ubuntu\Centos
+ 添加Redis缓存，之前使用内存缓存有问题

**如果想在点击应用之后自动跳转到重置页面，请将回调接口配置成YOURDOMAIN.com/auth**


## 线上环境需要的基础环境：
+ Python 3.8.16 (可自行下载源码包放到项目目录下，使用一键安装)
+ Nginx
+ Uwsgi
+ Redis

### 界面效果

<img alt="截图10" width="500" src="screenshot/QQ截图20230116152954.png">

<img alt="截图10" width="500" src="screenshot/212473880-4a59c535-85bb-42d2-a99a-899265c83136.png">

<img alt="截图10" width="500" src="screenshot/212474222-e1c13e1b-bb6f-4523-b040-24a65055d681.png">

### 移动端
<img alt="截图10" width="500" src="screenshot/212474177-dd68b0c9-81cc-4eb0-9196-e760784e3f69.jpg">
<img alt="截图10" width="500" src="screenshot/212474293-0cd60898-22c3-4258-ac4c-dfee52a6cf1e.png">

## 钉钉必要条件：
#### 创建企业内部应用
* 在钉钉工作台中通过“自建应用”创建应用，选择“企业内部开发”，创建H5微应用，在应用首页中获取应用的：AgentId、AppKey、AppSecret。
* 应用需要权限：通讯录只读权限、邮箱等个人信息，范围是全部员工或自行选择
* 应用安全域名和IP一定要配置，否则无法返回接口数据。

> **如果想实现进入应用就自动授权，跳转重置页面，可将回调域名指定向pwd.abc.com/auth**

参考截图配置：
![截图3](screenshot/h5微应用.png)

![截图4](screenshot/创建H5微应用03.png)

![截图5](screenshot/创建H5微应用04.png)
![截图5](screenshot/创建H5微应用--版本管理与发布.png)

#### 移动接入应用--登录权限：
> 废弃，已经不再需要，如果之前有配置，可以删除！！


## 企业微信必要条件：
* 创建应用，记录下企业的CorpId，应用的ID和Secret。

> **如果想实现进入应用就自动授权，跳转重置页面，可将回调域名指定向pwd.abc.com/auth**


参考截图：
![截图7](screenshot/微扫码13.png)

![截图8](screenshot/微信小应用01-应用主机.png)

![截图9](screenshot/微信小应用01-应用主页-配置.png)

![截图10](screenshot/微信小应用01-网页授权及J-SDK配置.png)
![截图10](screenshot/微信小应用01-企业可信IP.png)


## 飞书必要条件：
 * 暂时没时间，做不了，已经剔除了！

## 如果你觉得这个小工具对你有帮忙的话，可以请我喝杯咖啡~😁😁😁
<img alt="截图10" height="400" src="screenshot/143fce31873f4d7a4ecd7a7b8c6a24c.png" width="300"/>
<img alt="截图10" height="400" src="screenshot/微信图片_20221220140900.png" width="300"/>


## 使用脚本自动部署：
使用脚本自动快速部署，只适合Centos，其它发行版本的Linux请自行修改相关命令。

### 把整个项目目录上传到新的服务器上

#### 先修改配置文件，按自己实际的配置修改项目配置文件：
修改conf/local_settings.py中的参数，按自己的实际参数修改

### 执行部署脚本  
```shell
chmod +x auto-install.sh
./auto-install.sh
```
等待所有安装完成。
#### 以上配置修改完成之后，则可以通过配置的域名直接访问。


# 手动部署：
#### 自行安装完python3之后，使用python3目录下的pip3进行安装依赖：
#### 我自行安装的Python路径为/usr/local/python3

项目目录下的requestment文件里记录了所依赖的相关python模块，安装方法：
>/usr/local/python3/bin/pip3 install -r requestment

等待所有模块安装完成之后进行下一步。

### 按自己实际的配置修改项目配置参数：
修改conf/local_settings.py中的参数，按自己的实际参数修改

```

安装完依赖后，直接执行
/usr/local/python3/bin/python3 manager.py runserver x.x.x.x:8000
即可临时访问项目，线上不适用这种方法，线上环境请使用uwsgi。


## 修改uwsig.ini配置:
IP和路径按自己实际路径修改

```

## 通过uwsgiserver启动：
```shell
请自行修改将脚本修改完之后
复制到/etc/init.d/，给予执行权限。
执行/etc/init.d/uwsigserver start 启动
```

## 自行部署Nginx，然后添加Nginx配置
#### Nginx配置：
Nginx Server配置：
* proxy_pass的IP地址改成自己的服务器IP
* 配置可自己写一个vhost或直接加在nginx.conf中
``` nginx
server {
    listen  80;
    server_name pwd.abc.com;

    location / {
        proxy_pass         http://192.168.x.x:8000;
        proxy_set_header   Host              $host;
        proxy_set_header   X-Real-IP         $remote_addr;
        proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
    }
	access_log  off;
}
```
- 执行Nginx reload操作，重新加载配置