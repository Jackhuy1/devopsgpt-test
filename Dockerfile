FROM nginx:alpine

# Copy custom homepage
COPY index.html /usr/share/nginx/html/index.html

# Copy custom NGINX configuration
COPY default.conf /etc/nginx/conf.d/default.conf
