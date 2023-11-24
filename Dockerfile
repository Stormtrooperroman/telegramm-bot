# FROM python:3.11-slim
FROM ubuntu:20.04
RUN apt-get update; DEBIAN_FRONTEND=noninteractive apt-get install -y ffmpeg git \
python3 python3-pip wget

# RUN curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

# RUN echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

# RUN DEBIAN_FRONTEND=noninteractive apt-get install -y redis

RUN apt-get autoremove
COPY requirements.txt .
# RUN python -m pip install -r requirements.txt
# RUN python -m pip install git+https://github.com/Desklop/StressRNN
RUN pip3 install -r requirements.txt
RUN pip3 install git+https://github.com/Desklop/StressRNN
RUN pip3 install torch --index-url https://download.pytorch.org/whl/cpu
WORKDIR /bot

RUN wget https://huggingface.co/IlyaGusev/saiga2_7b_gguf/resolve/main/model-q4_K.gguf -P /bot

COPY . /bot

CMD ["python3", "-u","main.py"]
