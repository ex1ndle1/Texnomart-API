This is an API service for  Texnomart
I've added unit tests into test.py file

For this project I used this stack:
   DB:postgresql
   Cache:Redis
   Frameworks:Django rest framework 
   Technologies: JWT
   Clouad storage: Cloudinary S3



So I containerizied all project into docker.

All you need is just to docker-compose file :
docker-compose up -d


And you should try to check is Redis working:
redis-cli ping
Output should be: PONG
If not, write into terminal : redis-server
So , you can do all CRUD  actions with API 
