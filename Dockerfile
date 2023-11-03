FROM objectiv/backend


ENV DEBIAN_FRONTEND=non-interactive


ENV APP=/services/version_checker/

USER root
# setup nginx proxy
RUN mkdir -p $APP && \
    apt -q update && \
    apt -qy upgrade && \
    apt install -qy nginx && \
    apt clean

WORKDIR /services

COPY version_checker/docker/*.py  $APP
COPY version_checker/docker/requirements.txt $APP

RUN pip install -r version_checker/requirements.txt


COPY version_checker/docker/gunicorn.conf.py /etc/
COPY version_checker/docker/nginx.conf /etc/nginx/
COPY version_checker/docker/entry_point.sh /services


CMD /services/entry_point.sh
ENTRYPOINT /services/entry_point.sh
