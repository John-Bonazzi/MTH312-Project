import secrets
from threading import Timer

class Password:
    password_plain = []

    password = ''

    unknown_positions = []

    gui_update = None

    def __init__(self, password, gui_update=None, length_limit=16, fixed_length=False):
        if length_limit:
            pass
        self.set_password(password)
        self.gui_update = gui_update
        self.unknown_positions = list(range(0, len(self.password_plain)))
        t = Timer(3.0, self.give_hint)
        t.start()
        

    def set_password(self, new_password):
        self.password_plain = list(new_password)
        self.hide_password(new_password)

    def hide_password(self, string):
        self.password = list('*'*len(string))

    def get_password(self):
        return "".join(self.password)

    def get_password_plain(self):
        return "".join(self.password_plain)

    def give_hint(self):
        position = secrets.choice(self.unknown_positions)
        self.password[position] = self.password_plain[position]
        self.unknown_positions.remove(position)
        if self.gui_update is not None:
            self.gui_update(self.get_password())

    def get_pos(self):
        return self.unknown_positions
