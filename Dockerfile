FROM ubuntu:22.04

RUN mkdir /test

COPY . /test
RUN cd test
RUN sudo apt update && sudo apt install libglew-dev unzip libxrandr-dev libxinerama-dev libxcursor-dev libinput-dev libxi-dev g++ cmake
RUN python3 -m venv venv
RUN ./test/venv/script/activate

RUN pip install -U --pre aiogram