import logging

logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def append_to_file(filename, string, allow_empty=False, allow_duplicate = False, debug = True):
    if not debug:
        logging.disable(logging.DEBUG)
    logging.info("filename: " + filename + " || value: " + string + " || allow empty: " + str(allow_empty))
    logging.info("Process to write file booting...")
    write = True
    if filename is None or filename == "":
        logging.info("String empty, process stopping...")
        write = False
    elif not allow_duplicate:
        logging.info("Checking for duplicates...")
        try:
            with open(filename, 'r') as file:
                for line in file:
                    if string == line[0:-1]:
                        logging.info("Duplicate found, the process won't update the file...")
                        write = False
                        break
        except FileNotFoundError:
            logging.info("File not found, creating file...")
    if write:
        with open(filename, 'a') as file:
            logging.info("File opened...")
            if allow_empty or string != "":
                file.writelines(string+'\n')
    logging.info("Process completed.")
    return

if __name__ == "__main__":
    append_to_file("database/test.txt", "first line")
    append_to_file("database/test.txt", "appended")
