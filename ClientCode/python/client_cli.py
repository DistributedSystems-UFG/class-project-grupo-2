import argparse
import pickle


parser = argparse.ArgumentParser(description='Interface CLI para clientes gRPC')
parser.add_argument('--login', '-l', dest='login', required=False)

args = parser.parse_args()

data = ['', '']  # [login, password]
if args.login or args.password:
    with open('.credentials', 'rb') as f:
        data = pickle.loads(f.read())

        print(data)

if args.login:
    data[0] = args.login
    with open('.credentials', 'wb') as f:
        f.write(pickle.dumps(data))

if args.password:
    data[1] = args.password
    with open('.credentials', 'wb') as f:
        f.write(pickle.dumps(data))