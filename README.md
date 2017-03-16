# march-madness
A model to predict the results of the NCAA Division I Men's Basketball Tournament bracket

### Instructions to run

`python bracket.py` will train the model for the 2017 tournament and output the predicted teams advancing to each round, moving backwards from the championship game to the first round.

### The model

For now this project employs a very simple model. A basic logistic regression or random forest model is used to compute the probability of a team beating another team in a head-to-head matchup using basic stats for each team. The full joint distribution for the entire bracket is then estimated using this head-to-head model and basic conditional probability to estimate the chances of each team advancing to each round.

Potential improvements may include using a more interesting model for head-to-head predictions and acquiring more data to improve the feature set, as tempo-free statistics and information about strength of schedule would probably improve results. I don't think the current features are informative enough on their own to make a model competitive with human predictions.

### The data

The following features are used for each team from 2003 to 2016:
- Points per game
- Opponents per game
- 3 point attempts per game
- 3 point %
- Free throws per game
- Free throw %
- Offensive Rebound %
- Defensive Rebound %
- Assists per game
- Turnovers per game
- Steals per game
- Blocks per game
- Fouls per game

These features are computed from historical data obtained from [Kaggle's March Madness contest](https://www.kaggle.com/c/march-machine-learning-mania-2017). The training data is included in the repo but not the Kaggle data it's computed from as I don't have the rights to distribute it.
