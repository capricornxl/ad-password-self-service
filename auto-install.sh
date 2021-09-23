#!/bin/bash
echo -e "此脚本为快速部署，目前只做了Centos版本的，如果是其它系统请自行修改下相关命令\n请准备一个新的环境运行\n本脚本会快速安装相关的环境和所需要的服务\n如果你运行脚本的服务器中已经存在如：Nginx、Python3等，可能会破坏掉原有的应用配置。"

##Check IP
function check_ip() {
    local IP=$1
    VALID_CHECK=$(echo $IP|awk -F. '$1<=255&&$2<=255&&$3<=255&&$4<=255{print "yes"}')
    if echo $IP|grep -E "^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$" >/dev/null; then
        if [[ $VALID_CHECK == "yes" ]]; then
            return 0
        else
            return 1
        fi
    else
        return 1
    fi
}

##Check domain
function check_domain() {
    local DOMAIN=$1
    if echo $DOMAIN |grep -P "(?=^.{4,253}$)(^(?:[a-zA-Z0-9](?:(?:[a-zA-Z0-9\-]){0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$)" >/dev/null; then
        return 0
    else
        return 1
    fi
}

##Check Port
function check_port() {
    local PORT=$1
    VALID_CHECK=$(echo $PORT|awk '$1<=65535&&$1>=1{print "yes"}')
    if echo $PORT |grep -E "^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]{1}|6553[0-5])$" >/dev/null; then
        if [[ $VALID_CHECK == "yes" ]]; then
            return 0
        else
            return 1
        fi
    else
        return 1
    fi
}

while :; do echo
    echo "请确认你此台服务器是全新干净的，以防此脚本相关操作对正在运行的服务造成影响（不可逆）。"
    read -p "请确认是否继续执行，输入 [y/n]: " ensure_yn
    if [[ ! "${ensure_yn}" =~ ^[y,n]$ ]]; then
      echo "输入有误，请输入 y 或 n"
    else
      break
    fi
done

if [[ "${ensure_yn}" = n ]]; then
    exit 0
fi

echo "======================================================================="
while :; do echo
    read -p "请输入密码自助平台使用的本机IP: " PWD_SELF_SERVICE_IP
    check_ip ${PWD_SELF_SERVICE_IP}
    if [[ $? -ne 0 ]]; then
      echo "---输入的IP地址格式有误，请重新输入。"
    else
      break
    fi
done

echo "======================================================================="
while :; do echo
    read -p "请输入密码自助平台使用的端口(不要和Nginx一样): " PWD_SELF_SERVICE_PORT
    check_port ${PWD_SELF_SERVICE_PORT}
    if [[ $? -ne 0 ]]; then
      echo "---输入的端口有误，请重新输入。"
    else
      break
    fi
done

echo "======================================================================="
while :; do echo
    read -p "请输入密码自助平台使用域名，例如：pwd.abc.com（不需要加http://或https://） " PWD_SELF_SERVICE_DOMAIN
    check_domain ${PWD_SELF_SERVICE_DOMAIN}
    if [[ $? -ne 0 ]]; then
      echo "---输入的域名格式有误，请重新输入。"
    else
      break
    fi
done

##当前脚本的绝对路径
SHELL_FOLDER=$(dirname $(readlink -f "$0"))



echo "关闭SELINUX"
sudo setenforce 0
sudo sed -i 's@SELINUX=*@SELINUX=disabled@g' /etc/selinux/config
echo "DONE....."
echo "关闭防火墙"
sudo systemctl disable firewalld
sudo systemctl stop firewalld
echo "DONE....."

echo "初始化编译环境----------"
sudo yum install gcc patch libffi-devel python-devel zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel wget psmisc -y
echo "======================================================================="
echo "初始化编译环境完成"
echo "======================================================================="

##Quick install nginx
echo "======================================================================="
echo "安装 Nginx"
sudo cat << EOF > /etc/yum.repos.d/nginx.repo
[nginx-stable]
name=nginx stable repo
baseurl=http://nginx.org/packages/centos/7/\$basearch/
gpgcheck=1
enabled=1
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true
EOF

sudo yum makecache fast
sudo yum install nginx -y

if [[ $? -eq 0 ]]
then
  sudo systemctl enable nginx
  sudo systemctl start nginx
  echo "======================================================================="
  echo "nginx 安装成功！"
  echo "======================================================================="
else
  echo "======================================================================="
  echo "nginx 安装失败！"
  echo "======================================================================="
  exit 1
fi

##install python3
##如果之前用此脚本安装过python3，后续就不会再次安装。
PYTHON_VER='3.8.9'
PYTHON_INSTALL_DIR=/usr/share/python-${PYTHON_VER}
if [[ -f "${PYTHON_INSTALL_DIR}/bin/python3" ]]
then
    echo "己发现Python3，将不会安装。"
else
    if [[ -f "Python-${PYTHON_VER}.tar.xz" ]]
    then
        echo "将安装Python${PYTHON_VER}"
        tar xf Python-${PYTHON_VER}.tar.xz
        cd Python-${PYTHON_VER}
        sudo ./configure --prefix=${PYTHON_INSTALL_DIR} && make && make install
    else
        echo "脚本目录下没有发现Python${PYTHON_VER}.tar.xz，将会下载python ${PYTHON_VER}"
        sudo wget https://www.python.org/ftp/python/${PYTHON_VER}/Python-${PYTHON_VER}.tar.xz
        tar xf Python-${PYTHON_VER}.tar.xz
        cd Python-${PYTHON_VER}
        sudo ./configure --prefix=${PYTHON_INSTALL_DIR} && make && make install
    fi

    if [[ $? -eq 0 ]]
    then
      echo "创建python3和pip3的软件链接"
      cd ${SHELL_FOLDER}
      sudo ln -svf ${PYTHON_INSTALL_DIR}/bin/python3 /usr/bin/python3
      sudo ln -svf ${PYTHON_INSTALL_DIR}/bin/pip3 /usr/bin/pip3
      echo "======================================================================="
      echo "Python3 安装成功！"
      echo "======================================================================="
    else
      echo "======================================================================="
      echo "Python3 安装失败！"
      echo "======================================================================="
      exit 1
    fi
fi


##修改PIP源为国内
mkdir -p ~/.pip
cat << EOF > ~/.pip/pip.conf
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host=pypi.tuna.tsinghua.edu.cn
EOF

cd ${SHELL_FOLDER}
echo "====升级pip================"
/usr/bin/pip3 install --upgrade pip
/usr/bin/pip3 install -r requestment

if [[ $? -eq 0 ]]
then
  echo "======================================================================="
  echo "Pip3 requestment 安装成功！"
  echo "======================================================================="
else
  echo "======================================================================="
  echo "Pip3 requestment 安装失败！"
  echo "======================================================================="
  exit 1
fi

##处理配置文件
echo "======================================================================="
echo "处理uwsgi.ini配置文件"
CPU_NUM=$(cat /proc/cpuinfo | grep processor | wc -l)
sed -i "s@CPU_NUM@${CPU_NUM}@g" ${SHELL_FOLDER}/uwsgi.ini
sed -i "s@PWD_SELF_SERVICE_HOME@${SHELL_FOLDER}@g" ${SHELL_FOLDER}/uwsgi.ini
sed -i "s@PWD_SELF_SERVICE_IP@${PWD_SELF_SERVICE_IP}@g" ${SHELL_FOLDER}/uwsgi.ini
sed -i "s@PWD_SELF_SERVICE_PORT@${PWD_SELF_SERVICE_PORT}@g" ${SHELL_FOLDER}/uwsgi.ini
echo "处理uwsgi.ini配置文件完成"
echo
echo "处理uwsgiserver启动脚本"
sed -i "s@PWD_SELF_SERVICE_HOME@${SHELL_FOLDER}@g" ${SHELL_FOLDER}/uwsgiserver
sed -i "s@PYTHON_INSTALL_DIR@${PYTHON_INSTALL_DIR}@g" ${SHELL_FOLDER}/uwsgiserver
alias cp='cp'
cp -f ${SHELL_FOLDER}/uwsgiserver /etc/init.d/uwsgiserver
chmod +x /etc/init.d/uwsgiserver
chkconfig uwsgiserver on
echo "处理uwsgiserver启动脚本完成"
echo

sed -i "s@PWD_SELF_SERVICE_DOMAIN@${PWD_SELF_SERVICE_DOMAIN}@g" ${SHELL_FOLDER}/conf/local_settings.py

##Nginx vhost配置
cat << EOF > /etc/nginx/conf.d/pwdselfservice.conf
server {
    listen  80;
    server_name ${PWD_SELF_SERVICE_DOMAIN} ${PWD_SELF_SERVICE_IP};

    location / {
        proxy_pass         http://${PWD_SELF_SERVICE_IP}:${PWD_SELF_SERVICE_PORT};
        proxy_set_header   Host              \$host;
        proxy_set_header   X-Real-IP         \$remote_addr;
        proxy_set_header   X-Forwarded-For   \$proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto \$scheme;
    }
	access_log off;
}
EOF
rm -f /etc/nginx/conf.d/default.conf
systemctl restart nginx

echo
echo "======================================================================="
echo
echo "密码自助服务平台的访问地址是：http://${PWD_SELF_SERVICE_DOMAIN}或http://${PWD_SELF_SERVICE_IP}"
echo "请确保以上域名能正常解析，否则使用域名无法访问。"
echo
echo "Uwsgi启动：/etc/init.d/uwsgi start"
echo "Uwsgi停止：/etc/init.d/uwsgi stop"
echo "Uwsgi重启：/etc/init.d/uwsgi restart"
echo
echo
echo "文件${SHELL_FOLDER}/conf/local_setting.py中配置参数请自动确认下是否完整"
echo
echo "======================================================================="
