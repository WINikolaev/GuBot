import pickle

data = {
	'a': [1, 2.0, 3, 4+6j],
	'b': ("character string", b"byte string"),
	'c': {None, True, False}
}

with open('data.pickle', 'wb') as f:
	pickle.dump(data, f)

with open('data.pickle', 'rb') as f:
	data_new = pickle.load(f)

print(data_new)