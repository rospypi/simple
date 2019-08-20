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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /root
COPY rospy-builder/install.sh /root/
RUN ./install.sh
COPY rospy-all /root/rospy-all
COPY tf2_py /root/tf2_py
COPY PyKDL /root/PyKDL
COPY rospy-builder /root/rospy-builder
RUN pip3 install /root/rospy-builder
RUN rospy-build -a
CMD ["python3", "-m", "http.server"]
