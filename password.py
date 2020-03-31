import secrets
from threading import Timer, RLock
from multiprocessing import Process
from write_process import append_to_file
import string

class Password:
    password_plain = [] #The plain password in a list form

    raw_password = '' #The plain password in a string form

    password = []

    unknown_positions = []

    gui_update = None

    hints_on = True

    hint = True

    lock = None

    running = False

    timeLimit = 0.0

    delay = 0.0

    timers = []

    databases = {
        database: None,
        stored_db: None
    }

    def __init__(self, password, gui_update=None, delay=1.0, time_limit=5.0, length_limit=16, fixed_length=False, use_hint=True, starting_hint=True, database_path=database/db.txt, stored_path=database/stored.txt):
        if length_limit:
            pass
        self.databases[database] = database_path
        self.databases[stored_db] = stored_path
        self.set_password(password)
        self.gui_update = gui_update
        self.unknown_positions = list(range(0, len(self.password_plain)))
        self.lock = RLock()
        self.delay = delay
        self.timeLimit = time_limit
        self.hints_on = use_hint
        self.running = True
        self.hint = starting_hint
        self.timers = []
        self.set_timers()
        
    
    # Create the Timer objects, ready to be used
    def set_timers(self):
        self.timers.append(Timer(self.timeLimit, self.game_over).start())   #0
        if self.hints_on:
            self.timers.append(Timer(self.delay, self.run).start())             #1
            self.timers.append(Timer(self.delay, self.give_hint).start())       #2
    
    # Set a single timer, used to reset a timer.
    def set_timer(self, index, delay, func):
        self.timers[index] = Timer(delay, func).start()
            
    #Method to try and decrease time drift. Ideally, the two Timer threads are concurrent, so that the Timer is not set in the Thread giving the hint, but set in another Thread to prevent (most) drifting issues
    #The idea is to have a primitive scheduler that fits our purposes better.
    def run(self):
        self.timers_operator()
        """
        Code block for:
        - Creating Threads
        - Join()ing Threads - maybe
        - start threads
        """
    
    def timers_operator(self):
        if self.running and self.hints_on:
            self.set_timer(1, self.delay, self.timers_operator)
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
        self.raw_password = new_password
        self.password_plain = list(new_password)
        self.hide_password(new_password)

    def hide_password(self, string):
        self.password = list('*'*len(string))

    def get_password(self):
        return "".join(self.password)

    def get_password_plain(self):
        return "".join(self.password_plain)

    def give_hint(self):
        if len(self.unknown_positions) != 0 and self.running:
            with self.lock:
                self.hint = True

    def brute_force(self):
        vals = string.ascii_letters + string.digits + string.punctuation 
        repeat = False
        while self.running:
            val = secrets.choice(vals)
            with self.lock:
                position = secrets.choice(self.unknown_positions)
                if self.hint:
                    self.password[position] = self.password_plain[position]
                    self.unknown_positions.remove(position)
                    self.hint = False
                    repeat = True
            if repeat:
                repeat = False
                continue
            else:
                with self.lock:
                    if self.password_plain[position] == val:
                        self.password[position] = self.password_plain[position]
                        self.unknown_positions.remove(position)
                    else:
                        pass #add increment to stats?
     
    def database_search(self):
        with open(self.databases[database], 'r') as f:
            for line in f:
                if line[0:len(line)-1] == self.raw_password:
                    self.game_over()
    
    def stored_search(self):
        with open(self.databases[stored_db], 'r') as f:
            for line in f:
                if line[0:len(line)-1] == self.raw_password:
                    self.game_over() 

    def game_over(self):
        self.gui_update("GAME OVER")
        p = Process(target=append_to_file, args=(self.databases[stored_db], self.raw_password)) #Process because if something happens to the main program the save process will survive.
        p.start()
        self.stop()
        p.join()

    def get_pos(self):
        return self.unknown_positions
