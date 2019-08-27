import pytest
import time
import os

from figo.models import User
from figo.models import TaskState
from figo.models import TaskToken

from figo import FigoConnection
from figo import FigoSession
from figo import FigoException

from dotenv import load_dotenv
load_dotenv()

API_ENDPOINT = os.getenv("API_ENDPOINT")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

connection  = FigoConnection(CLIENT_ID, CLIENT_SECRET, "https://127.0.0.1/", api_endpoint=API_ENDPOINT)
CREDENTIALS =  { 'account_number' : "foobarbaz", 'pin' : "12345" }
CONSENT = { "recurring": True, "period": 90, "scopes": ["ACCOUNTS", "BALANCES", "TRANSACTIONS"], "accounts": [{ "id": "DE67900900424711951500", "currency": "EUR" }] }
ACCESS_METHOD_ID = "ae441170-b726-460c-af3c-b76756de00e0"
data = {}


def pytest_namespace():
  return {'session': '', 'token': '', 'access_id': '', 'sync_id': '', 'challenge_id': '', 'account_id': ''}

def test_add_user():
  response = connection.add_user("John Doe", "john.doe@example.com", "password")
  assert response == {}

def test_create_token_and_session():
  token = connection.credential_login("john.doe@example.com", "password")
  pytest.token = token["access_token"]
  assert pytest.token
  pytest.session = FigoSession(token["access_token"])
  assert pytest.session.user.full_name == "John Doe"

def test_add_access():
  response = pytest.session.add_access(ACCESS_METHOD_ID, CREDENTIALS, CONSENT)
  pytest.access_id = response["id"]
  assert response.has_key("id") == True

def test_add_access_with_wrong_access_id(access_token):
  figo_session = FigoSession(access_token)
  access_method_id = "pipo"
  response = figo_session.add_access(access_method_id,CREDENTIALS,CONSENT)
  assert response.has_key("error") == True

def test_get_accesses():
  accesses = pytest.session.get_accesses()
  print accesses
  assert len(accesses) > 0

def test_get_access():
  accesses = pytest.session.get_access(pytest.access_id)
  assert len(accesses) > 0

def test_add_sync():
  response = pytest.session.add_sync(pytest.access_id, None, None, None, None, None)
  #TODO: Add error and challenge in the response!!!
  pytest.sync_id = response["id"]
  assert response["status"] == 'QUEUED'

def test_get_synchronization_status():
  time.sleep(10)
  response = pytest.session.get_synchronization_status(pytest.access_id, pytest.sync_id)
  pytest.challenge_id = response["challenge"]["id"]
  assert response["status"] == "AWAIT_AUTH"

def test_solve_synchronization_challenge(access_token):
  payload = { "value": "111111" }
  response = pytest.session.solve_synchronization_challenge(pytest.access_id, pytest.sync_id, pytest.challenge_id, payload)
  assert response == {}

def test_get_sync_after_challenge():
  time.sleep(10)
  response = pytest.session.get_synchronization_status(pytest.access_id, pytest.sync_id)
  assert response["status"] == "COMPLETED"

def test_get_synchronization_challenges():
  response = pytest.session.get_synchronization_challenges(pytest.access_id, pytest.sync_id)
  assert len(response) > 0

def test_get_synchronization_challenge():
  response = pytest.session.get_synchronization_challenge(pytest.access_id, pytest.sync_id, pytest.challenge_id)
  assert len(response) > 0

def test_get_accounts():
  response = pytest.session.get_accounts()
  pytest.account_id = response["accounts"][0]["account_id"]
  assert isinstance(response["accounts"][0]["account_id"], unicode)

def test_get_account():
  response = pytest.session.get_account(pytest.account_id)
  assert len(response) > 0

def test_get_account_balance():
  response = pytest.session.get_account_balance(pytest.account_id)
  assert response.balance == 0

def test_delete_account():
  response = pytest.session.remove_account(pytest.account_id)
  assert response == None

def test_remove_user():
  response = pytest.session.remove_user()
  assert response == {}