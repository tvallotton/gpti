FROM python:3.9.15
WORKDIR /home/app
COPY . .
RUN pip install -r requirements.txt
CMD [ "fastapi", "run" ]