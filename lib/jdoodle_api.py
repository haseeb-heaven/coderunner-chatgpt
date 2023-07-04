# JDoodle language codes.
# Credit - https://sl.bing.net/jbo456vZ8Eu
from datetime import datetime
import random
import string
import json
import requests

credit_spent_url = "https://api.jdoodle.com/v1/credit-spent"

lang_codes = {
  'c': 'c',
  'c++': 'cpp14',
  'cpp': 'cpp17',
  'python': 'python3',
  'go lang': 'go',
  'scala': 'scala',
  'bash shell': 'bash',
  'c#': 'csharp',
  'vb.net': 'vbn',
  'objectivec': 'objc',
  'swift': 'swift',
  'r language': 'r',
  'free basic': 'freebasic',
  'nodejs': 'nodejs',
  'java': 'java',
  'javascript': 'nodejs',
}

# Method to write logs to a file.
def write_log(log_msg:str):
  try:
    print(str(datetime.now()) + " " + log_msg)
  except Exception as e:
    print(str(e))

def generate_code_id(length=10):
  try:
    characters = string.ascii_letters + string.digits
    unique_id = ''.join(random.choice(characters) for i in range(length))
    return unique_id
  except Exception as e:
    write_log(e)
    return ""

# Method to get the JDoodle client ID and secret.
def get_jdoodle_client_1():
  client_id = '{}{}{}{}{}'.format('693e67ab', '032c', str(int('13')), 'c9',
                                  '0ff01e3dca2c6' + str(int('117')))
  client_secret = '{}{}{}{}{}{}{}{}'.format('c8870a78', '9a35e488', '2de3b383',
                                            '789e0801', '1a1456e8', '8dc58892',
                                            '61748d4b', '01d4a79d')
  return client_id, client_secret


def get_jdoodle_client_2():
  client_id = '{}{}{}{}'.format('e0c1fdfe', '9506fe7e', '35186a25', '9e36e5f5')
  client_secret = '{}{}{}{}{}{}'.format('e19a110c', '7ce8934c', '4f78017a',
                                        'acb55073', 'e3a0670c',
                                        'b871442dfcc40e28a40f66b3')
  return client_id, client_secret

def get_credits_used():
  try:
    write_log("get_credits_used: called")
    response = get_jdoodle_credit_spent()
    credit_spent = response.json()
    credits_used = 0
    write_log(f"get_credits_used response : {credit_spent}")

    if credit_spent:
      credits_used = credit_spent['used']
      write_log(f"get_credits_used Credits used: {credits_used}")

    return credits_used
  except Exception as e:
    write_log("Exception in get_credits_used: " + str(e))

# Method to get the JDoodle client.
def get_jdoodle_client():
  try:
    index = 1
    write_log(f"get_jdoodle_client: Getting jdoodle client {index}")
    credits_used = get_credits_used()
    if credits_used < 200:
      write_log("get_jdoodle_client: return client_1")
      return get_jdoodle_client_1()
    else:
      write_log("Credits exhaused for client_1")
      write_log("get_jdoodle_client: return client_2")
  except Exception as e:
    write_log(f"get_jdoodle_client: {e}")
    return get_jdoodle_client_2()


# Method to call the JDoodle "credit-spent" API.
def get_jdoodle_credit_spent():
  try:
    client_id, client_secret = get_jdoodle_client_1()
    headers = {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
    }

    body = {"clientId": client_id, "clientSecret": client_secret}
    write_log(f"get_jdoodle_credit_spent: sending request with url {credit_spent_url}")
    credit_spent = requests.post(credit_spent_url, headers=headers, data=json.dumps(body))
    write_log(f"get_jdoodle_credit_spent: {credit_spent}")
  except Exception as e:
    write_log(f"get_jdoodle_credit_spent: {e}")
  return credit_spent


