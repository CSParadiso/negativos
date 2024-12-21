FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY negativos.py ./

EXPOSE 9876

ENTRYPOINT ["streamlit", "run", "negativos.py", "--server.port=9876", "--server.address=0.0.0.0"]