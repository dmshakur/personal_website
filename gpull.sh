# This file is slightly necessary in my development environment
# As this program was created in termux on an android phone
eval "$(ssh-agent -s)"
ssh-add flask_app
git pull
