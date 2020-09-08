# # For more information, please refer to https://aka.ms/vscode-docker-python
# FROM python:3.8-slim-buster

# # Keeps Python from generating .pyc files in the container
# ENV PYTHONDONTWRITEBYTECODE 1

# # Turns off buffering for easier container logging
# ENV PYTHONUNBUFFERED 1

# RUN set -xe \
#     && apt-get update \
#     && apt-get install -y autoconf \
#                           build-essential \
#                           git \
#                           libffi-dev \
#                           libssl-dev \
#                           libtool \
#                           libxml2 \
#                           libxml2-dev \
#                           libxslt1.1 \
#                           libxslt1-dev \
#                           python3 \
#                           python3-dev \
#                           vim-tiny \
#     && apt-get install -y libtiff5 \
#                           libtiff5-dev \
#                           libfreetype6-dev \
#                           libjpeg62-turbo \
#                           libjpeg62-turbo-dev \
#                           liblcms2-2 \
#                           liblcms2-dev \
#                           libwebp6 \
#                           libwebp-dev \
#                           zlib1g \
#                           zlib1g-dev

# RUN mkdir -p /app
# WORKDIR /app
# COPY . .
# # Install pip requirements
# COPY ./requirements.txt ./requirements.txt 
# RUN python3 -m pip3 install -r requirements.txt

# # Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
# RUN useradd appuser && chown -R appuser /app
# RUN chmod 777 -R /app

# USER appuser
# EXPOSE 6800
# # During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# # CMD ["python", "app.py"]
# # CMD ["scrapyd", "--pidfile="]
# CMD ["/bin/bash"]
FROM python:3.7.0

RUN mkdir -p /app
WORKDIR /app
COPY . /app

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --upgrade pip

