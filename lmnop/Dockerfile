FROM python:3.8
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt gunicorn
EXPOSE 5000
ENTRYPOINT ["gunicorn", "-w=4", "-b=0.0.0.0:5000", "application:app" ]