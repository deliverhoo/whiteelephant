# whiteelephant
Virtual White Elephant

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
3. Click on Add Player > Add Name and Photo file name (will get to that later). Dont enter enything in the position. Leave it at 0
4. Add as many players as you want
5. Click on Game Properties > Select Game > Dont select anythign else and click on Save.
6. Click on Gifts > Add Gift > Select Original Owner and Fill in Gift File Name and photo og gift wrap for that gift. Click on Save.
7. Add gifts for all players.

# Files setup
1. For each player, there is a photo file name (from above). Have a photo of size 128x128 pixels for each player with correct file name in static\players
2. For each gift, there are 3 photos
  a. Photo of gift thumbnail 128x128 pixels (same name as used when saving in database)
  b. Photo of actual gift (full size). Name should be same as saved in database above with "_big_" added to the end of the file name. Gift photos should be inside: static\gifts
  c. Each gift should also have a wrap with the same name as specified while saving the gift. Gift wrap photos should be inside: static\giftboxes

There are example photos of gifts, gift boxes inside the respective directories. There are no example photos of players. Please add that.
