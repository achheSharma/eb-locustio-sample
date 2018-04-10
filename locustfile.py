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
import logging
import json

from locust import HttpLocust, TaskSet, task
from threading import Timer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('INIT')

#test data
global test_id
test_id = '3d616fd585'

problem_ids = [50,239,524]
problem_language_id_map = {
    50: [4, 11, 27, 35, 43, 44, 55, 114, 116, 510, 511, 512],
    239: [4, 11, 27, 35, 43, 44, 55, 114, 116, 510, 511, 512],
    524: [4, 11, 27, 35, 43, 44, 55, 114, 116, 510, 511, 512]
}

problem_codes = {
    50: [
        'syntax error',
        'wrong output',
        'public class Solution {// DO NOT MODIFY THE LISTpublic ArrayList<Integer> slidingMaximum(final List<Integer> A, int B) {int n = A.size();int i;ArrayList<Integer> res = new ArrayList<>();int window = Math.min(A.size(), B);Deque<Node> deque = new LinkedList<>();int val;Node ans;      for (i = 0; i < window - 1; i++) {val = A.get(i);           while (!deque.isEmpty() && deque.peekFirst().val <= val) {deque.pollFirst();}           deque.addFirst(new Node(i, val));}      for (; i < n; i++) {val = A.get(i);         while (!deque.isEmpty() && (i - deque.peekLast().index >= window)) {deque.pollLast();}          while (!deque.isEmpty() && deque.peekFirst().val <= val) {deque.pollFirst();}           deque.addFirst(new Node(i, val));           ans = deque.peekLast();         res.add(ans.val);}      return res;}    class Node {int val;int index;      public Node(int index, int val) {this.index = index;this.val = val;}}}'
        ],
    239: [
        'syntax error',
        'wrong output',
        'public class Solution {       static class Node {       int key;       int val;       Node prev, next;       public Node(int key, int val) {           this.key = key;           this.val = val;       }   }       Node head;   Node tail;   int N;   int MAX;   HashMap<Integer, Node> mMap;       public Solution(int capacity) {       head = null;       tail = null;       MAX = capacity;       N = 0;       mMap = new HashMap<>();   }       public int get(int key) {               if (N == 0)           return -1;               if (mMap.containsKey(key)) {                       Node node = mMap.get(key);                       if (key == head.key) {               return node.val;           }                       if (tail.key == key) {               tail = tail.prev;           }                       Node temp = node.prev;           temp.next = node.next;           temp = node.next;           if (temp != null)               temp.prev = node.prev;                           node.next = head;           head.prev = node;           node.prev = null;           head = node;                       return node.val;       }                       return -1;   }       public void set(int key, int value) {               if (mMap.containsKey(key)) {                       Node node = mMap.get(key);           Node temp;                       if (node.key == head.key) {               node.val = value;               return;           }                       if (tail.key == key) {               tail = tail.prev;           }                       temp = node.prev;           temp.next = node.next;           temp = node.next;           if (temp != null)               temp.prev = node.prev;                           node.next = head;           head.prev = node;           node.prev = null;           head = node;                       node.val = value;                       return;       }               if (N == MAX) {           if (tail != null) {               mMap.remove(tail.key);               tail = tail.prev;                               if (tail != null) {                   tail.next.prev = null;                   tail.next = null;               }               N--;           }       }               Node node = new Node(key, value);       node.next = head;       if (head != null)           head.prev = node;           head = node;       N++;               if (N == 1)           tail = head;               mMap.put(key, node);       }}'
        ],
    524: [
        'syntax error',
        'wrong output',
        'public class Solution {public int canCompleteCircuit(final List<Integer> gas, final List<Integer> cost) {      int n;int petrol = 0;int i;int min = 0;int temp = 0;int lastPos = 0;        n = gas.size();     for (i = 0; i < n; i++) {petrol += gas.get(i);petrol -= cost.get(i);lastPos = Math.max(petrol, gas.get(i) - cost.get(i) + lastPos);         if (lastPos >= 0) {if (min == -1)min = i;} else {min = -1;}         lastPos = Math.max(0, lastPos);}        if (petrol < 0)return -1;               return min;     }}'
        ]
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

    l.client.post( "/test/" + test_id + '/' + "save-candidate-details",{
        "candidate_email": "abhimanyu+" + str(random_user) +  "@interviewbit.com",
        "password": '12ABXYZ12',
         "candidate_name": str(random_user),
         "candidate_city": "Random",
         "candidate_branch": "candidate_branch",
         "candidate_degree": "candidate_degree",
         "candidate_university": "candidate_university",
         "candidate_contact_number": "9923704608",
         "disclaimer": "on",
         "slug": "dkjhfkdfjhg"
     })

def login(l):
    l.client.post("/users/sign_in/", {"user[email]":"abhimanyu@interviewbit.com", "user[password]":"12!@abAB<>"})

def logout(l):
    l.client.post("/users/sign_out/", {"_method":"delete"})

def check_status(l, test_id, problem_id, submission_id):
    response = l.client.get("/test/" + str(test_id) + "/status/?problem_id=" + str(problem_id) + "&submission_id=" + str(submission_id))

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
        programming_language_id = 511#supported_languages[random.randint(0,(len(supported_languages) - 1))]
        response = self.client.post("/test/" + str(test_id) + "/save-code/", {
            "problem_id": problem_id, 
            "programming_language_id": 511,
            "is_objective": 'false',
            "problem_code": problem_codes[problem_id][2]
        })

    # #Submit Code
    @task(80)
    def submit_code(self):
        problem_id = problem_ids[random.randint(0,(len(problem_ids) - 1))]
        supported_languages = problem_language_id_map[problem_id]
        programming_language_id = supported_languages[random.randint(0,(len(supported_languages) - 1))]

        response = self.client.post("/test/" + test_id + "/evaluate-code/", {
            "problem_id": problem_id, 
            "programming_language_id": 511,
            "submission_content": problem_codes[problem_id][2],
            "submission_type": 'submit'
        }, {
            'X-Requested-With': 'XMLHttpRequest'
        })        
        logger.info(response.content)
        resp_json = json.loads(response.content)

        for i in range(1,30):
            #check_status(self, test_id, problem_id, resp_json['submission_id'])
            r = Timer(i, check_status, (self, test_id, problem_id, resp_json['submission_id']))
            r.start()

    #get submission status
    #@task(2400)
    #def submission_status(self):                    
        #response = self.client.get("/test/" + str(test_id) + "/status/?problem_id=" + str(problem_id) + "&submission_id=" + str(response.submission_id))        

    #session poll
    @task(4000)
    def session_poll(self):
        response = self.client.get("/test/" + str(test_id) + "/poll/?current_duration=30" + "&current_extra_time=0")

class MyLocust(HttpLocust):
    host = os.getenv('TARGET_URL', "http://localhost:3000")
    task_set = MyTaskSet
    min_wait = 90
    max_wait = 100
