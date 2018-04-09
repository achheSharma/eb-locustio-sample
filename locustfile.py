# Copyright 2015-2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file
# except in compliance with the License. A copy of the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under the License.

import os
import string
import random
from locust import HttpLocust, TaskSet, task

#test data
global test_id
test_id = 'e6d4468467'
problem_ids = [1,2]
problem_language_id_map = {
    1: [4, 11, 27, 35, 43, 44, 55, 114, 116, 510, 511, 512],
    2: [4, 11, 27, 35, 43, 44, 55, 114, 116, 510, 511, 512]
}

def login(l):
    l.client.post("/users/sign_in/", {"user[email]":"abhimanyu@interviewbit.com", "user[password]":"12!@abAB<>"})

def logout(l):
    l.client.post("/users/sign_out/", {"_method":"delete"})

class MyTaskSet(TaskSet):
    
    def on_start(self):
        login(self)

    def on_stop(self):
        logout(self)

    #open the test programming_language_id
    @task(100)
    def index(self):    
        response = self.client.get("/test/" + test_id + '/')

    #fetch code
    @task(600)
    def fetch_code(self):
        #todo randomize problem id and lanaguege id
        programming_language_id = 1
        problem_id = 2
        response = self.client.get("/test/" + str(test_id) + "/get-code/?programming_language_id=" + str(programming_language_id) + "&problem_id=" + str(problem_id))

    # #save code
    @task(1500)
    def save_code(self):
        programming_language_id = 1
        problem_id = 2
        response = self.client.post("/test/" + str(test_id) + "/save-code/", {
            "problem_id": problem_id, 
            "programming_language_id": programming_language_id,
            "is_objective": 'false',
            "problem_code": 'some content'
        })

    # #Submit Code
    @task(80)
    def submit_code(self):
        programming_language_id = 1
        problem_id = 2
        self.client.post("/test/" + test_id + "/evaluate-code/", {
            "problem_id": problem_id, 
            "programming_language_id": programming_language_id,
            "solution_code": 'some code',  #TODO randomize between function code and various type of non functioning code
            "submission_type": 0
        })

class MyLocust(HttpLocust):
    host = os.getenv('TARGET_URL', "http://localhost:3000")
    task_set = MyTaskSet
    min_wait = 90
    max_wait = 100
