FROM python:3.8.0-buster

MAINTAINER Vamshi Basupalli <vamshi@cs.wisc.edu>

RUN apt-get update \
    && apt-get upgrade --yes \
    && apt-get update \
    && apt-get install alien --yes

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get install --fix-missing --yes \
    apt-utils lsb-release sudo ncompress \
    xz-utils net-tools libssl-dev \
    curl unzip git wget \
    gcc make autoconf automake build-essential unzip
    
ENV USERNAME builder

RUN /usr/sbin/groupadd -g 10010 $USERNAME \
    && /usr/sbin/useradd -u 10010 -g 10010 --create-home --home /home/$USERNAME $USERNAME \
    && echo '' >> /etc/sudoers \
    && echo "$USERNAME ALL = (ALL) NOPASSWD: ALL" >> /etc/sudoers \
    && chown -R $USERNAME.$USERNAME /home/$USERNAME \
    && chsh -s /bin/bash $USERNAME \
    && sed --in-place -E 's@^(Defaults    requiretty)$@#&@' /etc/sudoers

USER $USERNAME

WORKDIR /home/$USERNAME

COPY . .

run pip install --user -r requirements.txt

ENV PATH=/home/$USERNAME/.local/bin:$PATH

EXPOSE 9090

ENTRYPOINT ["python3", "-m", "flask_weather"]
