# Django App with RabbitMQ Integration
## Environment Setup
### Setting up MySQL Server
To start the MySQL Docker container, run the following commands in your terminal:
```
export MYSQL_CONTAINER_NAME=mysql-db
export MYSQL_ROOT_PASSWORD=pswd 
export MYSQL_PORT=3307
docker run -p ${MYSQL_PORT}:3306 --detach --name=$MYSQL_CONTAINER_NAME --env="MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD" mysql
```

Wait approximately 10 seconds for the MySQL server to be ready, then create the database schema for the backend server with the following command:
```sh
docker exec -i $MYSQL_CONTAINER_NAME mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "CREATE DATABASE restaurant CHARACTER SET utf8;"
```

### Setting up RabbitMQ
To start RabbitMQ, run the following commands:

```sh
export RABBITMQ_CONTAINER_NAME=rabbitmq
export RABBITMQ_PORT=5672
docker run -p ${RABBITMQ_PORT}:5672 --detach --name $RABBITMQ_CONTAINER_NAME rabbitmq:3.13-management
```

## Backend server

To dockerize and run the Django web server, update the settings paths and run the following commands:
```sh
cd restaurant_backend
docker build -t onurklngc/restaurant-backend:0.0.1 .

export RESTAURANT_BACKEND_CONTAINER_NAME=restaurant-backend
export RESTAURANT_BACKEND_PORT=8001
export RESTAURANT_BACKEND_SETTINGS_PATH=/home/onur/Coding/repos/assignment-django/restaurant_backend/application/settings.py
export RESTAURANT_BACKEND_ORDERING_SETTINGS_PATH=/home/onur/Coding/repos/assignment-django/restaurant_backend/ordering/settings.py

docker stop $RESTAURANT_BACKEND_CONTAINER_NAME && docker rm $RESTAURANT_BACKEND_CONTAINER_NAME
docker run -p ${RESTAURANT_BACKEND_PORT}:8000 --name $RESTAURANT_BACKEND_CONTAINER_NAME \
-v ${RESTAURANT_BACKEND_SETTINGS_PATH}:/application/settings.py \
-v ${RESTAURANT_BACKEND_ORDERING_SETTINGS_PATH}:/ordering/settings.py \
onurklngc/restaurant-backend:0.0.1
```

For the first-time installation, run the following commands to initialize the database and create a superuser:
```sh
docker exec -i $RESTAURANT_BACKEND_CONTAINER_NAME python manage.py migrate
docker exec -it $RESTAURANT_BACKEND_CONTAINER_NAME python manage.py createsuperuser
docker exec -i $MYSQL_CONTAINER_NAME mysql -uroot -p$MYSQL_ROOT_PASSWORD restaurant < scripts/populate_data.sql

```

## Order Processor App

To dockerize and run the order processor application, update the settings paths and run the following commands:
```sh
cd order_processor
export ORDER_PROCESSOR_CONTAINER_NAME=order-processor
export ORDER_PROCESSOR_SETTINGS_PATH=/home/onur/Coding/repos/assignment-django/order_processor/settings.py

docker build -t onurklngc/order-processor:0.0.1 -f Dockerfile .

docker stop $ORDER_PROCESSOR_CONTAINER_NAME && docker rm $ORDER_PROCESSOR_CONTAINER_NAME

docker run --name $ORDER_PROCESSOR_CONTAINER_NAME -v ${ORDER_PROCESSOR_SETTINGS_PATH}:/settings.py \
onurklngc/order-processor:0.0.1

```


## Testing
To run tests for the ordering app, use the following command:


```sh
cd restaurant_backend
python manage.py test ordering.tests
```
