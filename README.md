# Chatbot-ATTT
## Guide
### 1. Setup environtment for poject
- Open terminal inside project and run follow commands:
```
  docker-compose up --build
```
- Open another terminal and run
```
  docker-compose run api bash
  python manage.py migrate
  python manage.py create_permission
  python manage.py createsuperuser
```

### 2. API endpoint: 
