import os
import string
import random
import sys
import logging
import json
import datetime
import gevent
import websocket
from locust import HttpLocust, TaskSet, task, events, Locust
from threading import Timer
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('INIT')

#test data
global test_id
test_id = '5645c712df' #8a2c3d05c2 local, 5645c712df staging
problem_ids = [228, 382, 900, 1195, 1262]
program_languages_random_map = [44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 116, 116, 511]
problem_language_id_map = {
  228: program_languages_random_map,
  382: program_languages_random_map,
  900: program_languages_random_map,
  1195: program_languages_random_map,
  1262: program_languages_random_map,
}
random_matrix = [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,3,3,3,4,4]

python_tle = """
class Solution: 
    # @param A : string 
    # @return a strings 
    def solve(self, A): 
        while True:
            continue
"""
python_mle = """
class Solution: 
  # @param A : string 
  # @return a strings 
  def solve(self, A): 
    Solution.solve(self, A)
"""
problem_codes = {
  228: {
      44: [
        'syntax error',
        'int Solution::isSymmetric(TreeNode* A) { return 0; }',
        'vector<int>ans; void inOrder(TreeNode* A) {if(A==NULL)return; inOrder(A->left); ans.push_back(A->val); inOrder(A->right);} int Solution::isSymmetric(TreeNode* A) {ans.clear();inOrder(A);int l=0;int r=ans.size()-1;while(l<r){if(ans[l]!=ans[r])return 0;l++;r--;}return 1;}',
        'int Solution::isSymmetric(TreeNode* A) { int i=1; while(true) {i+=1;} return 0; }',
        'int Solution::isSymmetric(TreeNode* A) { isSymmetric(A); }',
      ],
      116: [
        'syntax error',
"""
class Solution: 
  def isMirror(self,root1,root2): 
    if(root1==None and root2==None): 
      return True 
    if(root1 and root2 and root1.val==root2.val): 
      return self.isMirror(root1.left,root2.right) and self.isMirror(root1.right,root2.left) 
    return False 
  
  def isSymmetric(self, A): 
    if self.isMirror(A,A): 
      return 0
    return 0
""",
"""
class Solution: 
  def isMirror(self,root1,root2): 
    if(root1==None and root2==None): 
      return True 
    if(root1 and root2 and root1.val==root2.val): 
      return self.isMirror(root1.left,root2.right) and self.isMirror(root1.right,root2.left) 
    return False 
  
  def isSymmetric(self, A): 
    if self.isMirror(A,A): 
      return 1 
    return 0
""",
python_tle,
python_mle
      ],
      511: [
          'syntax error',
          'public class Solution {public int isSymmetric(TreeNode A) {return 0;}}',
          'public class Solution { boolean isMirror(TreeNode A,TreeNode B){ if(A==null && B==null) return true; if(A==null || B==null) return false; return (A.val==B.val && isMirror(A.left,B.right) && isMirror(A.right,B.left)); } public int isSymmetric(TreeNode A) { if(A==null) return 1; if(A.left==null && A.right==null) return 1; if(A.left==null || A.right==null) return 0; return (isMirror(A.left,A.right)?1:0); } }',
          'public class Solution {public int isSymmetric(TreeNode A) {int i=0;while (true) {i++;}}}',
          'public class Solution {public int isSymmetric(TreeNode A) {int s = isSymmetric(A);return 1;}}'
      ]
  },
  382: {
      44: [
        'syntax error',
        'vector<string> Solution::fizzBuzz(int A) {return 0;}',
        'vector<string> Solution::fizzBuzz(int A) {vector<string> ans;for (int num = 1; num <= A; num++) {if ((num % 3 == 0) && (num % 5 == 0)) {ans.push_back("FizzBuzz");} else if(num % 3 == 0) {ans.push_back("Fizz");} else if(num % 5 == 0) {ans.push_back("Buzz");} else {string numStr;for(int i = num; i > 0; i /= 10) {numStr = char((i % 10) + \'0\') + numStr;}ans.push_back(numStr);}}return ans;}',
        'vector<string> Solution::fizzBuzz(int A) { int i=1; while(true) {i+=1;} return 0; }',
        'vector<string> Solution::fizzBuzz(int A) {vector<string> s = fizzBuzz(A);}',
      ],
      116: [
        'syntax error',
"""
class Solution: 
  def fizzBuzz(self, A): 
    lst = [] 
    i=0 
    while i < A: 
      if(((i+1)%3 == 0) & ((i+1)%5 == 0)): 
        lst.append("FizzBuzz") 
      elif((i+1)%5 == 0): 
        lst.append("Buzz") 
      elif((i+1)%3 == 0): 
        lst.append("Fizz") 
      else: 
        lst.append(i+1) 
      i += 1 
    return []
""",
"""
class Solution: 
  def fizzBuzz(self, A): 
    lst = [] 
    i=0 
    while i < A: 
      if(((i+1)%3 == 0) & ((i+1)%5 == 0)): 
        lst.append("FizzBuzz") 
      elif((i+1)%5 == 0): 
        lst.append("Buzz") 
      elif((i+1)%3 == 0): 
        lst.append("Fizz") 
      else: 
        lst.append(i+1) 
      i += 1 
    return lst
""",
python_tle,
python_mle
      ],
      511: [
          'syntax error',
          'public class Solution {public ArrayList<String> fizzBuzz(int A) {ArrayList<String> al = new ArrayList();return al;} }',
          'public class Solution { public ArrayList<String> fizzBuzz(int A) { ArrayList<String> al = new ArrayList(); for (int i = 1 ; i <= A ; i++){ if ( i%3 == 0 && i%5 == 0 ){ al.add("FizzBuzz"); }else if ( i%3 == 0 ){ al.add("Fizz"); }else if ( i%5 == 0 ){ al.add("Buzz"); }else{ al.add(i+""); } } return al; } }',
          'public class Solution {public ArrayList<String> fizzBuzz(int A) {ArrayList<String> al = new ArrayList();int i = 0;while (true) {i+=1;}} }',
          'public class Solution {public ArrayList<String> fizzBuzz(int A) {ArrayList<String> al = new ArrayList();al = fizzBuzz(A);return al;} }'
      ]
  },
  900: {
      44: [
        'syntax error',
        'string Solution::solve(string A) {return 0;}',
        'string Solution::solve(string A) {string s;s=A;int j=s.length();int len=j;j=j-1;int count=0;int i=0;string ans;if (s == string(s.rbegin(), s.rend())){if(len%2==1)ans="YES";elseans="NO";}else{while(i<=j){if(s[i]!=s[j])count++;i++;j--;}if(count>1)ans="NO";elseans="YES";}return ans;}',
        'string Solution::solve(string A) { int i=1; while(true) {i+=1;} return 0; }',
        'string Solution::solve(string A) {string s = solve(A);}',
      ],
      116: [
        'syntax error',
"""
class Solution: 
# @param A : string 
# @return a strings 
  def solve(self, A): 
    a=A[::-1] 
    c=0 
    if len(A)==1: 
      return 'YES' 
    for i in range(len(A)//2): 
      if a[i]!=A[i]: 
        c+=1 
    return 'WA'
""",
"""
class Solution: 
  # @param A : string 
  # @return a strings 
  def solve(self, A): 
    a=A[::-1] 
    c=0 
    if len(A)==1: 
      return 'YES' 
    for i in range(len(A)//2): 
      if a[i]!=A[i]: 
        c+=1 
    if len(A)%2==0 and c==1: 
      return 'YES'
    if len(A)%2!=0 and c<=1: 
      return 'YES' 
    else: 
      return 'NO'
""",
python_tle,
python_mle
      ],
      511: [
          'syntax error',
          'public class Solution { public String solve(String A) {return "";} }',
          'public class Solution { public String solve(String A) { int count = 0; for(int i = 0;i<A.length()/2;i++){ if(A.charAt(i)!=A.charAt(A.length()-1-i))count++; } if(count==0 && A.length()%2==0)return "NO"; if(count<2)return "YES"; return "NO"; } }',
          'public class Solution { public String solve(String A) {int i=0;while (true) {i+=1;}} }',
          'public class Solution { public String solve(String A) {String s = solve(A);return "";} }'
      ]
  },
  1195: {
      44: [
        'syntax error',
        'int Solution::solve(vector<int> &A) {return 0;}',
        'int Solution::solve(vector<int> &A) {int ans = 0;int mini = 1e9, maxi = -1e9;for(auto &i : A) {mini = min(mini, i);maxi = max(maxi, i);}for(auto &i : A) {if(mini < i and i < maxi)ans += 1;}return ans;}',
        'int Solution::solve(vector<int> &A) { int i=1; while(true) {i+=1;} return 0; }',
        'int Solution::solve(vector<int> &A) {int s = solve(A);}',
      ],
      116: [
        'syntax error',
"""
class Solution:
  def solve(self, A):
    ans = 0
    mini = 1e9
    maxi = -1e9

    for i in A:
      mini = min(mini, i);
      maxi = max(maxi, i);

    for i in A:
      if mini < i and i < maxi:
        ans += 1;

    return 0
""",
"""
class Solution:
  def solve(self, A):
    ans = 0
    mini = 1e9
    maxi = -1e9

    for i in A:
      mini = min(mini, i);
      maxi = max(maxi, i);

    for i in A:
      if mini < i and i < maxi:
        ans += 1;

    return ans
""",
python_tle,
python_mle
      ],
      511: [
          'syntax error',
          'public class Solution { public int solve(ArrayList<Integer> A) {return 0;} }',
          'public class Solution { public int solve(ArrayList<Integer> A) { Collections.sort(A); int duplicate = 0;for(int i=1;i<A.size()-1;i++){ int n = A.get(i);if(n<A.get(A.size()-1) && A.get(0)<n) { duplicate++;} } return duplicate; } }',
          'public class Solution { public int solve(ArrayList<Integer> A) {int i=0;while (true) {i+=1;}} }',
          'public class Solution { public int solve(ArrayList<Integer> A) {int i=solve(A);return i;} }'
      ]
  },
  1262: {
      44: [
        'syntax error',
        'int Solution::solve(int A) {return 0;}',
        'int Solution::solve(int A) {return A == 2 ? 1 : 2;}',
        'int Solution::solve(int A) { int i=1; while(true) {i+=1;} return 0; }',
        'int Solution::solve(int A) {int s = solve(A);}',
      ],
      116: [
        'syntax error',
"""
class Solution: 
  def solve(self, A): 
    if A == 2: 
      return 1 
    else: 
      return 1
""",
"""
class Solution: 
  def solve(self, A): 
    if A == 2: 
      return 1 
    else: 
      return 2
""",
python_tle,
python_mle
      ],
      511: [
          'syntax error',
          'public class Solution {public int solve(int A) {return 0;}}',
          'public class Solution { public static boolean isPrime(int n){ for(int i=2;i<n;i++){ if(n%i==0){ return false; } } return true; } public int solve(int n) { int half=n/2; if(n<=2){ return 1; } while(!isPrime(half)){ half--; if(isPrime(half)){ break; } } int otherHalf=n-half; return 2; } }',
          'public class Solution {public int solve(int A) {int i=0;while (true) {i+=1;}}',
          'public class Solution {public int solve(int A) {int i=solve(A);return i;}}'
      ]
  }
}
max_users = 3
user = None

def set_user():
  global user, max_users
  user_num = str(random.randint(0, max_users))

  return {
    'email': "loadtestinterviewbit+" + user_num + "@gmail.com",
    'password': "12ABXYZ12",
    'slug': "loadtest-user-" + user_num
  }

def login(self, user):
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

  def connect(self, ws_url):
    self.ws = websocket.WebSocket()
    self.ws.settimeout(10)
    self.ws_url = ws_url
    self.ws.connect(self.url + self.ws_url)
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
    if end_point == 'dummy':
      return
    start_time = time.time()
    e = None
    try:
      self.send_with_response(payload)
    except Exception as exp:
      e = exp
      self.ws.close()
      self.connect(self.ws_url)
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
    user = set_user()
    ws_url = '/cable/?token=' + user['slug']
    self.client.connect(ws_url)

  def on_stop(self):
    self.client.on_close()

  @task(1)
  def dummy_action(self):
    self.client.send('dummy', {})

class WSLocust(Locust):
  host = os.getenv('WS_TARGET_HOST', "ws://localhost:3000")
  task_set = WSTaskSet
  min_wait = 0
  max_wait = 0

  # Initialise WS Client
  client = SocketClient(host)

class HTTPTaskSet(TaskSet):
  def on_start(self):
    user = set_user()
    login(self, user)

  def on_stop(self):
    logout(self)

  # # Live Test Index
  # @task(1)
  # def index(self):
  #   time_to_wait = 10
  #   start = time.time()
  #   response = self.client.get("/test/" + test_id + '/')
  #   end = time.time()
  #   if end - start > time_to_wait:
  #     self._sleep(start + time_to_wait - end)

  # # Get Live Problems
  # @task(1)
  # def get_live_problems(self):
  #   time_to_wait = 10
  #   start = time.time()
  #   response = self.client.get("/test/" + str(test_id) + "/live-problems/")
  #   end = time.time()
  #   if end - start > time_to_wait:
  #     self._sleep(start + time_to_wait - end)

  # Submit Code
  @task(1)
  def submit_code(self):
    problem_id = problem_ids[random.randint(0,(len(problem_ids) - 1))]
    supported_languages = problem_language_id_map[problem_id]
    programming_language_id = supported_languages[random.randint(0,(len(supported_languages) - 1))]

    response = self.client.post("/test/" + test_id + "/evaluate-code/", {
      "problem_id": problem_id, 
      "programming_language_id": programming_language_id,
      "submission_content": problem_codes[problem_id][programming_language_id][random.choice(random_matrix)],
      "submission_type": 'submit'
    }, {
      'X-Requested-With': 'XMLHttpRequest'
    })        
    # logger.info(response.content)
    resp_json = json.loads(response.content)
    r = Timer(10, check_status, (self, test_id, problem_id, resp_json['submission_id']))
    r.start()
    for i in range(1,30):
      check_status(self, test_id, problem_id, resp_json['submission_id'])
      r = Timer(i, check_status, (self, test_id, problem_id, resp_json['submission_id']))
      r.start()

class HTTPLocust(HttpLocust):
  host = os.getenv('TARGET_DOMAIN', "http://localhost:3000")
  task_set = HTTPTaskSet
  min_wait = 0
  max_wait = 0