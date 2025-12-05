FROM python:3.8-alpine
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
COPY app.py /app.py
COPY storage.py /storage.py
COPY models.py /models.py