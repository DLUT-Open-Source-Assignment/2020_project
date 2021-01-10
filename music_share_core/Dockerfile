FROM python:3.9
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
CMD ["python", "app.py"]

EXPOSE 5000