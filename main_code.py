from typing_extensions import runtime
import imdb
from googleapiclient.discovery import build
from google.oauth2 import service_account
import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import urllib.parse
import random
import timeit


# Class for creating a dictionary for movies, seen, and liked
class Sheet: 
    def __init__(self, values):
        rows = values
        self.movie_cell = 0
        self.seen_cell = 0
        self.liked_cell = 0
        self.runtime_cell = 0
        self.genre_cell = 0
        self.rating_cell = 0
        self.id_cell = 0
        

        for i, cell in enumerate(rows[0]):
            if cell == 'id':
                self.id_cell = i
            if cell == 'Movies':
                self.movie_cell = i
            if cell == 'Seen':
                self.seen_cell = i
            if cell == 'Liked':
                self.liked_cell = i
            if cell == 'Runtime':
                self.runtime_cell = i
            if cell == 'Genre':
                self.genre_cell = i
            if cell == 'Rating':
                self.rating_cell = i

        # Check how many people are in the database
        self.number_of_people = self.liked_cell - self.seen_cell
        self.names = []

        #Names into self.names
        for i in range(self.number_of_people):
            self.names.append(rows[1][5 + i])
        self.sheet = {}

        #Names in format of [name]: {'Seen':[], 'Liked': []}
        for name in self.names:
            self.sheet[name] = {'Seen': [], 'Liked': []}

        
        #Append movies to format above
        self.movies_data = {}

        for row in rows[2:]:
            if row[self.id_cell] != '':
                id = str(row[self.id_cell])
                self.movies_data[id] = {}

                if row[self.movie_cell] != '' and row[self.movie_cell] is not None:
                    movie = str(row[self.movie_cell])
                    self.movies_data[id]['Title'] = encode_str(movie)

            
                # Get runtimes from database
                if row[self.runtime_cell] != '' and row[self.runtime_cell] is not None and row[self.runtime_cell] != 'Time Null':
                    hours = str(row[self.runtime_cell])
                    runtime = hours_to_min(hours)
                    self.movies_data[id]['Runtime'] = runtime

                # Get genres from database
                if row[self.genre_cell] != '' and row[self.genre_cell] is not None and row[self.genre_cell] != 'Genre Null':
                    genre = (row[self.genre_cell])
                    self.movies_data[id]['Genres'] = genre.split(',')

                # Get ratings from database
                if row[self.rating_cell] != '' and row[self.rating_cell] is not None and row[self.rating_cell] != 'Rating Null':
                    rating = str(row[self.rating_cell])
                    self.movies_data[id]['Rating'] = float(rating)
                
                #Append seen movies to format
                seen_list = []
                for i, cell in enumerate(row[self.seen_cell: self.number_of_people + 5]):
                    name = self.names[i]
                    if cell == 'TRUE':
                        seen_list.append(name)
                self.movies_data[id]['Seen'] = seen_list

                #Append liked movies to format
                liked_list = []
                for i, cell in enumerate(
                        row[self.number_of_people + 5:
                            2 * self.number_of_people + 5]):
                    name = self.names[i]
                    if cell == 'TRUE':
                        liked_list.append(name)
                self.movies_data[id]['Liked'] = liked_list
        
# Get information form imdb and return runtimes and genres
def imdb_API(movie):
    ia = imdb.IMDb()
    try:
        # Try to search movie in imdb
        search = ia.search_movie(movie) #To get value from list of lists
        id = search[0].movieID
        movie = ia.get_movie(id)
        print(movie)
        # Get runtime
        runtime = int(movie.data['runtimes'][0])
    except KeyError:
        runtime = 0
    # Get genres
    try:
        genreList = movie.data['genres']
    except KeyError:
        genreList = ['Comedy']
    
    # Get ratings
    try:
        rating = movie.data['rating']
    except KeyError:
        rating = 0

    return runtime, genreList, rating

# Change hours to minutes
def hours_to_min(time):
    try:
        hours = (re.findall('([0-9]+)h',time))
        hours = int(hours[0]) * 60
    except IndexError:
        hours = 0
    try:
        min = re.findall(' ([0-9]+).*',time)
        min = int(min[0])
    except IndexError:
        min = 0
    minutes = hours+min
    return minutes

# Read and write to google sheet
def read_database(spreadsheet_range):
    SERVICE_ACCOUNT_FILE = 'keys.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    creds = None
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID = '167p9oeTPaaWLjNnlw24o_Av7rCSQNU0NGDAxzsXVKjM' #sheet id

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range= spreadsheet_range ).execute()

    values = result.get('values', [])

    return SPREADSHEET_ID, service, values

# Write run times and genres to spread sheet
def write_tosheet(SPREADSHEET_ID, service, min_range, movie_name, runtime_list, genre_list, rating_list,count):
    MOVIE_RANGE = "Movies!A"
    TIME_RANGE = "Movies!B" 
    GENRE_RANGE = "Movies!C" 
    RATING_RANGE = "Movies!D"

    # Write onto google sheet
    if movie_name != None:
        request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, 
                                range=(MOVIE_RANGE) + str(min_range + count), valueInputOption="USER_ENTERED", body={"values":(movie_name)}).execute()
    if runtime_list != None:
        request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, 
                                range=(TIME_RANGE) + str(min_range + count), valueInputOption="USER_ENTERED", body={"values":(runtime_list)}).execute()
    if genre_list != None:
        request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, 
                                range=(GENRE_RANGE) + str(min_range + count), valueInputOption="USER_ENTERED", body={"values":(genre_list)}).execute()  
    if rating_list != None:
        request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, 
                                range=(RATING_RANGE) + str(min_range + count), valueInputOption="USER_ENTERED", body={"values":(rating_list)}).execute()  

# Filter Categories 
def filter(unseen, seen, liked, include_genre, exclude_genre, min_rating, max_runtime):
	def Unseen(id):
		# if there is any movie in the unseen list that is in the seen list of the movie: return false
		if 'Seen' in movieDatabase[id].keys():
			return not any(i in movieDatabase[id]['Seen'] for i in unseen)
		return True
	
	def Seen(id):
		# if all of the items in the seen list are in the seenList list: return true
		if 'Seen' in movieDatabase[id].keys():
			return all(i in movieDatabase[id]['Seen'] for i in seen)
		return True
	
	def IncludeGenres(id):
		# if there are all elements in include_genre are in the genreList: return true
		return all(i in movieDatabase[id]['Genres'] for i in include_genre)

	def ExcludeGenres(id):
		# if there are any elements int he exclude_genre list inside of the genreList list: return false
		return not any(i in movieDatabase[id]['Genres'] for i in exclude_genre)

	def MinRating(id):
		# if the movie rating is greater or equal to the minimum rating: return true
		return movieDatabase[id]['Rating'] >= min_rating

	def MaxRuntime(id):
        # if the movie runtime is less or equal to the max runtime: return true
		return movieDatabase[id]['Runtime'] <= max_runtime
	
	def Liked(id):
		if 'Liked' in movieDatabase[id].keys():
			return all(i in movieDatabase[id]['Liked'] for i in liked)
		return True

	filteredMovies = []
	for id in movieDatabase:
		if (Unseen(id) and Seen(id) and IncludeGenres(id) and ExcludeGenres(id) and MinRating(id) and MaxRuntime(id) and Liked(id)):
			filteredMovies.append(decode_str(movieDatabase[id]['Title'])) # decode movie for special characters that may be included
	return filteredMovies
     



# Encode string for special characters
def encode_str(movie):
    if '.' in movie:
        movie = movie.replace('.','%2E')
    encoded = urllib.parse.quote(movie,safe=' ',encoding='utf-8')
    return encoded

# Decode string for special characters
def decode_str(movie):
    decoded = urllib.parse.unquote(movie)
    decode = urllib.parse.unquote(decoded)
    return decode

# Move sheet database to firebase
def sheet_to_database():
    for i in database.movies_data:
        if len(database.movies_data[i]['Seen']) != 0:
            if len(database.movies_data[i]['Liked']) != 0:

                data = {
                        'Title':database.movies_data[i]['Title'],
                        'Runtime':database.movies_data[i]['Runtime'],
                        'Genre':database.movies_data[i]['Genres'],
                        'Rating':database.movies_data[i]['Rating'],
                        'Seen':database.movies_data[i]['Seen'],
                        'Liked':database.movies_data[i]['Liked']
                        }
            elif len(database.movies_data[i]['Liked']) == 0:
                data = {
                            'Title':database.movies_data[i]['Title'],
                            'Runtime':database.movies_data[i]['Runtime'],
                            'Genre':database.movies_data[i]['Genres'],
                            'Rating':database.movies_data[i]['Rating'],
                            'Seen':database.movies_data[i]['Seen']
                            }
        elif len(database.movies_data[i]['Seen']) == 0:

            data = {
                            'Title':database.movies_data[i]['Title'],
                            'Runtime':database.movies_data[i]['Runtime'],
                            'Genre':database.movies_data[i]['Genres'],
                            'Rating':database.movies_data[i]['Rating']
                            }
        movie_id = i
        print((movie_id),data)
        ref.update({movie_id:data})

# add movie to a group
def add_movie(group):
    ia = imdb.IMDb()
    movie_list = []
    group_database = db.reference('/'+str(group))

    movie = input("Enter movie name: ")


    search = ia.search_movie(movie) #To get value from list of lists
    for i in range(5):
        id = search[i].movieID
        movie = ia.get_movie(id)
        try:
        # Get runtime
            runtime = int(movie.data['runtimes'][0])
        except KeyError:
            runtime = 0
        # Get genres
        try:
            genreList = movie.data['genres']
        except KeyError:
            genreList = ['Comedy']
        # Get ratings
        try:
            rating = movie.data['rating']
        except KeyError:
            rating = 0
        movie_list.append([movie,runtime,genreList,rating])

        print(i+1,".",movie,' :Runtime:',runtime,', Genres:',genreList,', Rating:',rating)
    index = int(input("Enter the number you would like to add: ")) - 1
    try:
        movie_data = movieDatabase[str(search[index])]
        print("Movie already added ",search[index],":",movie_data)
    except KeyError:
        print("Adding: ",search[index])
        data = {'Runtime':movie_list[index][1],'Genre':movie_list[index][2],'Rating':movie_list[index][3]}
        group_database.update({search[index]:data})

# Remove movie from a group
def remove_movie(id,group):
    database_group = db.reference('/'+str(group))
    database_group.child(id).set([])

# Add a group to the main database
def add_group(name):
    database_name = db.reference('/'+str(name))
    data = {"Title": "Titanic","Runtime":194,"Genre": ['Drama','Romance'],"Rating":7.8}
    database_name.update({int("0120338"):data})

# Remove a group form the main database
def remove_group(name):
    database_name = db.reference('/')
    database_name.child(str(name)).set([])

# Search movie id
def imdb_id(movie):
    ia = imdb.IMDb()
    
    # Try to search movie in imdb
    search = ia.search_movie(movie) #To get value from list of lists
    id = search[0].movieID
    movie = ia.get_movie(id)
    id = movie.movieID
    return id

# Choose 5 random movies from given list
def random_moives(movie_list):
    sample_list = random.choices(movie_list, k=5)
    return sample_list

# Add people that have seen movie
def add_seen(name,group,movie_id):
    name = str(name)
    group = str(group)
    movie_id = str(movie_id)

    ref = db.reference('/'+str(group))
    group_database = ref.get()
    user_ref = ref.child(movie_id)
    try:
        seen_list = group_database[movie_id]['Seen']
        seen_list.append(str(name))
    except KeyError:
        seen_list = [name]
    user_ref.update({'Seen':seen_list})




#####FILTERSSSS######
#alphabetical movies.
def alphaAZ():
    alphaData = sorted(movieDatabase.items(), key = lambda x: x[1]['Title'])
    return alphaData

def alphaZA():
    alphaData = sorted(movieDatabase.items(), key = lambda x: x[1]['Title'], reverse=True)
    return alphaData
    
#Runtime of movies
#low runtime to high
def movieRunTimeLH():
    timeData = sorted(movieDatabase.items(), key = lambda x: x[1]['Runtime'])
    return timeData

#high runtime to low
def movieRunTimeHl():
    timeData = sorted(movieDatabase.items(), key=lambda x: x[1]['Runtime'], reverse=True)
    return timeData

#Ratings
#low to high
def movieRatingsLH():
    rateingData = sorted(movieDatabase.items(), key=lambda x: x[1]['Rating'])
    return rateingData

#high to low
def movieRatingsHL():
    rateingData = sorted(movieDatabase.items(), key=lambda x: x[1]['Rating'], reverse=True)
    return rateingData





# ------TESTING AREA------ #
# Read google sheets
# SPREADSHEET_ID, service, values = read_database('Movies!A1:O657')

# print(values)
# database = Sheet(values)
# print(database.movies_data)
cred = credentials.Certificate("firebasekey.json")
firebase_admin.initialize_app(cred, {'databaseURL' : 'https://movie-database-d01fd-default-rtdb.firebaseio.com/'})
ref = db.reference('/group1')
movieDatabase = ref.get()
print(movieDatabase)