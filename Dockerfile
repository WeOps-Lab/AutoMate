FROM centos:7

# ADD http://mirrors.aliyun.com/repo/Centos-7.repo /etc/yum.repos.d/CentOS-Base.repo
# ADD http://mirrors.aliyun.com/repo/epel-7.repo /etc/yum.repos.d/epel.repo
RUN  yum makecache && yum install -y epel-release && yum install -y  python3-pip java-1.8.0-openjdk libaio  && rm -rf /var/cache/yum/* && yum clean all

ENV LC_CTYPE=en_US.UTF-8

WORKDIR /opt


RUN pip3 install --upgrade pip
RUN pip3 install PyVmomi
RUN pip3 install requests
RUN pip3 install  ansible
RUN pip3 install supervisor

WORKDIR /app
ADD ./asserts ./asserts
ADD ./bin ./bin
ADD ./server ./server
ADD ./core ./core
ADD ./main.py ./main.py
ADD ./.env.prod ./env
ADD ./requirements.txt ./requirements.txt
ADD ./alembic ./alembic
ADD ./ansible_plugins ./ansible_plugins
ADD ./inventory ./inventory
ADD ./supervisord.conf ./supervisord.conf
ENV APP_HOST 0.0.0.0
ENV APP_PORT 8080
ENV ENV prod
ENV CELERY_BROKER redis://:password@127.0.0.1:6379/12
ENV CELERY_BACKEND redis://:password@127.0.0.1:6379/14
ENV VAULT_URL http://127.0.0.1:8200
ENV VAULT_TOKEN hvs.tokenxxxtoken
ENV REDIS_URL redis://:password@127.0.0.1:6379/14
ENV PUSH_GATEWAY_URL http://127.0.0.1:9001
RUN pip3 install -r requirements.txt 
RUN pip3 install -r ansible_plugins/requirements.txt 

RUN useradd -u 1001 -ms /bin/bash  example
RUN mkdir -p /app/run
RUN mkdir -p /app/ansible_data
RUN mkdir -p /app/logs/automate
RUN chown -R 1001:1001 /app

USER example
CMD supervisord -c supervisord.conf --nodaemon
