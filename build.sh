sudo docker-compose down --remove-orphan

if [[ "$ZEMFROG_ENV" = "production" ]]; then
    echo "Running in production..."
    sudo docker-compose up -d --build -f docker-compose.prod.yml
else
    sudo docker-compose up -d --build
fi