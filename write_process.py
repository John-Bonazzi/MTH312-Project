def append_to_file(filename, string):
    with open(filename, 'a') as file:
        file.writelines(string+'\n')

if __name__ == "__main__":
    append_to_file("database/test.txt", "first line")
    append_to_file("database/test.txt", "appended")
