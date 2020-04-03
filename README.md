# Events 'R' Us

This project was created and tested on Python 3.8.  
Hosted version: https://mcclymontdev.pythonanywhere.com/

## Setup

Using anaconda prompt:
```
conda create -n events_r_us
```

Once you have the conda enviroment (events_r_us) activate run:

```
pip install -r requirements.txt
or
pip3 install -r requirements.txt
```

Testing the install:
```
cd events_r_us
```
then run:
```
python manage.py runserver
```
Then go to:
```
http://127.0.0.1:8000/
```

## Populating the database
To populate the database first make sure there is no existing sqlite3 DB file.  
Make the initial migrations:
```
python manage.py makemigrations events
```
Apply the migrations:
```
python manage.py migrate
```
Then finally, run the population script:
```
python populate_events.py
```
