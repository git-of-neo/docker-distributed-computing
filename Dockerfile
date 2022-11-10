FROM python:3.11

WORKDIR /app

COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./app .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]
# CMD ["pwd"]