FROM python:2.7.7
ADD . app
WORKDIR app
RUN make install
