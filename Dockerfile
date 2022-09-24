FROM python

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./smartphones.json /code/smartphones.json

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./api.py /code/

# 
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]
