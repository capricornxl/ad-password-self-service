#!/bin/bash

#set -e

SCRIPT=$(readlink -f "$0")
CWD=$(dirname "$SCRIPT")

# ----------------------------
# 环境变量配置
# ----------------------------
export APP_ENV=${APP_ENV}
export HOME_URL=${HOME_URL}
export NGINX_HTTP_PORT=${NGINX_HTTP_PORT:-8001}
export ENABLE_HTTPS=${ENABLE_HTTPS:-false}
export NGINX_HTTPS_PORT=${NGINX_HTTPS_PORT:-8443}
export CERT_FILE_NAME=${CERT_FILE_NAME:-server.crt}
export KEY_FILE_NAME=${KEY_FILE_NAME:-server.key}
export PORT=${DJANGO_PORT:-9000}
export DJANGO_IP=0.0.0.0
export DJANGO_SITE_PATH=/opt/project    # 不要修改该路径
export DJANGO_SETTINGS_MODULE="config.settings"
export PATH=${DJANGO_SITE_PATH}:${PATH}
export GUNICORN_CONF="${DJANGO_SITE_PATH}/run/gunicorn_conf.py"
export GUNICORN_WORKERS=${GUNICORN_WORKERS:-$(( $(nproc) * 2 + 1 ))}  # 自动计算默认workers
export GRACEFUL_TIMEOUT=${GRACEFUL_TIMEOUT:-300}
export GUNICORN_MAX_REQUESTS=${GUNICORN_MAX_REQUESTS:-1000}
export GUNICORN_MAX_REQUESTS_JITTER=${GUNICORN_MAX_REQUESTS_JITTER:-100}
export GUNICORN_BIND="${DJANGO_IP}:${PORT}"
export GUNICORN_THREADS=${GUNICORN_THREADS:-$(( $(nproc) * 2 ))}
export GUNICORN_TIMEOUT=${GUNICORN_TIMEOUT:-120}
export GUNICORN_RELOAD=${GUNICORN_RELOAD:-false}
export GUNICORN_LOG_LEVEL=${GUNICORN_LOG_LEVEL:-info}
export GUNICORN_WSGI_APP="config.wsgi:application"
export GUNICORN_ASGI_APP="config.asgi:application"
export GUNICORN_KEEPALIVE="${GUNICORN_KEEPALIVE:-65}"
export GUNICORN_WORKER_CLASS="${GUNICORN_WORKER_CLASS:-uvicorn.workers.UvicornWorker}"


if [[ ! -d "${DJANGO_SITE_PATH}" ]]; then
    echo "Error: Django config path not found: ${DJANGO_SITE_PATH}"
    exit 1
fi

cd "${DJANGO_SITE_PATH}"
python_bin="/opt/venv/bin/python"

echo "Working dir: $(pwd)"
# ----------------------------
# Nginx 配置
# ----------------------------
mkdir -p ${DJANGO_SITE_PATH}/run/nginx/conf.d ${DJANGO_SITE_PATH}/run/nginx/certs
if [[ "${ENABLE_HTTPS}" == "true" ]]; then
    echo "HTTPS enabled. Nginx will listen on port ${NGINX_HTTPS_PORT}."
    echo "Generating HTTPS config from template..."
    sed -e "s/HOME_URL/${HOME_URL}/g" \
        -e "s/NGINX_HTTPS_PORT/${NGINX_HTTPS_PORT}/g" \
        -e "s/CERT_FILE_NAME/${CERT_FILE_NAME}/g" \
        -e "s/KEY_FILE_NAME/${KEY_FILE_NAME}/g" \
        -e "s/DJANGO_PORT/${DJANGO_PORT}/g" \
        ${DJANGO_SITE_PATH}/run/nginx/conf.d/site_https.conf.template > ${DJANGO_SITE_PATH}/run/nginx/conf.d/site_https.conf
    echo "HTTPS config generated: ${DJANGO_SITE_PATH}/run/nginx/conf.d/site_https.conf"
    if [[ ! -f ${DJANGO_SITE_PATH}/run/nginx/certs/${CERT_FILE_NAME} ]] || [[ ! -f ${DJANGO_SITE_PATH}/run/nginx/certs/${KEY_FILE_NAME} ]]; then
        echo "Error: Can't find SSL cert or key files: ${DJANGO_SITE_PATH}/run/nginx/certs/${CERT_FILE_NAME}, ${DJANGO_SITE_PATH}/run/nginx/certs/${KEY_FILE_NAME}"
        exit 1
    fi
else
    echo "HTTPS disabled. Nginx will listen on port ${NGINX_HTTP_PORT}."
    echo "Generating HTTP config from template..."
    sed -e "s/HOME_URL/${HOME_URL}/g" \
        -e "s/NGINX_HTTP_PORT/${NGINX_HTTP_PORT}/g" \
        -e "s/DJANGO_PORT/${DJANGO_PORT}/g" \
        ${DJANGO_SITE_PATH}/run/nginx/conf.d/site_http.conf.template > ${DJANGO_SITE_PATH}/run/nginx/conf.d/site_http.conf
    echo "HTTP config generated: ${DJANGO_SITE_PATH}/run/nginx/conf.d/site_http.conf"
fi

# ----------------------------
# 服务启动
# ----------------------------
if [ -f "${GUNICORN_CONF}" ]; then
    echo "Starting Gunicorn + Uvicorn with config: ${GUNICORN_CONF}"
    echo "Bind: ${GUNICORN_BIND}"
    ${python_bin} -m gunicorn \
        -c "${GUNICORN_CONF}" \
        --bind "${GUNICORN_BIND}" \
        --workers ${GUNICORN_WORKERS} \
        "${GUNICORN_WSGI_APP}"
else
    echo "Config file not found: ${GUNICORN_CONF}"
    echo "Starting Uvicorn standalone..."
    ${python_bin} -m uvicorn "${GUNICORN_WSGI_APP}" \
        --host ${IP} --port ${PORT} \
        --workers ${GUNICORN_WORKERS} \
        --log-level ${GUNICORN_LOG_LEVEL}
fi
