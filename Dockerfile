# FROM python:3.11-slim
FROM ubuntu:18.04
RUN apt-get update; DEBIAN_FRONTEND=noninteractive apt-get install -y ffmpeg git python3 python3-pip
RUN apt-get autoremove
COPY requirements.txt .
# RUN python -m pip install -r requirements.txt
# RUN python -m pip install git+https://github.com/Desklop/StressRNN
RUN pip3 install -r requirements.txt
RUN pip3 install git+https://github.com/Desklop/StressRNN


# RUN wget https://huggingface.co/IlyaGusev/saiga2_7b_gguf/resolve/main/model-q4_K.gguf
WORKDIR /bot
COPY . /bot

CMD ["python", "main.py"]
