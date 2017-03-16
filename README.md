# march-madness
A model to predict the results of the NCAA Division I Men's Basketball Tournament bracket

For now this project employs a very simple model. A simple logistic regression model is used to compute the probability of a team beating another team in a head-to-head matchup using basic stats each team (e.g. Win %, PPG, FT%). The full joint distribution for the entire bracket is then estimated using this head-to-head model and basic conditional probability to estimate the chances of each team advancing to each round.

Potential improvements may include using a more interesting model for head-to-head predictions and acquiring more data to improve the feature set, as tempo-free statistics and information about strength of schedule would probably improve results.

### Instructions to run

`python bracket.py` will train the model for the 2017 tournament and output the predicted teams advancing to each round, moving backwards from the championship game to the first round.
