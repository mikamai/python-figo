import pytest

from figo import FigoException
from figo import FigoSession
from figo.models import Service
from figo.models import LoginSettings

CREDENTIALS = ["figo", "figo"]
BANK_CODE = "90090042"
CLIENT_ERROR = 1000

def test_add_access(access_token):
    figo_session = FigoSession(access_token)
    print "### figo_session.user ###"
    print figo_session.user
    figo_session.add_access(CREDENTIALS)
    assert 1 == 2 #failed, but only to see the prints!

def test_get_accesses(access_token):
    figo_session = FigoSession(access_token)
    print "### figo_session.user ###"
    print figo_session.user
    accesses = figo_session.get_accesses()
    print "### ACCESSES ###"
    print accesses
    assert 1 == 2 #failed, but only to see the prints!

