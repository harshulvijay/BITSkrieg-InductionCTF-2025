FROM python:3.9-slim

RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
RUN mkdir -p /workspace/app /workspace/flag

COPY app/requirements.txt /workspace/app/
COPY app/ /workspace/app/

COPY flag/requirements.txt /workspace/flag/
COPY flag/ /workspace/flag/

RUN pip install --no-cache-dir -r /workspace/app/requirements.txt
RUN pip install --no-cache-dir -r /workspace/flag/requirements.txt

RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV FLASK_ENV=production
ENV FLASK_DEBUG=0

EXPOSE 3000

# Start supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
