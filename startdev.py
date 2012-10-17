#!/usr/bin/python
import os
port = raw_input("Please enter a port to run on:")
a = os.system("python manage.py runserver 18.181.0.46:" + port)
