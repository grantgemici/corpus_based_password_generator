import string, math, nltk, random, pickle,itertools, os.path, glob
from nltk.corpus import stopwords
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from password_strength import PasswordStats



def caesarfy (text, key, enc):
	new_string = ''
	if(enc):
		sign = 1
	else:
		sign = -1
	for i in text:
		if i.isupper():
			new_string += chr((ord(i) + sign * (key-65)) % 26 + 65)
		elif i == ' ':
			new_string += ' '
		elif i.isalpha() == False:
			print('non alphabetic character')
		else:
			new_string += chr((ord(i) + sign * (key - 97)) % 26 + 97)
	return new_string


def get_tokens(src):
	src_pkl = src + ".pkl"
	src_txt = src + ".txt"
	if os.path.isfile(src_pkl) == False:
		#getting stop words to remove
		stop_word = set(stopwords.words("english"))

		#initializing tokenizer
		tokenizer = RegexpTokenizer(r'\w+')

		#opening file
		with open(src_txt, encoding="utf8", errors='ignore') as f:
			file_content = f.read()

		#creating tokens
		tokens = tokenizer.tokenize(file_content)

		#replacing upper case w lower
		tokens = [x.lower() for x in tokens]

		#removing stop words
		for word in list(tokens):
		    if word in stop_word and word in tokens:
		        tokens.remove(word)
		    if word in ["verse","chorus","kanye","west"]:
		        tokens.remove(word)

		#shuffling
		random.shuffle(tokens)

		#saving to pkl
		pickle.dump(tokens, open(src_pkl, "wb" ))

	else:
		#loading file
		tokens = pickle.load( open( src_pkl, "rb" ) )

	counter = Counter(tokens)
	length = len(tokens) 
	least = math.floor(-(len(tokens) * .15 + 1))
	least_tokens = counter.most_common()[:least:-1]

	least_t = ['potato']

	for i in least_tokens:
		least_t.append(i[0])

	return least_t


def generate_password(src, site_name,id):
	least_t = get_tokens(src)
	
	seed = 0
	for i in caesarfy(site_name,-5, True):
		seed += ord(i)
	for i in id:
		seed += ord(i)
	#random.seed(seed)

	password = ''
	random.shuffle(least_t)
	while(len(password) <= 12):
		ind = random.randint(0, len(least_t)-1)
		password += least_t[ind].capitalize()

	#add num
	num = random.random()
	if(num < 0.5):
		password += random.choice(string.punctuation) + str(int(1000 * random.random()))
	else:
		password =  str(int(1000 * random.random())) + password + random.choice(string.punctuation)

	return password

def brute_force_guesser(password):
	for i in range(8,50):
		for possible_password in itertools.permutations(string.ascii_letters+string.digits+string.punctuation, i): 
			print(i);
			if(possible_password == password):
				print("Sucess");


def test_movies(id):
	movies = glob.glob("corpa/movies/*.txt")
	social_networks = ["Facebook", "WhatsApp", "QQ", "WeChat","QZone","Tumblr","Instagram","Twitter"]
	total_strength = 0
	total_weakness_factor = 0
	total = 0
	for i in movies:
		i = i[:-4]
		print(i[13:])
		for j in social_networks:
			p = generate_password(i,j,id)
			stats = PasswordStats(p)
			print('\t',p)
			total_strength += stats.strength()
			total_weakness_factor += stats.weakness_factor
			total += 1

	avg_s = total_strength / total
	avg_w = total_weakness_factor / total

	print("Average Strength:",avg_s)
	print("Average Strength:",avg_w)

# User has unique id (this one was taken from https://randomkeygen.com/)
id = "dpnMKnXkdDvntOcnbQKSlKOp4AcVzlPd"


#test_movies(id)


kanye = generate_password("corpa/music/kanye","Facebook",id)
twin_peaks = generate_password("corpa/movies/Twin+Peaks+-+Fire+Walk+With+Me","Facebook",id)

print("Kanye:",kanye)
print("Twin Peaks:",twin_peaks)
'''
stats = PasswordStats(kanye)
print("Strength:", stats.strength())
print("Weakness:", stats.weakness_factor)
stats = PasswordStats(twin_peaks)
print("Strength:", stats.strength())
print("Weakness:",stats.weakness_factor)
'''













