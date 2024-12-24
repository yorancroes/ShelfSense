class SharedData:
    def __init__(self):
        self.username = ""

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username

    def set_password(self, password):
        self.password = password

    def get_password(self):
        return self.password

def set_credentials(shared_data, username, password):
    shared_data.set_username(username)
    shared_data.set_password(password)

def get_credentials(shared_data):
    username = shared_data.get_username()
    pasword = shared_data.get_password()

    print(username)
    print(password)


