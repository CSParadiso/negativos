FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 9876

ENTRYPOINT ["streamlit", "run", "negativos.py", "--server.port=9876", "--server.address=0.0.0.0"]