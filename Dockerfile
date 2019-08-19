FROM ubuntu:18.04
RUN apt-get update \
    && apt-get install -y \
       python-dev \
       python3-dev \
       python-pip \
       python3-pip \
       git \
       libboost-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY rospy-builder/install.sh /root/
COPY rospy-all /root/rospy-all
COPY tf2_py /root/tf2_py
COPY rospy-builder /root/rospy-builder
WORKDIR /root
RUN ./install.sh
RUN pip3 install /root/rospy-builder
RUN rospy-build -a
CMD ["python3", "-m", "http.server"]
