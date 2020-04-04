import secrets
from threading import Thread, Timer, RLock
from multiprocessing import Process
from write_process import append_to_file
import string
import time

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
        "database": None,
        "stored_db": None
    }

    threads = {
        "brute_force": None,
        "database_search": None,
        "local_search": None,
    }

    stats = None

    #TODO: Delete globals after this line when done with Statistics class
    found = False

    count = 0 #Delete after testing

    #End delete here

    def __init__(self, password, gui_update=None, delay=1.0, time_limit=5.0, length_limit=16, fixed_length=False, use_hint=True, starting_hint=True, database_path="database/db.txt", stored_path="database/stored.txt"):
        if length_limit:
            pass
        self.gui_update = gui_update
        self.databases["database"] = database_path
        self.databases["stored_db"] = stored_path
        if password == '':
            print("Stopping game")
            self.game_over()
            return
        if self.stats == None:
            self.stats = self.Statistics()
        self.set_password(password)
        self.unknown_positions = list(range(0, len(self.password_plain)))
        self.lock = RLock()
        self.delay = delay
        self.timeLimit = time_limit
        self.hints_on = use_hint
        self.running = True
        self.hint = starting_hint
        self.timers = []
        self.found = False
        self.run()
    
    class Statistics:
        password_found = False
        
        letters_found = [] #list of tuples of (position, time found)

        hints_found = 0

        time_start = 0

        time_end = 0

        operators = {
            "brute force": 0,
            "database": 0,
            "local": 0,
            "unidentified": 0
        }

        def __init__(self):
            self.time_start = time.time()

        def found(self, winner):
            self.time_end = time.time()
            try:
                operators[winner] += 1
            except KeyError:
                operators["unidentified"] += 1
            self.password_found = True

        def found_letter(self, position):
            self.letters_found.append((position, time.time() - self.time_start))

        def found_hint(self):
            self.hints_found += 1

        def get_time(self):
            return self.time_end - self.time_start

        def get_letters_found(self):
            return len(self.letters_found) + self.hints_found

        #try and get an average of the time it takes to find a letter, hints are not counted.
        #The list must be sorted by time from lower to higher for this to work.
        def get_average_lt_found_time(self):
            total = 0
            previous = 0 #offset to get the interval between two findings
            for tp in self.letters_found:
                total += tp[1] - previous
                previous = tp[1]
            return total / len(self.letters_found)
        
        def reset(self):
            self.time_start = 0
            self.time_end = 0
            self.password_found = False
            self.letters_found = []
            self.hints_found = 0
        
        def total_reset(self):
            for key in self.operators:
                self.operators[key] = 0
            self.reset()
            

    # Set a single timer, used to reset a timer.
    def set_timer(self, index, delay, func):
        self.timers[index] = Timer(delay, func).start()
            
    def run(self):
        self.threads["brute_force"] = Thread(target = self.brute_force)
        self.threads["database_search"] = Thread(target = self.database_search)
        self.threads["local_search"] = Thread(target = self.stored_search)
        for t in self.threads:
            self.threads[t].start()
        self.timers.append(Timer(self.timeLimit, self.stop).start())       #0
        if self.hints_on:
            self.timers.append(Timer(self.delay, self.timers_operator).start()) #1
            self.timers.append(Timer(self.delay, self.give_hint).start())       #2
        self.threads["brute_force"].join()
        self.threads["database_search"].join()
        self.threads["local_search"].join()
        self.game_over()
    
    def timers_operator(self):
        if self.running and self.hints_on:
            self.set_timer(1, self.delay, self.timers_operator)
            self.set_timer(2, self.delay, self.give_hint)

    #Tells all threads to stop asap, and stop all timers.
    def stop(self):
        self.running = False
        for timer in self.timers:
            try:
                timer.cancel()
            except AttributeError:
                continue

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
                self.gui_update(str(self.timing+1))
                self.timing += 1

    def brute_force(self):
        vals = string.ascii_letters + string.digits + string.punctuation 
        repeat = False
        while self.running:
            val = secrets.choice(vals)
            with self.lock:
                if self.unknown_positions != []: # a redundant check made obsolete by the check put at the end of the loop, as this case should not be possible.
                    position = secrets.choice(self.unknown_positions)
                else:
                    position = None
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
                    if position is not None and self.password_plain[position] == val:
                        self.password[position] = self.password_plain[position]
                        self.unknown_positions.remove(position)
                    if self.unknown_positions == []:
                        self.found = True
                        self.stop()
                        """
                        Code block for:
                        - increment stats
                        - wrap up the execution
                        """
     
    def database_search(self):
        with open(self.databases['database'], 'r') as f:
            for line in f:
                if not self.running:
                    return
                if line[0:len(line)-1] == self.raw_password:
                    self.found = True
                    self.stop()
    
    def stored_search(self):
        with open(self.databases['stored_db'], 'r') as f:
            for line in f:
                if not self.running:
                    return
                if line[0:len(line)-1] == self.raw_password:
                    self.found = True
                    self.stop()

    def game_over(self):
        self.count += 1
        p = Process(target=append_to_file, args=(self.databases["stored_db"], self.raw_password)) #Process because if something happens to the main program the save process will survive.
        p.start()
        self.stop()
        print(self.count)
        self.gui_update("GAME OVER")
        p.join()
        

    def get_pos(self):
        return self.unknown_positions
