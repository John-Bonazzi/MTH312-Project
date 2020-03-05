class Password:
    password_plain = ''

    password = ''

    def __init__(self, password):
        self.set_password(password)

    def set_password(self, new_password):
        self.password_plain = new_password
        self.hide_password(self.password_plain)

    def hide_password(self, string):
        self.password = '*'*len(string)

    def get_password(self):
        return self.password

    def get_password_plain(self):
        return self.password_plain