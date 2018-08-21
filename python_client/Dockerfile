FROM python:3.6-alpine

RUN \
  apk --no-cache --update add build-base cmake boost-dev git                                                && \
  sed -i -E -e 's/include <sys\/poll.h>/include <poll.h>/' /usr/include/boost/asio/detail/socket_types.hpp  && \
  git clone --depth 1 --recursive -b release https://github.com/ethereum/solidity                           && \
  cd /solidity && cmake -DCMAKE_BUILD_TYPE=Release -DTESTS=0 -DSTATIC_LINKING=1                             && \
  cd /solidity && make solc && install -s  solc/solc /usr/bin

ADD ./requirements.txt /
ADD ./NameValue.sol /

RUN pip install -r /requirements.txt

ADD ./src/ /src

ENV FLASK_APP=/src/app.py
CMD flask run --host=0.0.0.0 --port=8000