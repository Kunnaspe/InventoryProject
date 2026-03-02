#!/bin/bash
set -e

APP_DIR="/home/ec2-user/InventoryProject"
VENV="$APP_DIR/.venv"

echo "=== [1/7] Installing system packages ==="
sudo dnf update -y
sudo dnf install -y python3 python3-pip python3-devel gcc nginx mariadb105-devel

echo "=== [2/7] Creating Python virtual environment ==="
cd "$APP_DIR"
python3 -m venv .venv
source .venv/bin/activate

echo "=== [3/7] Installing Python dependencies ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== [4/7] Downloading RDS SSL certificate ==="
curl -o "$APP_DIR/rds-ca.pem" https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem

echo "=== [4b/7] Running Django setup ==="
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py shell -c "
from django.contrib.sites.models import Site
Site.objects.update_or_create(id=1, defaults={'domain': 'd10al5xqkgu4pk.cloudfront.net', 'name': 'Inventory App'})
print('Site updated.')
"

echo "=== [5/7] Setting up Gunicorn systemd service ==="
sudo tee /etc/systemd/system/gunicorn.service > /dev/null <<EOF
[Unit]
Description=Gunicorn for InventoryProject
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=$APP_DIR
EnvironmentFile=$APP_DIR/.env
ExecStart=$VENV/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 DjangoProject.wsgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

echo "=== [6/7] Setting up Nginx ==="
sudo tee /etc/nginx/conf.d/inventory.conf > /dev/null <<EOF
server {
    listen 80 default_server;
    server_name _;

    location /static/ {
        alias $APP_DIR/static/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Remove the default server block from nginx.conf so it doesn't conflict
sudo python3 -c "
import re, shutil
shutil.copy('/etc/nginx/nginx.conf', '/etc/nginx/nginx.conf.bak')
with open('/etc/nginx/nginx.conf') as f:
    content = f.read()
# Strip the server { ... } block from inside the http block
content = re.sub(r'\n    server \{[^}]*(?:\{[^}]*\}[^}]*)*\}', '', content)
with open('/etc/nginx/nginx.conf', 'w') as f:
    f.write(content)
print('nginx.conf cleaned')
"

echo "=== [7/7] Starting services ==="
sudo systemctl daemon-reload
sudo systemctl enable --now gunicorn
sudo systemctl enable --now nginx
sudo systemctl restart gunicorn
sudo systemctl restart nginx

echo ""
echo "=== Deployment complete! ==="
echo "App: https://d10al5xqkgu4pk.cloudfront.net/inventory/"
