From python:3.6.5

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT 5000
EXPOSE $PORT

CMD [ "python", "./app.py" ]