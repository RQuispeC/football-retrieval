# Football retrieval project

basic previous steps

* Clone this repo
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

* `main.py` will control all our code
* Directory `football_lib` has the library we are going to implement

## Understanding the classes

* `Player` class has attributes: `x`, `y` and `id`.
* `Team` class stores a set of valid `Players`, a valid player as positions `x` and `y` inside the field.
* `Position` class implements `team_a`, `team_b`, `edges_team_a`, `edges_team_b` and `id`. The edges are build based on used-defined strategy.
* `Match` class implements the set of all the `Position` objects.

### Example in `main.py`

```
fpath = "data/dados_futebol/CapBotT1Suav.2d" #data of a match
save_dir = "log/" #directory for saving outputs

match = Match(fpath, edge_strategy_name='knn', k = 1) #read a match and create graph based on 'knn' strategy
plot_position(match[288], save_dir) #plot the position 288 of the match

match.update_edge_strategy(new_edge_strategy='threshold', thr = 40) #update graph edge strategy to threhold 
plot_position(match[289], save_dir) #plot the position 299 of the match
```