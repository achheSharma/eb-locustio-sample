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
import sys
from locust import HttpLocust, TaskSet, task

#test data
global test_id
test_id = '3d616fd585'

problem_ids = [50,239,524]
problem_language_id_map = {
    50: [4, 11, 27, 35, 43, 44, 55, 114, 116, 510, 511, 512],
    239: [4, 11, 27, 35, 43, 44, 55, 114, 116, 510, 511, 512],
    524: [4, 11, 27, 35, 43, 44, 55, 114, 116, 510, 511, 512]
}

def signup(l):
    random_user = random.randint(1,sys.maxint)
    l.client.post("/test/a/load_test/", {
        "candidate_email": "abhimanyu+" + str(random_user) +  "@interviewbit.com",
        "password": '12ABXYZ12',
         "candidate_name": str(random_user),
         "candidate_city": "Random",
         "candidate_branch": "candidate_branch",
         "candidate_degree": "candidate_degree",
         "candidate_university": "candidate_university",
         "candidate_contact_number": "9923704608"
         })

def login(l):
    l.client.post("/users/sign_in/", {"user[email]":"abhimanyu@interviewbit.com", "user[password]":"12!@abAB<>"})

def logout(l):
    l.client.post("/users/sign_out/", {"_method":"delete"})

class MyTaskSet(TaskSet):
    
    def on_start(self):
        signup(self)

    def on_stop(self):
        logout(self)

    #open the test programming_language_id
    @task(100)
    def index(self):    
        response = self.client.get("/test/" + test_id + '/')

    #fetch code
    @task(600)
    def fetch_code(self):    
        problem_id = problem_ids[random.randint(0,(len(problem_ids) - 1))]
        supported_languages = problem_language_id_map[problem_id]
        programming_language_id = supported_languages[random.randint(0,(len(supported_languages) - 1))]
        response = self.client.get("/test/" + str(test_id) + "/get-code/?programming_language_id=" + str(programming_language_id) + "&problem_id=" + str(problem_id))

    # #save code
    @task(1500)
    def save_code(self):
        problem_id = problem_ids[random.randint(0,(len(problem_ids) - 1))]
        supported_languages = problem_language_id_map[problem_id]
        programming_language_id = supported_languages[random.randint(0,(len(supported_languages) - 1))]
        response = self.client.post("/test/" + str(test_id) + "/save-code/", {
            "problem_id": problem_id, 
            "programming_language_id": programming_language_id,
            "is_objective": 'false',
            "problem_code": 'some content'
        })

    # #Submit Code
    @task(80)
    def submit_code(self):
        problem_id = problem_ids[random.randint(0,(len(problem_ids) - 1))]
        supported_languages = problem_language_id_map[problem_id]
        programming_language_id = supported_languages[random.randint(0,(len(supported_languages) - 1))]

        self.client.post("/test/" + test_id + "/evaluate-code/", {
            "problem_id": problem_id, 
            "programming_language_id": programming_language_id,
            "submission_content": 'some code',  #TODO randomize between function code and various type of non functioning code
            "submission_type": 'submit'
        }, {
        'X-Requested-With': 'XMLHttpRequest'
        })

    #get submission status
    @task(2400)
    def submission_status(self):        
        problem_id = problem_ids[random.randint(0,(len(problem_ids) - 1))]
        submission_id = 2667
        response = self.client.get("/test/" + str(test_id) + "/status/?problem_id=" + str(problem_id) + "&submission_id=" + str(submission_id))

    #session poll
    @task(4000)
    def session_poll(self):
        response = self.client.get("/test/" + str(test_id) + "/poll/?current_duration=30" + "&current_extra_time=0")

class MyLocust(HttpLocust):
    host = os.getenv('TARGET_URL', "http://localhost:3000")
    task_set = MyTaskSet
    min_wait = 90
    max_wait = 100
