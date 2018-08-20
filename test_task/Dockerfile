#FROM ubuntu:16.04 as builder
#
#RUN export DEBIAN_FRONTEND=noninteractive && \
#    apt-get update && \
#    apt-get install -y software-properties-common python-software-properties && \
#    apt-get update
#
#RUN add-apt-repository -y ppa:ethereum/ethereum && \
#    apt-get update -y && \
#    apt-get install -y build-essential unzip libdb-dev libleveldb-dev libsodium-dev zlib1g-dev libtinfo-dev solc sysvbanner wrk
#
#ENV CREL constellation-0.2.0-ubuntu1604
#RUN apt-get install -y wget \
#     tar \
#     git
#
#RUN wget -q https://github.com/jpmorganchase/constellation/releases/download/v0.2.0/$CREL.tar.xz && \
#    tar xfJ $CREL.tar.xz && \
#    cp $CREL/constellation-node /usr/local/bin && chmod 0755 /usr/local/bin/constellation-node && \
#    rm -rf $CREL
#
#ENV GOREL go1.7.3.linux-amd64.tar.gz
#ENV PATH $PATH:/usr/local/go/bin
#RUN wget -q https://storage.googleapis.com/golang/$GOREL && \
#    tar xfz $GOREL && \
#    mv go /usr/local/go && \
#    rm -f $GOREL && \
#    echo 'PATH=$PATH:/usr/local/go/bin' >> /root/.bashrc
#
#RUN git clone https://github.com/jpmorganchase/quorum.git
#RUN cd quorum && \
#    git checkout tags/v2.0.2 && \
#    make all  && \
#    cp build/bin/geth /usr/local/bin  && \
#    cp build/bin/bootnode /usr/local/bin
#
#RUN wget -q https://github.com/jpmorganchase/quorum/releases/download/v1.2.0/porosity && \
#    mv porosity /usr/local/bin && chmod 0755 /usr/local/bin/porosity


#FROM ubuntu:16.04 as builder
#
#WORKDIR /work
#
#RUN apt-get update && \
#    apt-get install -y \
#            build-essential \
#            git \
#            libdb-dev \
#            libsodium-dev \
#            libtinfo-dev \
#            sysvbanner \
#            unzip \
#            wget \
#            wrk \
#            zlib1g-dev
#
#RUN wget -q https://github.com/jpmorganchase/constellation/releases/download/v0.0.1-alpha/ubuntu1604.zip && \
#    unzip ubuntu1604.zip && \
#    cp ubuntu1604/constellation-node /usr/local/bin && \
#    chmod 0755 /usr/local/bin/constellation-node && \
#    cp ubuntu1604/constellation-enclave-keygen /usr/local/bin/ && \
#    chmod 0755 /usr/local/bin/constellation-enclave-keygen && \
#    rm -rf ubuntu1604.zip ubuntu1604
#
#ENV GOREL go1.7.3.linux-amd64.tar.gz
#ENV PATH $PATH:/usr/local/go/bin
#
#RUN wget -q https://storage.googleapis.com/golang/$GOREL && \
#    tar xfz $GOREL && \
#    mv go /usr/local/go && \
#    rm -f $GOREL
#
#RUN git clone https://github.com/jpmorganchase/quorum.git && \
#    cd quorum && \
##    git checkout tags/v2.0.2 && \
#    git checkout tags/v1.2.0 && \
#    make all && \
#    cp build/bin/geth /usr/local/bin && \
#    cp build/bin/bootnode /usr/local/bin && \
#    cd .. && \
#    rm -rf quorum
#
#### Create the runtime image, leaving most of the cruft behind (hopefully...)
#
#FROM ubuntu:16.04
#
## Install add-apt-repository
#RUN apt-get update && \
#    apt-get install -y --no-install-recommends software-properties-common && \
#    add-apt-repository ppa:ethereum/ethereum && \
#    apt-get update && \
#    apt-get install -y --no-install-recommends \
#        libdb-dev \
#        libsodium-dev \
#        libtinfo-dev \
#        solc && \
#    rm -rf /var/lib/apt/lists/*
#
## Temporary useful tools
##RUN apt-get update && \
##        apt-get install -y iputils-ping net-tools vim
#
#COPY --from=builder \
#        /usr/local/bin/constellation-node \
#        /usr/local/bin/constellation-enclave-keygen \
#        /usr/local/bin/geth \
#        /usr/local/bin/bootnode \
#    /usr/local/bin/
#
#CMD ["/qdata/start-node.sh"]


#FROM ubuntu:16.04 as builder
#
#WORKDIR /work
#
#RUN apt-get update && \
#    apt-get install -y \
#            build-essential \
#            git \
#            libdb-dev \
#            libsodium-dev \
#            libtinfo-dev \
#            sysvbanner \
#            unzip \
#            wget \
#            wrk \
#            zlib1g-dev
#
#RUN wget -q https://github.com/jpmorganchase/constellation/releases/download/v0.2.0/constellation-0.2.0-ubuntu1604.tar.xz && \
#    tar xfJ constellation-0.2.0-ubuntu1604.tar.xz && \
#    cp constellation-0.2.0-ubuntu1604/constellation-node /usr/local/bin && \
#    chmod 0755 /usr/local/bin/constellation-node && \
#    rm -rf constellation*
#
#ENV GOREL go1.7.3.linux-amd64.tar.gz
#ENV PATH $PATH:/usr/local/go/bin
#
#RUN wget -q https://storage.googleapis.com/golang/$GOREL && \
#    tar xfz $GOREL && \
#    mv go /usr/local/go && \
#    rm -f $GOREL
#
#RUN git clone https://github.com/jpmorganchase/quorum.git && \
#    cd quorum && \
#    git checkout tags/v2.0.0 && \
#    make all && \
#    cp build/bin/geth /usr/local/bin && \
#    cp build/bin/bootnode /usr/local/bin && \
#    cd .. && \
#    rm -rf quorum
#
#### Create the runtime image, leaving most of the cruft behind (hopefully...)
#
#FROM ubuntu:16.04
#
## Install add-apt-repository
#RUN apt-get update && \
#    apt-get install -y --no-install-recommends software-properties-common && \
#    add-apt-repository ppa:ethereum/ethereum && \
#    apt-get update && \
#    apt-get install -y --no-install-recommends \
#        libdb-dev \
#        libleveldb-dev \
#        libsodium-dev \
#        libtinfo-dev \
#        solc && \
#    rm -rf /var/lib/apt/lists/*
#
## Temporary useful tools
## RUN apt-get update && \
##     apt-get install -y iputils-ping net-tools vim
#
#COPY --from=builder \
#        /usr/local/bin/constellation-node \
#        /usr/local/bin/geth \
#        /usr/local/bin/bootnode \
#    /usr/local/bin/
#
#CMD ["/qdata/start-node.sh"]

FROM ubuntu:16.04 as builder

ARG CONSTELLATION_VERSION=0.3.2
ARG QUORUM_VERSION=2.0.2

WORKDIR /work

RUN apt-get update && \
    apt-get install -y \
            build-essential \
            git \
            libdb-dev \
            libsodium-dev \
            libtinfo-dev \
            sysvbanner \
            unzip \
            wget \
            wrk \
            zlib1g-dev

RUN wget -q https://github.com/jpmorganchase/constellation/releases/download/v$CONSTELLATION_VERSION/constellation-$CONSTELLATION_VERSION-ubuntu1604.tar.xz && \
    tar -xvf constellation-$CONSTELLATION_VERSION-ubuntu1604.tar.xz && \
    cp constellation-$CONSTELLATION_VERSION-ubuntu1604/constellation-node /usr/local/bin && \
    chmod 0755 /usr/local/bin/constellation-node && \
    rm -rf constellation-$CONSTELLATION_VERSION-ubuntu1604.tar.xz constellation-$CONSTELLATION_VERSION-ubuntu1604

ENV GOREL go1.7.3.linux-amd64.tar.gz
ENV PATH $PATH:/usr/local/go/bin

RUN wget -q https://storage.googleapis.com/golang/$GOREL && \
    tar xfz $GOREL && \
    mv go /usr/local/go && \
    rm -f $GOREL

RUN git clone https://github.com/jpmorganchase/quorum.git && \
    cd quorum && \
    git checkout tags/v$QUORUM_VERSION && \
    make all && \
    cp build/bin/geth /usr/local/bin && \
    cp build/bin/bootnode /usr/local/bin && \
    cd .. && \
    rm -rf quorum

### Create the runtime image, leaving most of the cruft behind (hopefully...)

FROM ubuntu:16.04

# Install add-apt-repository
RUN apt-get update && \
    apt-get install -y --no-install-recommends software-properties-common && \
    add-apt-repository ppa:ethereum/ethereum && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        libdb-dev \
        libleveldb-dev \
        libsodium-dev \
        zlib1g-dev\
        libtinfo-dev \
        solc && \
    rm -rf /var/lib/apt/lists/*

# Temporary useful tools
#RUN apt-get update && \
#        apt-get install -y iputils-ping net-tools vim

COPY --from=builder \
        /usr/local/bin/constellation-node \
        /usr/local/bin/geth \
        /usr/local/bin/bootnode \
    /usr/local/bin/

CMD ["/qdata/start-node.sh"]