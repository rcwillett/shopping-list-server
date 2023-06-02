FROM python:3
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD flask --app flaskr run --port=8000 --host=0.0.0.0