## ikmBackend

# To run this program
create a folder named IKMWEB

# clone this repository inside of your folder
https://github.com/AntProRo/ikmBackend.git

and rename the folder "backend" instead of ikmBackend

# run this line
pip install - r requirements.txt

# and maybe these lines

1. python manage.py makemigrations

2. python manage.py migrate

# and finally

python manage.py runserver     

# if is not working you could change auth_system/settings.py
## from this 
ALLOWED_HOSTS = ['ikmbackend-production.up.railway.app','ikmfrontend-production.up.railway.app'] 
## to this
ALLOWED_HOSTS = []

# Web page

https://railway.app/project/e2f4cb1d-7d26-4120-a5fb-c74e2391f601/service/87996043-e129-4018-854d-df537d905283
