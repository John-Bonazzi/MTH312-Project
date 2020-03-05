from password import Password

if __name__ == '__main__':
    passw = Password("hello")
    print(passw.get_password())
    print(passw.get_password_plain())