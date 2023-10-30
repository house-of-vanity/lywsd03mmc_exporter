FROM python:slim

WORKDIR /app

COPY requirements.txt ./
RUN apt update && apt install -y make clang libglib2.0-dev bluez dbus 
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD [ "python", "./bt_exporter.py" ]
CMD ./entrypoint.sh
