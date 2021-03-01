FROM python:3.9.2-alpine

WORKDIR /api
COPY . .
RUN pip install -r requirements.txt

WORKDIR /
EXPOSE 8000
CMD [ "gunicorn", "-b", "0.0.0.0:8000", "api:create_app(testing=False)" ]