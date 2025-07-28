FROM nginx:latest
COPY default.conf /etc/nginx/conf.d/default.conf
COPY index.html 404.html 50x.html /usr/share/nginx/html/
EXPOSE 80
