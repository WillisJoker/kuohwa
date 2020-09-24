FROM nvidia/cuda:10.1-cudnn7-devel-centos7

ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV TZ Asia/Taipei

# system packages
RUN set -xe; \
    yum -y install gcc gcc-c++ make wget; \
    yum -y install python3 python3-devel; \
    yum -y install lapack-devel blas-devel; \
    yum -y install java-1.8.0-openjdk-1.8.0.242.b08-1.el7; \
    rm -rf /var/cache/yum

# epel packages
RUN set -xe; \
    yum -y install epel-release; \
    yum -y install jq; \
    yum-config-manager --disable epel; \
    rm -rf /var/cache/yum

# python3 basic packages
ENV PYTHONIOENCODING utf-8
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel
RUN python3 -m pip install --no-cache-dir numpy==1.18.5
RUN python3 -m pip install --no-cache-dir pandas==1.0.4
RUN python3 -m pip install --no-cache-dir pytest-runner==5.2
RUN python3 -m pip install --no-cache-dir pytest==5.4.3
RUN python3 -m pip install --no-cache-dir pytest-mock==3.1.0
RUN python3 -m pip install --no-cache-dir psutil==5.7.2
RUN python3 -m pip install --no-cache-dir pyyaml==5.3.1

WORKDIR /workdir
ENV PYTHONPATH /workdir
COPY . .
RUN python3 setup.py pytest
