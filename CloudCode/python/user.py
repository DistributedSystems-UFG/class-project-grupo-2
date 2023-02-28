import secrets

class User:
    def __init__(self, name, login, password):
        self.name = name
        self.login = login
        self.password = password
        self.set_authorizations()

    users = {
        "Alice": "senha123"
    }
    
    access_tokens = {
        "Alice": "69ace8a2-96a6-11ed-a1eb-0242ac120002",
        "Bob": "73a25f82-96aa-11ed-a1eb-0242ac120002",
    }
    authorizations = {
        "69ace8a2-96a6-11ed-a1eb-0242ac120002": ["led-red", "temperature-1"],
        "73a25f82-96aa-11ed-a1eb-0242ac120002": ["led-red", "led-green", "luminosity-1"]
    }

    def register(self, request):
        name = request.name
        login = request.login
        password = request.password

        if login not in self.users:
            self.users[login] = password
            print(self.users)
            self.access_tokens[login] = secrets.token_hex(20)
            print(self.access_tokens)
        else:
            print("login já cadastrado.")

    def set_authorizations(self):
        count = 0
        for token in self.access_tokens:
            if(count%2==0):
                self.authorizations[token] = ['lavanderia', 'sala', 'banheiro']
            else:
                self.authorizations[token] = ['cozinha', 'escritorio', 'quarto']
            count+=1
            print(self.authorizations, count)
    
