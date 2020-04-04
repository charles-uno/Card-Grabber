
FROM centos

RUN yum install -y epel-release

RUN yum install -y python36 python36-pip

# Grumble grumble
RUN ln -s /usr/bin/python3.6 /usr/bin/python3

RUN pip3.6 install matplotlib Pillow

CMD ["/bin/bash"]
