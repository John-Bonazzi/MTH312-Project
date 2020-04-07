import secrets
from threading import Thread, Timer, RLock
from multiprocessing import Process
from write_process import append_to_file
import string
import time
import logging
import itertools

logging.basicConfig(filename='log_password.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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

    length_limit = 0

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

    def __init__(self, password, gui_update=None, delay=1.0, time_limit=10.0, length_limit=12, fixed_length=False, use_hint=False, starting_hint=True, database_path="database/db.txt", stored_path="database/stored.txt"):
        logging.debug("password: " + password + " || delay: " + str(delay) + " || time limit: " + str(time_limit))
        self.length_limit = length_limit
        self.gui_update = gui_update
        self.databases["database"] = database_path
        self.databases["stored_db"] = stored_path
        if password == '':
            self.game_over()
            return
        if self.stats == None:
            self.stats = self.Statistics(len(password))
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
        operators = ["brute force", "database", "local", "unidentified"] #The name of each Thread that tries to break the password, with a default ['unidentified'] that is used internally to check for errors.
        
        indices = ["SAFE", "HIGH", "MEDIUM", "LOW"] #The name of each INDEX

        definitions = ['not broken','wow', 'ok', 'sigh'] #The definition for each INDEX, it follows the same order, first definition is for first INDEX and so forth.

        password_found = False
        
        letters_found = [] #list of tuples of (position, time found)

        password_length = 0

        hints_found = 0

        time_start = 0

        time_end = 0

        tries = {} #Map of password-breaking tries for each operator. if password is broken in 3 or less tries, it is low by default

        winner = -1

        winners_count = {}

        INDEX = {}

        def __init__(self, passw_length):
            self.time_start = time.time()
            self.password_length = passw_length
            self.build_dictionary(self.operators, [0] * len(self.operators), self.winners_count)
            self.build_dictionary(self.indices, self.definitions, self.INDEX)
            self.build_dictionary(self.operators, [0] * len(self.operators), self.tries)
        
        def build_dictionary(self, keys, values, pointer):
            for key, value in zip(keys, values):
                pointer[key] = value


        def found(self, winner = -1):
            self.time_end = time.time()
            try:
                self.winners_count[self.operators[winner]] += 1
            except KeyError:
                self.winners_count[self.operators[-1]] += 1
            self.winner = winner
            self.password_found = True

        def found_letter(self, position):
            self.letters_found.append((position, time.time() - self.time_start))

        def found_hint(self):
            self.hints_found += 1

        def get_time(self):
            return self.time_end - self.time_start

        def get_letters_found(self):
            return len(self.letters_found) + self.hints_found

        def get_INDEX(self):
            #key_position = 0
            key = 'LOW'
            operator = self.operators[self.winner]
            if not self.password_found: #TODO: change it so that it is safe based on how few letters brute force found (hints are not considered)
                key = "SAFE"
            elif self.tries[operator] <= 3:
                key = "LOW"
            elif self.winner == 2:
                key = "LOW"
            elif self.winner == 0:#TODO: complete this with brute force and something else
                key = "HIGH"
            elif self.winner == 0 or self.winner == 1:
                key = "MEDIUM"
            logging.debug("found: " + str(self.password_found) + " || tries: " + str(self.tries) + " || winner: " + self.operators[self.winner] + " || key: " + key)
            #key = self.indices[key_position]
            return (key, self.INDEX[key])

        def increase_tries(self, caller = -1):
            self.tries[self.operators[caller]] += 1

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
            self.winner = -1
            self.time_start = 0
            self.time_end = 0
            self.password_found = False
            self.letters_found = []
            self.hints_found = 0
            self.tries = {}
            self.build_dictionary(self.operators, [0] * len(self.operators), self.tries)
        
        def total_reset(self):
            for key in self.operators:
                self.operators[key] = 0
            self.reset()

        def who_won(self):
            return self.winner   

    # Set a single timer, used to reset a timer.
    def set_timer(self, index, delay, func):
        if self.running:
            self.timers[index] = Timer(delay, func).start()
            
    def run(self):
        self.threads["brute_force"] = Thread(target = self.brute_force)
        self.threads["database_search"] = Thread(target = self.database_search, args = ("database", self.stats.operators.index("database")))
        self.threads["local_search"] = Thread(target = self.database_search, args = ("stored_db", self.stats.operators.index("local")))
        self.timers.append(Timer(self.timeLimit, self.stop).start())       #0
        if self.hints_on:
            self.timers.append(Timer(self.delay, self.timers_operator).start()) #1
            self.timers.append(Timer(self.delay, self.give_hint).start())       #2
        for t in self.threads:
            self.threads[t].start()
        self.threads["brute_force"].join()
        self.threads["database_search"].join()
        self.threads["local_search"].join()
        self.game_over()
        logging.debug("PROGRAM COMPLETE")
    
    def timers_operator(self):
        if self.running and self.hints_on:
            self.set_timer(1, self.delay, self.timers_operator)
            self.set_timer(2, self.delay, self.give_hint)

    #Tells all threads to stop asap, and stop all timers.
    def stop(self):
        self.running = False
        for tmr in self.timers:
            try:
                logging.debug("Stopped a timer")
                tmr.cancel()
            except AttributeError as err:
                logging.debug("Timer could not be stopped, error: " + str(err))

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
        len_vals = len(vals)
        repeat = False
        for i in range(self.length_limit):
            if not self.running:
                logging.debug("BRUTE FORCE -- STOPPING EXECUTION")
                break
            max_iter = len_vals ** i
            if max_iter > 2000000:
                max_iter = 2000000
            permutations = itertools.islice(itertools.permutations(vals, i), max_iter)
            for perm in permutations:
                word = ''.join(perm)
                self.stats.increase_tries(0)
                if word == self.raw_password:
                    with self.lock:
                        if self.running:
                            self.stats.found(0)
                            self.stop()
                            break
            if not self.running:
                logging.debug("BRUTE FORCE -- EXECUTION STOPPED")
                break
        self.stop()
        logging.debug("Brute force stopped at words of length: " + str(i))
    
    def database_search(self, db_name, operator = -1):
        try:
            with open(self.databases[db_name], 'r') as f:
                for line in f:
                    if not self.running:
                        return
                    self.stats.increase_tries(operator)
                    if line[0:len(line)-1] == self.raw_password:
                        with self.lock:
                            if self.running:
                                self.stats.found(operator)
                                self.stop()
        except FileNotFoundError:
            return

    def game_over(self):
        logging.debug("GAME OVER -- STOPPING EXECUTION")
        join = False
        if self.stats.who_won != 1:
            p = Process(target=append_to_file, args=(self.databases["stored_db"], self.raw_password)) #Process because if something happens to the main program the save process will survive.
            p.start()
        self.stop()
        self.gui_update(self.stats.get_INDEX()) #FIXME: delete
        if join:
            p.join()
        logging.debug("GAME OVER -- EXECUTION STOPPED")
        
    def get_pos(self):
        return self.unknown_positions
