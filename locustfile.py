
import os
import logging
import json
import pyquery

from locust import HttpLocust, TaskSet, task
from threading import Timer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('INIT')

def login(l):
    print ("=========Login=========")
    resp = l.client.get("/users/sign_in")
    dom = pyquery.PyQuery(resp.content)
    auth_token = dom.find('input[name="authenticity_token"]')[0].attrib['value']
    l.client.post("/users/sign_in/", {"user[email]":"vaibhavasthana.lmp@gmail.com", "user[password]":"stagingpassword", "authenticity_token":auth_token})

def logout(l):
    print ("=========Logout=========")
    l.client.post("/users/sign_out/", {"_method":"delete"})

class MyTaskSet(TaskSet):

    def on_start(self):
        login(self)

    def on_stop(self):
        logout(self)

    @task
    def dashboard(self):
        print ("=========Mentee-Dashbaord=========")
        response = self.client.get('/academy/mentee-dashboard/')
        logger.info(response.status_code)

    @task
    def dashboard_classroom(self):
        print ("=========Mentee-Dashbaord-Classroom=========")
        response = self.client.get('/academy/mentee-dashboard/classroom/')
        logger.info(response.status_code)

class MyLocust(HttpLocust):
    host = os.getenv('TARGET_URL', "http://localhost:3000")
    task_set = MyTaskSet
    min_wait = 90
    max_wait = 100
