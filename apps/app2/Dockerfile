FROM httpd:alpine

COPY index.html /usr/local/apache2/htdocs/index.html

RUN echo "OK" > /usr/local/apache2/htdocs/health_check

COPY security.conf /usr/local/apache2/conf/extra/security.conf

RUN echo "Include conf/extra/security.conf" >> /usr/local/apache2/conf/httpd.conf
