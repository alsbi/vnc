# Description
-------------------

##Config

### nginx.conf

    server {
            listen 80;
            server_name  DOMAIN.RU;
            location ~* .(jpg|jpeg|gif|png|ico|css|zip|rar|pdf|m3u|js)$ {
                    rewrite /include/(.*)$ /$1 last;
                    access_log /home/vnc/log;
                    root STATIC_PATH;
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