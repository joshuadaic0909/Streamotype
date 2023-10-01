events { worker_connections 1024; }

http {
    log_format proxy '[$time_local] $remote_addr passed to: $host ($upstream_addr): $request_uri, proxy pass: $proxy_host, location: $request_uri';


    server {
        access_log /var/log/nginx/access.log proxy;
        listen 80;
        server_name default_server;

        location / {
            proxy_connect_timeout 300s; # Wait for 300s before giving up
            proxy_pass http://$FLASK_HOST:$FLASK_PORT;
        }

        location ~ ^/streamlit_apps/(?<port>\d+) {
            proxy_pass http://$FLASK_HOST:$port$request_uri;
            proxy_set_header   Host      $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Proto $scheme;
            proxy_buffering    off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_read_timeout 86400;
        }
    }
}