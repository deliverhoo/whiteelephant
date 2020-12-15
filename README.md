# whiteelephant
Virtual White Elephant - Very rudimentary. Quick working protype.

# How to play
1. One person is the host (and does all of the below)
2. Everyone mails the host a photo of the gift (and their own photo - or host can add any photo)

# How to setup:
1. Clone this repository
2. Install python 3
3. python -m venv /path/to/new/virtual/environment
4. Run /path/to/new/virtual/environment/Source/activate
5. Go to main directory 
6. run: pip install -r requirements.txt

# Run server - continued from above
1. python manage.py makemigrations
2. python manage.py makemigrations mainapp
3. python manage.py migrate
4. python manage.py createsuperuser
5. python manage.py runserver

# Create a Game
1. Goto:  http://127.0.0.1:8000/admin or whatever IP and port assigned by manage.py
2. Click on Games > Add Game > Save
3. Click on Add Player > Add Name and Photo file name (will get to that later). Dont enter anything in the position. Leave it at 0
4. Add as many players as you want
5. Click on Game Properties > Select Game > Dont select anything else and click on Save.
6. Click on Gifts > Add Gift > Select Original Owner and Fill in Gift File Name and photo of gift wrap for that gift. Click on Save.
7. Add gifts for all players.

# Files setup
1. For each player, there is a photo file name (from above). Have a photo of size 128x128 pixels for each player with correct file name in static\players
2. For each gift, there are 3 photos
  a. Photo of gift thumbnail 128x128 pixels (same name as used when saving in database)
  b. Photo of actual gift (full size). Name should be same as saved in database above with `_big` added to the end of the file name. Gift photos should be inside: static\gifts
  c. Each gift should also have a wrap with the same name as specified while saving the gift. Gift wrap photos should be inside: static\giftboxes

There are example photos of gifts, gift boxes inside the respective directories. There are no example photos of players. Please add that.

# To Play Game:
1. When game was created, there is a game id. Go to http://127.0.0.1:8000/admin to look up the game id if you didn ttake note
2. Go to http://127.0.0.1:8000/game/<game_id>
3. Share screen in zoom or whereever. 
4. Click on Start Game when everyone is ready to start Game.
5. Reset Game will clear everything. There is no double confirmation so be careful.
6. The number is yellow is the sequence number that was randomly generated for that person.
7. Number in red is the number of times, the gift was stolen.
8. If Lock sign in Red, then that gift cannot be stolen.

# Rules for the Game:
1. Gift Value  - You decide. (Change that in the code) - Should have added it to the model but forgot.
2. Maximum 3 steals of any gift
3. Gift cannot be stolen in the same round
4. 1st player goes again - Last Round
