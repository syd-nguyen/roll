FROM python:3.8-alpine
COPY requirements.txt /requirements.txt
ENV CONNECTION_STRING="mongodb+srv://sydnguyen:uva343TL%23%2B%23%2B@cluster0.9srpoaq.mongodb.net/?appName=Cluster0"
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
COPY app.py /app.py
COPY storage.py /storage.py
COPY models.py /models.py