
import os
import string
import random
import sys
import logging
import json
import datetime
import gevent
import websocket

from locust import HttpLocust, TaskSet, task, events
from threading import Timer
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('INIT')

#test data
global test_id
test_id = '8a2c3d05c2'

problem_ids = [1, 50]
problem_language_id_map = {
  1: [4, 11, 27, 35, 39, 42, 43, 44, 55, 114, 116, 510, 511, 512],
  50: [4, 11, 27, 35, 39, 42, 43, 44, 55, 114, 116, 510, 511, 512]
}

random_matrix = [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]

problem_codes = {
  1: [
    'syntax error',
    'public class Solution {public int canCompleteCircuit(final List<Integer> gas, final List<Integer> cost) {return 1;}}',
    'public class Solution {public int canCompleteCircuit(final List<Integer> gas, final List<Integer> cost) {int currentFuel = 0;int remaining = 0;int total = 0;int start = 0;for(int i = 0; i < gas.size(); i++){remaining = gas.get(i) - cost.get(i);if(currentFuel >= 0)currentFuel += remaining;else{currentFuel = remaining;start = i;}total += remaining;}return total >= 0 ? start : -1;}}'
  ],
  50: [
    'syntax error',
    'public class Solution {public ArrayList<Integer> slidingMaximum(final List<Integer> a, int b) {ArrayList<Integer> result = new ArrayList<>(); return result;}}',
    'public class Solution {public ArrayList<Integer> slidingMaximum(final List<Integer> a, int b) {ArrayList<Integer> result = new ArrayList<>();Deque<Integer> dq = new LinkedList<>();        for(int i=0; i<b; i++){while(!dq.isEmpty()&& a.get(dq.peekLast())<a.get(i))dq.pollLast();dq.offerLast(i);                }for(int i = b ; i<a.size() ; i++){result.add(a.get(dq.peekFirst()));int currWindowStartIndex = i-b+1;while(!dq.isEmpty() && dq.peek()<currWindowStartIndex)dq.pollFirst();while(!dq.isEmpty()&& a.get(dq.peekLast())<a.get(i))dq.pollLast();dq.offerLast(i);  }result.add(a.get(dq.peekFirst()));return result;}}'
  ]
}

# def signup(l):
#   global user_num
  
#   response = l.client.post("/test/a/load_test/", {
#       "candidate_email": "loadtestinterviewbit+" + user_num +  "@gmail.com",
#       "password": '12ABXYZ12',
#         "candidate_name": user_num,
#         "candidate_city": "Random",
#         "candidate_branch": "candidate_branch",
#         "candidate_degree": "candidate_degree",
#         "candidate_university": "candidate_university",
#         "candidate_contact_number": "9923704608"
#         })

#   l.client.post( "/test/" + test_id + '/' + "save-candidate-details",{
#       "candidate_email": "loadtestinterviewbit+" + user_num +  "@gmail.com",
#       "password": '12ABXYZ12',
#         "candidate_name": user_num,
#         "candidate_city": "Random",
#         "candidate_branch": "candidate_branch",
#         "candidate_degree": "candidate_degree",
#         "candidate_university": "candidate_university",
#         "candidate_contact_number": "9923704608",
#         "disclaimer": "on",
#         "slug": "dkjhfkdfjhg"
#     })

# class MyTaskSet(TaskSet):

    #record event
    # @task(33)
    # def record_event(self):
    #     response = self.client.post("/test/" + test_id + '/record-event/',{
    #         "event_type": "jhsdfgjdsf",
    #         "event_value": "kjdkjdhfgkjdfhgifderiuy eiruty idufgy difuyg",
    #         "timestamp": datetime.datetime.now()
    #     })

    #mark problem opened
    # @task(13)
    # def mark_problem_opened(self):
    #     problem_id = problem_ids[random.randint(0,(len(problem_ids) - 1))]
    #     response = self.client.post("/test/" + str(test_id) + "/mark-problem-opened/",{
    #         "problem_id": problem_id
    #     })


    #fetch code
    # @task(22)
    # def fetch_code(self):    
    #     problem_id = problem_ids[random.randint(0,(len(problem_ids) - 1))]
    #     supported_languages = problem_language_id_map[problem_id]
    #     programming_language_id = supported_languages[random.randint(0,(len(supported_languages) - 1))]
    #     response = self.client.get("/test/" + str(test_id) + "/get-code/?programming_language_id=" + str(programming_language_id) + "&problem_id=" + str(problem_id))

    # #save code
    # @task(52)
    # def save_code(self):
    #     problem_id = problem_ids[random.randint(0,(len(problem_ids) - 1))]
    #     supported_languages = problem_language_id_map[problem_id]
    #     programming_language_id = 511#supported_languages[random.randint(0,(len(supported_languages) - 1))]
    #     response = self.client.post("/test/" + str(test_id) + "/save-code/", {
    #         "problem_id": problem_id, 
    #         "programming_language_id": 511,
    #         "is_objective": 'false',
    #         "problem_code": problem_codes[problem_id][random.choice(random_matrix)]
    #     })

    #get submission status
    #@task(2400)
    #def submission_status(self):                    
        #response = self.client.get("/test/" + str(test_id) + "/status/?problem_id=" + str(problem_id) + "&submission_id=" + str(response.submission_id))        

    #session poll
    # @task(90)
    # def session_poll(self):
    #     response = self.client.get("/test/" + str(test_id) + "/poll/?current_duration=30" + "&current_extra_time=0")

max_users = 100000
user_num = str(random.randint(0, max_users))
user = None

def set_user():
  global user, user_num

  user = user or {
    'email': "loadtestinterviewbit+" + user_num + "@gmail.com",
    'password': "12ABXYZ12",
    'slug': "loadtest-user-" + user_num
  }

def login(self):
  global user

  self.client.post(
    "/users/sign_in/", 
    {
      "user[email]": user['email'],
      "user[password]": user['password']
    }
  )

def logout(self):
  self.client.post(
    "/users/sign_out/", 
    {"_method":"delete"}
  )

def check_status(self, test_id, problem_id, submission_id):
  self.client.get(
    "/test/" + test_id + "/status/?problem_id=" + problem_id + "&submission_id=" + submission_id
  )


class SocketClient(object):
  def __init__(self, url):
    self.url = url

  def connect(self):
    self.ws = websocket.WebSocket()
    self.ws.settimeout(10)
    self.ws.connect(self.url)

    events.quitting += self.on_close

    self.attach_session()

  def attach_session(self):
    payload = {
      "command": "subscribe",
      "identifier": "{\"channel\":\"AppearanceChannel\"}"
    }
    self.send('subscribe', payload)

  def send_with_response(self, payload):
    json_data = json.dumps(payload)

    g = gevent.spawn(self.ws.send, json_data)
    g.get(block=True, timeout=2)
    g = gevent.spawn(self.ws.recv)
    result = g.get(block=True, timeout=10)

    return json.loads(result)

  def on_close(self):
    self.ws.close()

  def send(self, end_point, payload):
    start_time = time.time()
    e = None
    try:
      self.send_with_response(payload)
    except Exception as exp:
      e = exp
      self.ws.close()
      self.connect()

    elapsed = int((time.time() - start_time) * 1000)

    if e:
      events.request_failure.fire(
        request_type='sockjs', name=end_point,
        response_time=elapsed, exception=e
      )
    else:
      events.request_success.fire(
        request_type='sockjs', name=end_point,
        response_time=elapsed, response_length=0
      )

class WSTaskSet(TaskSet):
  def on_start(self):
    # self.http_client.login(self.user)
    self.client.connect()

  def on_stop(self):
    self.client.on_close()

  @task(1)
  def action(self):
    data = {
      "action": "do_stuff",
      "param": "123",
    }
    self.client.send('action', data)

class WSLocust(HttpLocust):
  host = os.getenv('WS_TARGET_HOST', "ws://localhost:3000")
  task_set = WSTaskSet
  min_wait = 0
  max_wait = 0

  def __init__(self, *args, **kwargs):
    super(WSLocust, self).__init__(*args, **kwargs)

    set_user()

    # Initialise WS Client
    ws_url = self.host + '/cable/?token=' + user['slug']
    self.client = SocketClient(ws_url)

class HTTPTaskSet(TaskSet):
  def on_start(self):
    login(self)
  
  def on_stop(self):
    logout(self)

  # Live Test Index
  @task(10)
  def index(self):    
    time_to_wait = 10
    start = time.time()
    response = self.client.get("/test/" + test_id + '/')
    end = time.time()
    if end - start > time_to_wait:
      self._sleep(start + time_to_wait - end)

  # Get Live Problems
  @task(10)
  def get_live_problems(self):
    time_to_wait = 10
    start = time.time()
    response = self.client.get("/test/" + str(test_id) + "/live-problems/")
    end = time.time()
    if end - start > time_to_wait:
      self._sleep(start + time_to_wait - end)
  
  # Submit Code
  @task(22)
  def submit_code(self):
    problem_id = problem_ids[random.randint(0,(len(problem_ids) - 1))]
    supported_languages = problem_language_id_map[problem_id]
    programming_language_id = supported_languages[random.randint(0,(len(supported_languages) - 1))]

    response = self.client.post("/test/" + test_id + "/evaluate-code/", {
      "problem_id": problem_id, 
      "programming_language_id": 511,
      "submission_content": problem_codes[problem_id][random.choice(random_matrix)],
      "submission_type": 'submit'
    }, {
      'X-Requested-With': 'XMLHttpRequest'
    })        
    logger.info(response.content)
    resp_json = json.loads(response.content)

    r = Timer(10, check_status, (self, test_id, problem_id, resp_json['submission_id']))
    r.start()
    for i in range(1,30):
      check_status(self, test_id, problem_id, resp_json['submission_id'])
      r = Timer(i, check_status, (self, test_id, problem_id, resp_json['submission_id']))
      r.start()

class HTTPLocust(HttpLocust):
  host = os.getenv('TARGET_DOMAIN', "http://localhost:3000")
  set_user()

  task_set = HTTPTaskSet
  min_wait = 0
  max_wait = 0
