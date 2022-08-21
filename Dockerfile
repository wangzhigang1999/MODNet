FROM  python:3.8.12-slim-buster

WORKDIR /root

COPY . .

#RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y && /usr/local/bin/python -m pip install --upgrade pip && pip install -r req.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y && /usr/local/bin/python -m pip install --upgrade pip && pip install -r req.txt
#RUN  /usr/local/bin/python -m pip install --upgrade pip && pip install -r req.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN   #pip install -r req.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 5000


CMD ["python","main.py"]