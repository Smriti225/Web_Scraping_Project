Download  "redis" to run celery and check its running or not by following steps: 
c_drive > program files > redis >  redis cli > type ping 
if it returns pong means it is working.

Also download "chrome driver" compatible to your chrome and in update
chrome_driver_path in your scraper.py file with the  address where chromedriver is installed

run project using command : python manage.py runserver
run celery worker using command :celery -A scraping_task.celery worker -l info
 
To create tables in sqlite : python manage.py makemigrations
oython manage.py migrate

**Note: All these things are mentioned for "windows operating system"
 
