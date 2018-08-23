1. pacman install postgresql
2. follow arch wiki to configure postgres and create a new user 
3. pro tip give psql user same name as ur username
4. create database beatlstw
5. python manage.py createsuperuser
6. python manage.py runserver
7. get localhost:8000/admin and login with superuser

8. to deploy, take care of awseb auth and cli installs, then run eb deploy

9. to dump the db, use:
    pg_dump -h aat4bf9s6yui7a.csg9dlnvxudw.us-west-2.rds.amazonaws.com -U root -f ./dump.sql ebdb

10. the pw is what you think it is
