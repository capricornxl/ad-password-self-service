#!/bin/bash

SCRIPT=$(readlink -f $0)
CWD=$(dirname ${SCRIPT})
os_distro=''
os_version=''
get_selinux=''
gen_password=$(echo "$(hostname)$(date)" |base64 |cut -b 1-24)

function get_os_basic_info() {
    if [[ -f /etc/lsb-release ]]; then
        os_distro=$(lsb_release -d |awk '{print $2}')
        os_version=$(lsb_release -d -s |awk '{print $2}')
    elif [[ -f /etc/redhat-release ]]; then
        os_distro=$(cat /etc/redhat-release |awk '{print $1}')
        os_version=$(cat /etc/redhat-release |awk '{print $4}')
        get_selinux=$(getenforce)
        if [[ ${get_selinux} =~ enforcing|Enforcing ]];then
            echo "请先禁用SELINUX~~! ..."
            exit 1
        fi
    else
        echo "不能识别的操作系统，请选择使用Ubuntu或Centos! ..."
        exit 1
    fi
}

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

function check_domain() {
    local DOMAIN=$1
    if echo $DOMAIN |grep -P "(?=^.{4,253}$)(^(?:[a-zA-Z0-9](?:(?:[a-zA-Z0-9\-]){0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$)" >/dev/null; then
        return 0
    else
        return 1
    fi
}

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

function safe_installer() {
    local _run_cmd="$@"
    if [[ ${os_distro} =~ (CentOS|Redhat) ]]; then
        sudo yum makecache
        sudo yum install -y ${_run_cmd}
    elif [[ ${os_distro} =~ (Ubuntu|Debian) ]]; then
        sudo apt-get update
        sudo apt-get install -y ${_run_cmd}
    else
        echo "未适配的操作系统 ${os_distro}"
        exit 1
    fi
    if [[ $? -ne 0 ]]; then
        echo "安装 [${_run_cmd}] 失败"
        exit 1
    fi
}

get_os_basic_info
echo "============================================================================="
echo "  此脚本为快速部署，支持[Ubuntu, Debian, Centos]
  请准备一个新的环境运行,本脚本会快速安装相关的环境和所需要的服务
  如果你运行脚本的服务器中已经存在如：Nginx、Python3等，可能会破坏掉原有的应用配置"
echo "  当前目录：${CWD}"
echo "  操作系统发行版本：${os_distro}, 系统版本：${os_version} ..."
echo "============================================================================="

while :; do echo
    echo "请确认你此台服务器是全新干净的，以防此脚本相关操作对正在运行的服务造成影响（不可逆） ..."
    read -p "请确认是否继续执行，输入 [y/n]: " ensure_yn
    if [[ ! "${ensure_yn}" =~ ^[y,n]$ ]]; then
      echo "输入有误，请输入 y 或 n ..."
    else
      break
    fi
done

if [[ "${ensure_yn}" = n ]]; then
    exit 0
fi


while :; do echo
    read -p "请输入密码自助平台使用的本机IP: " PWD_SELF_SERVICE_IP
    check_ip "${PWD_SELF_SERVICE_IP}"
    if [[ $? -ne 0 ]]; then
      echo "---输入的IP地址格式有误，请重新输入 ..."
    else
      break
    fi
done

while :; do echo
    read -p "请输入密码自助平台使用的端口(不要和Nginx[80]一样): " PWD_SELF_SERVICE_PORT
    check_port "${PWD_SELF_SERVICE_PORT}"
    if [[ $? -ne 0 ]]; then
      echo "---输入的端口有误，请重新输入 ..."
    else
      break
    fi
done

while :; do echo
    read -p "请输入密码自助平台使用域名，例如：pwd.abc.com（不需要加http://或https://） " PWD_SELF_SERVICE_DOMAIN
    check_domain "${PWD_SELF_SERVICE_DOMAIN}"
    if [[ $? -ne 0 ]]; then
      echo "---输入的域名格式有误，请重新输入 ..."
    else
      break
    fi
done

echo
echo "==============================================="
echo "开始部署 ..."

if [[ ! -f "${CWD}/.init_package.Done" ]]; then
    echo "初始化依赖包 ..."
    if [[ ${os_distro} =~ (CentOS|Redhat) ]]; then
        sudo yum makecache
        sudo yum install epel-release
        sudo yum makecache
        sudo yum install -y @development zlib-devel bzip2 bzip2-devel readline-devel sqlite \
    sqlite-devel openssl openssl-devel xz xz-devel libffi-devel ncurses-devel readline-devel tk-devel \
    libpcap-devel findutils wget nginx curl tar initscripts
    elif [[ ${os_distro} =~ (Ubuntu|Debian) ]]; then
        sudo apt-get update
        sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl wget nginx curl tar initscripts
    fi
    if [[ $? -eq 0 ]]; then
        echo "初始化依赖包完成 ..."
        touch ${CWD}/.init_package.Done
    else
        echo "初始化依赖包失败 ..."
        exit 1
    fi
fi

if [[ ! -f "${CWD}/.redis.Done" ]]; then
    safe_installer redis
    if [[ $? -eq 0 ]]; then
        sed -i 's@^requirepass.*@@g' /etc/redis/redis.conf
        sed -i "/# requirepass foobared/a requirepass ${gen_password}" /etc/redis/redis.conf
        sed -i "s@REDIS_PASSWORD.*@REDIS_PASSWORD = r'${gen_password}'@g" ${CWD}/conf/local_settings.py
        touch ${CWD}/.redis.Done
        echo "安装 redis-server 成功"
    else
        echo "安装 redis-server 失败，请重新运行本脚本再试"
    fi
fi

redis_service=''
if [[ -f /usr/lib/systemd/system/redis.service ]];then
    redis_service=redis
elif [[ -f /usr/lib/systemd/system/redis-server.service ]]; then
    redis_service='redis-server'
fi

if [[ -z ${redis_service} ]]; then
    echo "Redis服务名未能识别到，请自行手动重启本机的Redis服务 ..."
else
    rm -f /etc/nginx/conf.d/default.conf
    rm -f /etc/nginx/sites-enabled/default.conf
    systemctl restart ${redis_service}
fi

NGINX_USER=$(grep -E '^user' /etc/nginx/nginx.conf |sed 's@user @@g' |sed 's@;@@g' |awk '{print $1}')

cat <<'EOF' >/etc/nginx/nginx.conf
worker_processes auto;
pid /run/nginx.pid;

events {
    use epoll;
    worker_connections 2048;
}

http {
    include mime.types;
    default_type application/octet-stream;
    server_tokens off;
    client_header_buffer_size 16k;
    client_body_buffer_size 128k;
    keepalive_timeout 65;
    keepalive_requests 120;
    sendfile on;
    tcp_nodelay on;
    tcp_nopush on;
    charset utf-8;
    autoindex off;
    # gzip
    gzip on;
    gzip_min_length 1k;
    gzip_buffers 4 16k;
    gzip_comp_level 3;
    gzip_disable "MSIE [1-6]\.";
    gzip_types text/plain application/x-javascript text/css application/xml text/javascript application/x-httpd-php image/jpeg image/gif image/png application/json;
    gzip_vary on;
    gzip_static on;
    # upload file
    client_max_body_size 0;
    proxy_buffering off;
    proxy_send_timeout 10m;
    proxy_read_timeout 10m;
    proxy_connect_timeout 10m;
    proxy_request_buffering off;
    # log
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    access_log /var/log/nginx/access.log;
    # config file
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*.conf;
}
EOF
sed -i "1i\user ${NGINX_USER};" /etc/nginx/nginx.conf

PYTHON_VER='3.8.16'
PYTHON_INSTALL_DIR=/usr/share/python-${PYTHON_VER}
PYTHON_VENV_DIR=${CWD}/pwd_venv

if [[ -f "${CWD}/.python3.Done" ]];then
    echo "Python3己部署，跳过 ..."
else
    if [[ -f "${CWD}/Python-${PYTHON_VER}.tar.xz" ]] && [[ -f "${CWD}/python.${PYTHON_VER}.md5" ]]; then
        python3_md5=$(md5sum "${CWD}/Python-${PYTHON_VER}.tar.xz" |awk '{print $1}')
        python3_md5_record=$(cat ${CWD}/python.${PYTHON_VER}.md5)
        if [[ x"${python3_md5}" != x"${python3_md5_record}" ]]; then
            rm -f "${CWD}/Python-${PYTHON_VER}.tar.xz"
            rm -f "${CWD}/python.${PYTHON_VER}.md5"
        fi
    else
        echo "无Python${PYTHON_VER}.tar.xz，执行下载python ${PYTHON_VER} ..."
        rm -f "${CWD}/Python-${PYTHON_VER}.tar.xz"

        sudo wget -c -t 10 -T 120 https://repo.huaweicloud.com/python/${PYTHON_VER}/Python-${PYTHON_VER}.tar.xz -O ${CWD}/Python-${PYTHON_VER}.tar.xz

        md5sum "${CWD}/Python-${PYTHON_VER}.tar.xz" |awk '{print $1}' > ${CWD}/python.${PYTHON_VER}.md5
        if [[ $? -ne 0 ]]; then
            echo "下载${PYTHON_VER}/Python-${PYTHON_VER}.tar.xz失败，请重新运行本脚本再次重试 ..."
            exit 1
        fi
    fi
    echo "执行安装Python${PYTHON_VER} ..."
    tar xf ${CWD}/Python-${PYTHON_VER}.tar.xz -C ${CWD}/
    cd "${CWD}/Python-${PYTHON_VER}" || exit 1
    sudo ./configure --prefix=${PYTHON_INSTALL_DIR} && make && make install

    if [[ $? -eq 0 ]]; then
      echo "创建python虚拟环境 -> ${PYTHON_VENV_DIR} ..."
      rm -rf "${PYTHON_VENV_DIR}"
      ${PYTHON_INSTALL_DIR}/bin/python3 -m venv --copies "${PYTHON_VENV_DIR}"
      touch ${CWD}/.python3.Done
      echo "Python3 安装成功 ..."
    else
      echo "Python3 安装失败，请重试 ..."
      exit 1
    fi
fi

##修改PIP源为国内
mkdir -p ~/.pip
cat <<'EOF' > ~/.pip/pip.conf
[global]
index-url=https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host=pypi.tuna.tsinghua.edu.cn
EOF

if [[ ! -f "${CWD}/.pip3.Done" ]]; then
    echo "部署pip依赖 ..."
    ${PYTHON_VENV_DIR}/bin/pip3 install --upgrade pip
    ${PYTHON_VENV_DIR}/bin/pip3 install wheel setuptools
    ${PYTHON_VENV_DIR}/bin/pip3 install -r ${CWD}/requirement
    if [[ $? -eq 0 ]]; then
        touch ${CWD}/.pip3.Done
        echo "Pip3 Requirement 安装成功 ..."
    else
        echo "Pip3 Requirement 安装失败 ..."
        exit 1
    fi
fi

##处理配置文件
echo "处理uwsgi.ini配置文件 ..."
CPU_NUM=$(cat /proc/cpuinfo | grep processor | wc -l)
sed -i "s@CPU_NUM@${CPU_NUM}@g" ${CWD}/uwsgi.ini
sed -i "s@PYTHON_VENV_DIR@${PYTHON_VENV_DIR}@g" ${CWD}/uwsgi.ini
sed -i "s@PWD_SELF_SERVICE_HOME@${CWD}@g" ${CWD}/uwsgi.ini
sed -i "s@PWD_SELF_SERVICE_IP@${PWD_SELF_SERVICE_IP}@g" ${CWD}/uwsgi.ini
sed -i "s@PWD_SELF_SERVICE_PORT@${PWD_SELF_SERVICE_PORT}@g" ${CWD}/uwsgi.ini
echo "处理uwsgi.ini配置文件完成 ..."
echo
echo "处理uwsgiserver启动脚本 ..."
sed -i "s@PWD_SELF_SERVICE_HOME@${CWD}@g" ${CWD}/uwsgiserver
sed -i "s@PYTHON_VENV_DIR@${PYTHON_VENV_DIR}@g" ${CWD}/uwsgiserver

alias cp='cp'
cp -rfp ${CWD}/uwsgiserver /etc/init.d/uwsgiserver

chmod +x /etc/init.d/uwsgiserver

systemctl daemon-reload

systemctl enable uwsgiserver

echo "处理uwsgiserver启动脚本完成 ..."
echo

sed -i "s@PWD_SELF_SERVICE_DOMAIN@${PWD_SELF_SERVICE_DOMAIN}@g" ${CWD}/conf/local_settings.py

##Nginx vhost配置
mkdir -p /etc/nginx/conf.d
cat <<EOF >/etc/nginx/conf.d/pwdselfservice.conf
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

systemctl start nginx

systemctl start uwsgi

echo
echo
echo "密码自助服务平台的访问地址是：http://${PWD_SELF_SERVICE_DOMAIN}或http://${PWD_SELF_SERVICE_IP} ..."
echo "请确保以上域名能正常解析，否则使用域名无法访问 ..."
echo "如果本机防火墙是开启状态，请自行放行端口: [80, ${PWD_SELF_SERVICE_PORT}]"
echo
echo "Uwsgi启动：/etc/init.d/uwsgi start ..."
echo "Uwsgi停止：/etc/init.d/uwsgi stop ..."
echo "Uwsgi重启：/etc/init.d/uwsgi restart ..."
echo
echo "Redis Server密码是：${gen_password}，可在/etc/redis.conf中查到 ..."
echo
echo "文件${CWD}/conf/local_setting.py中配置参数请自行确认下是否完整 ..."
echo
