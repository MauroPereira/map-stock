#! /bin/bash

# Update the system
sudo yum update -y

# Install Apache
sudo yum install -y httpd.x86_64

# Enable and start the Apache service
sudo systemctl enable httpd --now

# Create a custom index.html file
sudo bash -c 'cat <<EOF > /var/www/html/index.html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Página de Inicio - PIN2 DevOps 2403</title>
</head>
<body>
    <h1>PIN2 DevOps 2024</h1>
    <p><a href="https://github.com/MauroPereira/PIN2_public" target="_blank">PIN2_public project repository</a></p>
    <p>Created by 
        <a href="mailto:mauro.a.p.pereira@gmail.com">Pereira, Mauro Alejandro</a>
    </p>
</body>
</html>
EOF'

