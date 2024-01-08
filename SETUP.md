1. Run migrations
1.1. py manage.py makemigrations users
1.2. py manage.py migrate
1.3. py manage.py init_groups
1.2. Create a superuser (necessary, because it will be the default user, look at the code)
1.4. py manage.py makemigrations events
1.5. py manage.py migrate
1.6. python manage.py populate_event_categories
1.7. python manage.py makamigrations
1.8. python manage.py migrate

The second step will create permissions groups and set the permissions
You can change the standard permissions in run time or in the users app /management/init_groups.py