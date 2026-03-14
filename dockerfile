FROM php:8.2-apache

# Instalacja rozszerzeń MySQL
RUN docker-php-ext-install mysqli pdo pdo_mysql
RUN docker-php-ext-enable mysqli

# Włączenie mod_rewrite
RUN a2enmod rewrite

# Kopiowanie plików
COPY . /var/www/html/

# Ustawienie uprawnień
RUN chown -R www-data:www-data /var/www/html/
RUN chmod -R 755 /var/www/html/

# Konfiguracja Apache
RUN echo "DirectoryIndex index.php index.html" > /etc/apache2/conf-available/directory-index.conf
RUN a2enconf directory-index

EXPOSE 80
