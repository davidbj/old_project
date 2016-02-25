FROM centos:centos6
MAINTAINER shaozhi.zhang <davidbjhd@gmail.com>

#Install epel repo.
#RUN rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
RUN rpm -ivh http://mirrors.163.com/centos/6.7/extras/x86_64/Packages/epel-release-6-8.noarch.rpm

# install sshd
RUN yum install -y supervisor vim unzip openssh-server openssh-clients passwd

#generate ssh key
RUN ssh-keygen -q -N "" -t dsa -f /etc/ssh/ssh_host_dsa_key
RUN ssh-keygen -q -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key
RUN sed -ri 's/UsePAM yes/UsePAM no/g' /etc/ssh/sshd_config

RUN mkdir -p /root/.ssh
COPY ./etc/ssh/id_rsa /root/.ssh/id_rsa
COPY ./etc/ssh/id_rsa.pub /root/.ssh/id_rsa.pub
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan git.pydevops.com >> /root/.ssh/known_hosts

#change root password to 123456
RUN echo 'root:123456' | chpasswd

#EXPOSE 22
COPY ./etc/supervisor/supervisord.conf /etc/supervisord.conf
CMD ["/etc/init.d/supervisord", "start"]
