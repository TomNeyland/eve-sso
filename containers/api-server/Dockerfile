FROM python:2.7.7
ADD ../../ /usr/src/app
#RUN pip install uwsgi
#RUN pip install psycopg2
#RUN pip install Flask
#RUN pip install Flask-SocketIO
#RUN pip install ujson
RUN pip install gunicorn
WORKDIR /usr/src/app
RUN make install
CMD evesso runsocket
