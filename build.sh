sudo docker-compose down --remove-orphan

if [[ "$ZEMFROG_ENV" = "production" ]]; then
    sudo docker-compose -f docker-compose.prod.yml up -d --build
else
    sudo docker-compose up -d --build db redis
fi
