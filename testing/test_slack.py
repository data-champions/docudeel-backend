
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))
print(sys.path)
from src.slack import send_slack_message


def test_slack_works():
    assert send_slack_message('unit-test-docudeel')