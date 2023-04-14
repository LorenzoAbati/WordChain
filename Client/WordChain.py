

import requests

import sys


# basic check email
# params = {"email": "lorenzo@gmail.com"}
#
# response = requests.get('http://localhost:8080/', params=params)

# game

print(sys.argv[1])

params = {"email": "lorenzo@gmail.com", "game_id": "18", "word": f"{sys.argv[1]}"}

response = requests.get('http://localhost:8080/game/', params=params)


# start



# params = {"email": "lorenzo@gmail.com"}
#
# response = requests.get('http://localhost:8080/start/', params=params)


# stop

# params = {"email": "lorenzo@gmail.com"}
#
# response = requests.get('http://localhost:8080/stop/', params=params)

print(response.status_code)
print(response.text)


# generally the steps the client should follow to play the game are:

# - /start, retrieve the game_id
# - /game, specifying the game_id, the word

