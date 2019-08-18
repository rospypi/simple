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
COPY install.sh /root/
COPY build.py /root/
RUN /root/install.sh
COPY rospy3 /root/rospy3
COPY tf2_py /root/tf2_py
WORKDIR /root
RUN python3 build.py
CMD ["python3", "-m", "http.server"]
