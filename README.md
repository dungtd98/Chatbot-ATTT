# Chatbot-ATTT
## Feature:
### Authentication and Authorization
- Custom user model, login base on email
- Custom permissions for 4 types of user: - ContentCreator/Moderator/Admin/Leader
- Login/Logout with block after several login failed time
- Tracking user do to endpoint in their login phase
### Chatbot
- Use viber chatbot to automatic answer question base on database
- Implement with ChatGPT gpt-3.5-turbo model
- User sub/unsub chatbot measurement system

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
