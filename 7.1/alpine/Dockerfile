#
# NOTE: FILE GENERATED VIA "update.sh"
#
# PLEASE DO NOT EDIT IT DIRECTLY
#
FROM php:7.1-alpine

MAINTAINER Paweł Tomulik <ptomulik@meil.pw.edu.pl>

ARG SAMI_UID=1000
ARG SAMI_GID=1000
ARG SAMI_CONFIG
ARG SAMI_PROJECT_TITLE
ARG SAMI_SOURCE_DIR
ARG SAMI_BUILD_DIR
ARG SAMI_CACHE_DIR
ARG SAMI_SERVER_PORT=8001

ENV SAMI_UID=$SAMI_UID \
    SAMI_GID=$SAMI_GID \
    SAMI_CONFIG=$SAMI_CONFIG \
    SAMI_PROJECT_TITLE=$SAMI_PROJECT_TITLE \
    SAMI_SOURCE_DIR=$SAMI_SOURCE_DIR \
    SAMI_BUILD_DIR=$SAMI_BUILD_DIR \
    SAMI_CACHE_DIR=$SAMI_CACHE_DIR \
    SAMI_SERVER_PORT=$SAMI_SERVER_PORT

RUN set -xe && \
  apk add --no-cache --update inotify-tools git && \
  curl -s -L -o /usr/local/bin/sami http://get.sensiolabs.org/sami.phar && \
  chmod a+x /usr/local/bin/sami && \
  addgroup -g $SAMI_GID sami && \
  adduser -D -G sami -u $SAMI_UID sami

COPY bin/* /usr/local/bin/

VOLUME /home/sami/project

USER sami
COPY etc/sami.conf.php /home/sami/

WORKDIR /home/sami/project

ENTRYPOINT [ "sami-entrypoint" ]
CMD [ "sami-autoserve" ]

EXPOSE $SAMI_SERVER_PORT
# vim: ft=dockerfile:
