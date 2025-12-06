# Używamy oficjalnego obrazu Nginx
FROM nginx:alpine

# Kopiujemy plik index.html do katalogu domyślnego serwera Nginx
COPY index.html /usr/share/nginx/html/index.html
COPY script.js /usr/share/nginx/html/script.js
COPY styles.css /usr/share/nginx/html/styles.css

# Kopiujemy opcjonalny plik konfiguracyjny Nginx (jeśli potrzebny)
# COPY nginx.conf /etc/nginx/nginx.conf

# Domyślnie Nginx nasłuchuje na porcie 80
EXPOSE 80

# Uruchamiamy Nginx w trybie foreground
CMD ["nginx", "-g", "daemon off;"]


