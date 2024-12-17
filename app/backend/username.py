
from backend.sharedate import SharedData

def get_username():
    shared_data = SharedData()
    username = shared_data.get_username()
    print(f"The username is: {username}")
    return username
