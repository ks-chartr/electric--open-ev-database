FROM python:3.6
RUN mkdir /app
WORKDIR /app
COPY Opendata/requirements.txt . 
RUN pip install -r requirements.txt
COPY . .
WORKDIR /app/Opendata
EXPOSE 8000
CMD ["python","manage.py","runserver","0.0.0.0:8000"]

