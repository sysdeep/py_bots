FROM python:3.10.12-slim


WORKDIR /app/


COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

# app
COPY main.py ./
COPY app ./app/

CMD ["python3", "main.py"]
