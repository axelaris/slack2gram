FROM python:3.9
ADD main.py /app/
ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
CMD python3 main.py