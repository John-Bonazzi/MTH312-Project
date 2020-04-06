from password import Password

def print_result(obj):
    print("The key is [" + str(obj[0]) + "]")
    print("The definition is [" + str(obj[1]) + "]")

if __name__ == "__main__":
    print("insert password:")
    pasw = input()
    runner = Password(password=pasw, gui_update=print_result)