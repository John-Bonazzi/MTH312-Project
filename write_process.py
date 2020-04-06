import logging

logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def append_to_file(filename, string, allow_empty=False, allow_duplicate = False, debug = False):
    if not debug:
        logging.disable(logging.DEBUG)
    logging.info("filename: " + filename + " || value: " + string + " || allow empty: " + str(allow_empty))
    logging.info("Process to write file booting...")
    if filename is None or filename == "":
        logging.info("String empty, process stopping...")
    else:
        with open(filename, 'a') as file:
            logging.info("File opened")
            if allow_empty or string != "":
                file.writelines(string+'\n')
    logging.info("Process completed.")
    return

if __name__ == "__main__":
    append_to_file("database/test.txt", "first line")
    append_to_file("database/test.txt", "appended")
