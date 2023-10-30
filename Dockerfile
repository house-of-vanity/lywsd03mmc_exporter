FROM python:slim

WORKDIR /app

COPY requirements.txt ./
RUN apt update && apt install --no-install-recommends -y make clang libglib2.0-dev bluez dbus && pip install --no-cache-dir -r requirements.txt && apt remove -y make clang libglib2.0-dev && apt-get clean autoclean && apt-get autoremove --yes && rm -rf /var/lib/apt/lists/*
#RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD [ "python", "./bt_exporter.py" ]
CMD ./entrypoint.sh
