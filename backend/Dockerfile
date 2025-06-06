FROM python:3.13-slim

RUN apt-get update && apt-get install -y gcc python3-dev wget

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --retries 10 --default-timeout=100 -r /app/requirements.txt

RUN mkdir -p /weights/facenet-torch/ && \
    wget https://github.com/timesler/facenet-pytorch/releases/download/v2.2.9/20180402-114759-vggface2.pt \
    -O /weights/facenet-torch/20180402-114759-vggface2.pt

RUN mkdir -p /weights/mobilenet-v3/ && \
    wget https://download.pytorch.org/models/mobilenet_v3_small-047dcff4.pth \
    -O /weights/mobilenet-v3/mobilenet_v3_small.pth

COPY . /app

RUN chmod +x initialization/entrypoint_db.sh

ENTRYPOINT ["./initialization/entrypoint_db.sh"]

CMD [ "python", "main.py" ]