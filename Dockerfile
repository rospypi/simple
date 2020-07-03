FROM ubuntu:18.04
RUN apt-get update \
    && apt-get install -y \
       python-dev \
       python-pip \
       python3-dev \
       python3-pip \
       python3-sip-dev \
       git \
       libboost-dev \
       libeigen3-dev \
       liblz4-dev \
       curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /root
COPY rospy-builder/install.sh /root/
RUN ./install.sh
COPY cv_bridge /root/cv_bridge
COPY PyKDL /root/PyKDL
COPY roslz4 /root/roslz4
COPY rospy-all /root/rospy-all
COPY rospy-builder /root/rospy-builder
COPY tf2_py /root/tf2_py
COPY packages.yaml /root/packages.yaml
RUN pip3 install /root/rospy-builder
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN rospy-build build -d any
RUN rospy-build build -d linux --native
RUN rospy-build index index --local any --local linux
CMD ["python3", "-u", "-m", "http.server"]
