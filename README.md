# Jukebox development repository

### About
Mobile music sharing service

### Prerequisites
* Postgres
* Python 2.7
* Pip
* Virtualenv
* Virtualenvwrapper
* Autoenv

### Installation
Run the following set of commands in the directory where you would like to install Jukebox

```
$ mkvirtualenv jukebox
$ workon jukebox
$ git clone https://github.com/nliolios24/jukebox.git
$ cd jukebox
$ pip install -r requirements.txt
$ touch .env
```

Now, open `.env` in the text editor of your choice and add the following lines:
```
export DB_USER=\<postgres username\>
export DB_PASSWORD=\<postgres password\>
```

Leave this directory and cd back in. If you have autoenv installed properly, the contents of your .env file will be added to your path