FROM python:3.11
WORKDIR /app
COPY ./ /app/
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD uvicorn main:app --reload --port 8000 --host 0.0.0.0