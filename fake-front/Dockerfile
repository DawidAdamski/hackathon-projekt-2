# Używamy oficjalnego obrazu Nginx
FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html

# Opcjonalny config do nginx (jeśli potrzebny)
# COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

# Uruchamiamy Nginx w trybie foreground
CMD ["nginx", "-g", "daemon off;"]

