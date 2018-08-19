FROM python:3.6-alpine

RUN \
  apk --no-cache --update add build-base cmake boost-dev git                                                && \
  sed -i -E -e 's/include <sys\/poll.h>/include <poll.h>/' /usr/include/boost/asio/detail/socket_types.hpp  && \
  git clone --depth 1 --recursive -b release https://github.com/ethereum/solidity                           && \
  cd /solidity && cmake -DCMAKE_BUILD_TYPE=Release -DTESTS=0 -DSTATIC_LINKING=1                             && \
  cd /solidity && make solc && install -s  solc/solc /usr/bin
#  cd / && rm -rf solidity                                                                                   && \
#  apk del sed build-base git make cmake gcc g++ musl-dev curl-dev boost-dev                                 && \
#  rm -rf /var/cache/apk/*
#RUN apt-get install -y software-properties-common
#RUN add-apt-repository ppa:ethereum/ethereum
#RUN apt-get update
#RUN apt-get install -y solc
#RUN apt-get update && apt-get install -y libssl-dev

ADD ./requirements.txt /
ADD ./NameValue.sol /

RUN pip install -r /requirements.txt
#RUN python -m solc.install v0.4.24

ADD ./src/ /src

ENV FLASK_APP=/src/app.py
CMD flask run --host=0.0.0.0 --port=8000