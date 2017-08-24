FROM tiangolo/uwsgi-nginx-flask:flask-python3.5-upload

RUN apt-get update
RUN apt-get install -y liblua5.2-dev
RUN	apt-get install -y python3-dev

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# We will copy only python code; all static will be mounted as volumes
# at startup. If you want to use it separatly: uncomment the folllowing lines:
# COPY ./app/templates /app/app/templates
# COPY ./project/static /app/static
COPY ./configs/uwsgi.ini /app/uwsgi.ini
ADD ./app/abac/runtime/alfa.lua /usr/local/share/lua/5.2/angine/alfa.lua
COPY ./app/*.py /app/
COPY ./app/abac /app/abac
