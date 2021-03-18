# Hypexblog
Open Source :heart: Blogging Platform For Community :dizzy:

# Notes

This project is still under `development`, so see you in the future!

# Features

Currently hypexblog only supports:

* [API User](#1)
* [API Comment](#2)
* [API Article](#4)
* [API Likes](#5)
* [API Bookmarks](#6)

# Usage

Clone this repository and move to it, e.g:

```sh
git clone https://github.com/aprilahijriyan/hypexblog --depth 1
cd hypexblog
```

To run this you need:

* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [Virtualenv](https://pypi.org/project/virtualenv/)

Assume that everything required is installed on your device.


## Running in development

Creating virtualenv

```sh
virtualenv venv
source venv/bin/activate
```

Prevents you from running in other modes, e.g production.

```
unset ZEMFROG_ENV
bash build.sh
```

Run the application

```
cd app
pip install -r requirements.txt
flask run
```

## Running in production

Set the `ZEMFROG_ENV` to `production`:

```sh
export ZEMFROG_ENV=production
```

Make sure you are in the root of the `hypexblog` directory.
And restart the application with `build.sh`

```sh
bash build.sh
```
