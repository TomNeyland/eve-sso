FROM tutum/nginx
RUN apt-get update
RUN apt-get install -y git
RUN rm /etc/nginx/sites-enabled/default
ADD sites-enabled/ /etc/nginx/sites-enabled
RUN git clone https://github.com/TomNeyland/neweden.im-frontend.git
RUN mkdir /www /www/static
RUN mv neweden.im-frontend/build /www/static/neweden.im
