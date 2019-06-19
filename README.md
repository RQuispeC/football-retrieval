# Football retrieval project

## Dependecies

This proyect was developed and tested under a linux distribution, dependecies are:

* Python 3
* matplotlib
* jsonschema
* tqdm
* numpy
* pandas
* texttable
* gensim
* networkx
* joblib
* logging
* flask
* flask_cors

## Basics

basic previous steps

* Clone this repo

```
git clone https://github.com/RQuispeC/football-retrieval.git
```

* Download the file shared by the professor
* Create a directory `data` and unzip data in a directory `dados_futebol`. Final `data` should look like:
  ```
  data\
    dados_futebol\
      CapBotT1Suav.2d
      CapBotT1Vel.vel
      ...
      possecorfluT2.txt
  ```

* `main.py` has examples for comparing players, teams and positions using terminal interface

```
python3 main.py
```

results will be save in the directory `log/`

## Web interface

In order to start the web interface run

```
python3 server.py
```
