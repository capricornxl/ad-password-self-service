# 编译代码
FROM python:3.6.13-slim as stage-build
MAINTAINER Xiangle0109@outlook.com
ARG VERSION
ENV VERSION=1.0

WORKDIR /opt/password-self-service
ADD ./ad-password.tar.gz ./

ARG PIP_MIRROR=https://pypi.douban.com/simple
ENV PIP_MIRROR=$PIP_MIRROR

WORKDIR /opt/password-self-service


RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && apt update \
    && grep -v '^#' ./docker-src/deb_requirement | xargs apt -y install \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -c -f UTF-8 -i zh_CN zh_CN.UTF-8 \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime


RUN pip install --upgrade pip==20.2.4 setuptools==49.6.0 wheel==0.34.2 -i ${PIP_MIRROR} \
    && pip config set global.index-url ${PIP_MIRROR} \
    && pip install --no-cache-dir -r ./docker-src/requirement

VOLUME /opt/password-self-service/log

ENV LANG=zh_CN.UTF-8

EXPOSE 8070
EXPOSE 8080
ENTRYPOINT ["./entrypoint.sh"]
