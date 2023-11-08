FROM public.ecr.aws/lts/ubuntu:22.04

RUN apt update
RUN apt install -y build-essential
RUN apt install -y python3
RUN apt install -y python3-dev
RUN apt install -y python3-venv
RUN apt install -y curl
RUN apt install -y vim
RUN apt install -y wget

COPY . /helm/
RUN useradd -ms /bin/bash helm
RUN chown -R helm /helm

USER helm
WORKDIR /home/helm

RUN cd /helm && ./install-helm-local.sh

CMD cd /helm && . private_helm_env/bin/activate && exec /bin/bash
