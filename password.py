import secrets
from threading import Timer, RLock

class Password:
    password_plain = []

    password = []

    unknown_positions = []

    gui_update = None

    delay = 0.0

    lock = None

    running = False

    timeLimit = 0.0

    timers = []

    def __init__(self, password, gui_update=None, delay=1.0, time_limit=5.0, length_limit=16, fixed_length=False):
        if length_limit:
            pass
        self.set_password(password)
        self.gui_update = gui_update
        self.unknown_positions = list(range(0, len(self.password_plain)))
        self.lock = RLock()
        self.delay = delay
        self.timeLimit = time_limit
        self.running = True
        self.timers = []
        self.set_timers()
    
    # Create the Timer objects, ready to be used
    def set_timers(self):
        self.timers.append(Timer(self.timeLimit, self.game_over).start())   #0
        self.timers.append(Timer(self.delay, self.run).start())             #1
        self.timers.append(Timer(self.delay, self.give_hint).start())       #2
    
    # Set a single timer, used to reset a timer.
    def set_timer(self, index, delay, func):
        self.timers[index] = Timer(delay, func).start()
            
    #Method to try and decrease time drift. Ideally, the two Timer threads are concurrent, so that the Timer is not set in the Thread giving the hint, but set in another Thread to prevent (most) drifting issues
    #The idea is to have a primitive scheduler that fits our purposes better.
    def run(self):
        if self.running:
            self.set_timer(1, self.delay, self.run)
            self.set_timer(2, self.delay, self.give_hint)

    #Stop the execution of the progam, and stop all timers.
    def stop(self):
        self.running = False
        for timer in self.timers:
            try:
                timer.cancel()
            except AttributeError:
                print("ERROR!")

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
        if len(self.unknown_positions) == 0:
            return None
        with self.lock:
            position = secrets.choice(self.unknown_positions)
            self.password[position] = self.password_plain[position]
            self.unknown_positions.remove(position)
        if self.gui_update is not None and self.running:
            self.gui_update(self.get_password())

    #Don't try to find the final password, but find a close match, give back some stats on the time it takes, etc...
    def breakPassword(self):
        with self.lock:
            pass

    def game_over(self):
        self.gui_update("GAME OVER")
        #Do something
        self.stop()

    def get_pos(self):
        return self.unknown_positions
