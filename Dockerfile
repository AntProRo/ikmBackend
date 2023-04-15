FROM python:3.9
WORKDIR /ikmback
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
COPY ./requirements.txt /ikmback/requirements.txt
RUN apt-get update
RUN apt-get install -y --reinstall ca-certificates 
RUN apt install -y libgl1-mesa-glx python3-opencv poppler-utils postgresql-server-dev-all
RUN apt-get install 'ffmpeg'\
    'libsm6'\
    'libxext6'  -y
COPY ./uploadFile /ikmback/uploadFile 
COPY ./virtualStorage /ikmback/virtualStorage
#RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --no-cache-dir --upgrade -r /ikmbackend/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /ikmback/
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
