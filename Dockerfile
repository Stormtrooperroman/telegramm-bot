FROM  nvidia/opengl:base
ENV DISPLAY=":0"
RUN mkdir /test
ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY :0
COPY . /test
# RUN cd test
RUN apt update && apt install -y libglew-dev unzip libxrandr-dev libxinerama-dev libxcursor-dev libinput-dev libxi-dev g++ cmake python3-pip
# # RUN apt install -y xserver-xorg-video-dummy x11-apps glew-utils nvidia-331-updates nvidia-modprobe
# # RUN pip3 install -U --pre aiogram
# RUN apt install -y mesa-utils xorg-dev nvidia-331-updates
RUN apt install -y libegl1-mesa wget libxtst6 libxv1 libxt6 xauth x11-xkb-utils xkb-data mesa-utils xorg
RUN wget "https://sourceforge.net/projects/virtualgl/files/3.1/virtualgl_3.1_amd64.deb"
RUN wget "https://sourceforge.net/projects/turbovnc/files/3.0.3/turbovnc_3.0.3_amd64.deb"
RUN dpkg -i virtualgl_*.deb
RUN dpkg -i turbovnc_*.deb

# # VOLUME /tmp/.X11-unix
# RUN nvidia-xconfig -a --use-display-device=None --virtual=1024x768
# # COPY xorg.conf /etc/X11/xorg.conf
# # RUN /usr/bin/X :0 &
# # CMD cat 
CMD bash


# FROM alpine:edge

# RUN apk update

# # Dependencies for GLFW (not required for this example)
# RUN apk add \
#     build-base \
#     libx11-dev \ 
#     libxcursor-dev \
#     libxrandr-dev \
#     libxinerama-dev \
#     libxi-dev \
#     bash\
#     mesa-dev

# ENV GLIBC_REPO=https://github.com/sgerrand/alpine-pkg-glibc
# ENV GLIBC_VERSION=2.30-r0

# RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub
# RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.35-r1/glibc-2.35-r1.apk
# RUN apk add glibc-2.35-r1.apk

# # Required to run xvfb-run
# RUN apk add mesa-dri-gallium xvfb-run

# # virtualgl includes glxinfo
# RUN apk add virtualgl --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ --allow-untrusted

# RUN mkdir /test
# COPY . /test

# CMD bash