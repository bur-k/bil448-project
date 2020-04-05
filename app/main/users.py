import bcrypt

users = {}


def createUser(username, passwordHash, salt):
    if username not in users:
        users[username] = {
            "username": username, "passwordHash": passwordHash, "salt": salt
        }
    else:
        print("username exists")
        raise Exception(username)


def getUser(username):
    if username in users:
        print(users[username])
        return users[username]
    else:
        print("username not found in users")
        raise Exception(username)


def generateUsers():
    for i in range(0, 3):
        salt = bcrypt.gensalt()
        createUser("user" + str(i), bcrypt.hashpw(("pass"+str(i)).encode(), salt).decode(), salt.decode())
