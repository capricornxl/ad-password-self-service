# Base image
FROM python:3.12-slim

# Environment variables
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Shanghai \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    ca-certificates \
    tzdata \
 && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
 && echo "Asia/Shanghai" > /etc/timezone \
 && rm -rf /var/lib/apt/lists/*

# Create python venv
RUN python -m venv /opt/venv

# Upgrade pip tools
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple \
    --upgrade pip setuptools wheel

# Install Python requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple \
    --trusted-host pypi.tuna.tsinghua.edu.cn \
    -r /tmp/requirements.txt

# Setup project directory
WORKDIR /opt/project
RUN mkdir -p \
    /opt/project/gunicorn \
    /opt/project/uvicorn \
    /opt/project/log/nginx

# Entrypoint
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
