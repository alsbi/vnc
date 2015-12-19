# Description
-------------------

##Config

### nginx.conf

server {
       server_name  vnc.alsbi.ru;
       return       301 https://$server_name$request_uri;

}


server {
        listen 443 ssl;
        #/home/vnc/vnc_service/bin
        ssl on;
        server_name  vnc.alsbi.ru;
        ssl_certificate     /home/vnc/vnc_service/bin/server.crt;
        ssl_certificate_key /home/vnc/vnc_service/bin/server.key;
        ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;


        location ~* .(jpg|jpeg|gif|png|ico|css|zip|rar|pdf|m3u|js)$ {
                rewrite /include/(.*)$ /$1 last;
                access_log /home/vnc/log;
                root /home/vnc/vnc_service/lib/python3.4/site-packages/vnc_viewer/templates/static/;
                error_page 404 = 404;

        }

        location / {
                  access_log /home/vnc/log;
                  proxy_set_header X-Real-IP  $remote_addr;
                  proxy_set_header X-Forwarded-For $remote_addr;
                  proxy_set_header Host $host;
                  proxy_pass http://127.0.0.1:5000;
                  #include uwsgi_params;
                  #uwsgi_pass unix:///var/vnc.sock;
        }
}

### vds config

       <graphics type='vnc' port='-1' autoport='yes' websocket='-1' listen='0.0.0.0' keymap='ru' passwd='qazwsx12'>
          <listen type='address' address='0.0.0.0'/>
        </graphics>


# virsh config

       auth_tcp = "sasl"
       listen_tcp = 1
       listen_tls = 0
       

-------------------

# Install
-------------------

# Features
-------------------