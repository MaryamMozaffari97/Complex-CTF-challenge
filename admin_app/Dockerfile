# Use the official PHP image with Apache
FROM php:7.4-apache

# Install the necessary PHP extensions
RUN docker-php-ext-install mysqli

# Create a system user and set the ownership of the /var/www/html/ directory
RUN useradd -r -s /bin/false phpuser \
    && chown -R phpuser:www-data /var/www/html/

# Copy your PHP code to the container
COPY --chown=phpuser:www-data ./src/ /var/www/html/
