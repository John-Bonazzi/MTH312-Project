import secrets
from threading import Timer
import sched
import time

class Password:
    password_plain = []

    password = ''

    unknown_positions = []

    gui_update = None

    timer = None

    def __init__(self, password, gui_update=None, length_limit=16, fixed_length=False):
        if length_limit:
            pass
        self.set_password(password)
        self.gui_update = gui_update
        self.unknown_positions = list(range(0, len(self.password_plain)))
        """self.timer = sched.scheduler(time.time, time.sleep)
        self.timer.enter(5, 1, self.give_hint)
        self.timer.run()"""
        self.timer = Timer(1.0, self.give_hint)
        self.timer.start()
        

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
        # self.timer.enter(5, 1, self.give_hint)
        if len(self.unknown_positions) == 0:
            return None
        self.timer = Timer(1.0, self.give_hint)
        self.timer.start()
        position = secrets.choice(self.unknown_positions)
        self.password[position] = self.password_plain[position]
        self.unknown_positions.remove(position)
        if self.gui_update is not None:
            self.gui_update(self.get_password())
        #self.timer.start()

    def game_over():
        self.gui_update(self.get_password())

    def get_pos(self):
        return self.unknown_positions
