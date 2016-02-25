FROM centos:centos7
MAINTAINER from www.pydevops.com(davidbjhd@gmail.com)

#RUN rpm -ivh http://mirrors.yun-idc.com/centos/7.1.1503/extras/x86_64/Packages/epel-release-7-5.noarch.rpm
RUN rpm -ivh http://mirrors.163.com/centos/7.1.1503/extras/x86_64/Packages/epel-release-7-5.noarch.rpm

RUN \
    yum install --nogpgcheck -y openssh-server openssh-clients pwgen sudo hostname wget patch htop iftop vim mc links supervisor && \
    yum clean all && \
    ssh-keygen -q -b 1024 -N '' -t rsa -f /etc/ssh/ssh_host_rsa_key && \
    ssh-keygen -q -b 1024 -N '' -t dsa -f /etc/ssh/ssh_host_dsa_key && \
    ssh-keygen -q -b 521 -N '' -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key && \
    sed -i -r 's/.?UseDNS\syes/UseDNS no/' /etc/ssh/sshd_config && \
    sed -i -r 's/.?ChallengeResponseAuthentication.+/ChallengeResponseAuthentication no/' /etc/ssh/sshd_config && \
    sed -i -r 's/.?PermitRootLogin.+/PermitRootLogin yes/' /etc/ssh/sshd_config

RUN echo "root:123456" | chpasswd
RUN mkdir -p /var/log/supervisor
COPY sshd.ini /etc/supervisord.d/sshd.ini
COPY  bootstrap.sh /

#add id_rsa and id_rsa.pub
COPY ./etc/id_rsa /root/.ssh/id_rsa
COPY ./etc/id_rsa.pub /root/.ssh/id_rsa.pub
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan git.chunbo.com >> /root/.ssh/known_hosts
   
RUN chmod +x /bootstrap.sh
VOLUME ["/data"]
ENTRYPOINT ["/bootstrap.sh"]
