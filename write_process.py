def append_to_file(filename, string):
    print("Process to write file booting...")
    if filename is None or filename == "":
        print("String empty, process stopping...")
    else:
        with open(filename, 'a') as file:
            print("File opened")
            file.writelines(string+'\n')
    print("Process completed.")
    return

if __name__ == "__main__":
    append_to_file("database/test.txt", "first line")
    append_to_file("database/test.txt", "appended")
