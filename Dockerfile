FROM python:3.8

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./app/* /code/.
RUN mkdir -p /code/models_20230217
COPY ./app/models_20230217/* /code/models_20230217/.

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

