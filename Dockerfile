FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade pip
 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src
EXPOSE 8000

CMD ["uvicorn", "src.main.app:app", "--host", "0.0.0.0", "--port", "8000"]