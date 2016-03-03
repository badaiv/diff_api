# diff_api

Was tested on Ubuntu 14.04 using vagrant.

## Vgrant steps:
```bash 
vagrant init ubuntu/trusty64
vagrant up
vagrant ssh
```

## Ubuntu steps
```bash 
sudo apt-get install git python3-pip
sudo pip3 install virtualenv
virtualenv env
source ./env/bin/activate
pip install pytest flask
git clone https://github.com/badaiv/diff_api.git
```

## To run app
```bash 
python3 diff_api.py
```

## To run tests
```bash 
python3 -m py.test test_api.py
```
