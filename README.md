# Tennis Predictor
Machine learning model with built-in platform for reading and analyzing tennis results.\
The project is part of my BSc Thesis, which compares popular ML algorithms.\
Many thanks to [Jeff Sackmann's repository](https://github.com/JeffSackmann/tennis_atp), which collects all ATP match data in a neat CSV format.

## Requirements
* Python:
	* scikit-learn
	* scikit-optimize
	* pandas
	* numpy
	* xgboost
	* joblib
	* flask
	* flask-cors
* Node.js and npm

## Installation
1. Clone this repository:  ```git clone https://github.com/Ziusz/tennis-predictor.git```
2. Install python dependencies via pip: ```pip install -r requirements.txt```
3. Initialize Jeff Sackmann's repository: ```git submodule update --init --recursive```
4. Initialize the data preprocessing script: ```python scripts/preprocess_data.py```
5. Initialize the model learning script (It might take several hours ¯\_(ツ)_/¯): ```python scripts/train_models.py```
6. If you want to use the web interface, install all frontend dependencies via npm: 
```bash
cd frontend
npm install
```

## Usage
### Command-line Interface
CLI has two commands:
* **evaluate**, to get stats and info about trained model: 
```bash
python scripts/cli.py evaluate <model_name>
# example:
python scripts/cli.py evaluate logistic_regression
```
* **predict**, to get probability of player1 winning calculated by all models: 
```bash
python scripts/cli.py predict <p1_hand> <p1_height> <p1_age> <p1_rank> <p1_rank_points> <p2_hand> <p2_height> <p2_age> <p2_rank> <p2_rank_points> <surface> <tourney_level> <tourney_round>
# example:
python scripts/cli.py predict L 180 25.5 14 3500 R 198 21 44 1250 Grass G R32
```
### API
There is also an optional API that allows to send HTTP requests to models.\
To turn on API you need to initialize api script: ```python scripts/api.py```\
There are 3 endpoints:
* GET: **/players**, which returns JSON with all players info
* GET: **/evaluate/<model_name>**, which returns JSON with metrics of chosen model
* POST: **/predict**, which returns JSON with probability of player1 winning calculated by all models
	Example body structure of request: 
	```json
	{
	  "player1": {
	    "hand": "R",
	    "height": 194,
	    "age": 25,
	    "rank": 11,
	    "rank_points": 4000
	  },
	  "player2": {
	    "hand": "L",
	    "height": 178,
	    "age": 19,
	    "rank": 150,
	    "rank_points": 35
	  },
	  "surface": "Hard",
	  "tourney_level": "A",
	  "round": "QF"
	}
	```
API runs on port 7771 by default.

### Web Interface
This is a frontend written in Vue.js, so it requires dependencies installed by npm. If you haven't installed them yet, go back to the last section of the installation description.\
It requires an initialized API to work.
To turn on frontend you need to initialize serve script: 
```bash
cd frontend
npm run serve
```
API runs on port 8080 by default.\
If you host the site locally, you can visit the URL http://localhost:8080.
![The website should look like this in your browser.](https://github.com/ziusz/tennis-predictor/blob/main/frontend/public/screenshot.png)

## Evaluation of models
### Current metrics
||Accuracy (%)|Precision (%)|Recall (%)|F1-score (%)|
|--|--|--|--|--|
|**Logistic regression**|64.81%|64.90%|64.51%|64.70%|
|**SVM**|51.04%|50.55%|95.81%|66.18%|
|**Random Forest**|70.78%|70.97%|70.34%|70.65%|
|**KNN**|65.95%|66.41%|64.54%|65.46%|
|**Gradient Boosting**|67.31%|67.31%|67.33%|67.32%|
|**XGBoost**|66.87%|66.87%|66.87%|66.87%|

Random Forest is definitely the best one at the moment.\
SVM has a very high recall rate, suggesting a problem with excessive false classifications.

### Current hyperparameters selected by Bayes Search
#### Logistic regression
|Hyperparameter|Value|
|--|--|
|C|10|
|max_iter|1203
|solver|saga

#### SVM
|Hyperparameter|Value|
|--|--|
|C|0.12842116071378784|
|coef0|0.006382660838799905
|gamma|auto
|kernel|poly
|max_iter|825

#### Random Forest
|Hyperparameter|Value|
|--|--|
|criterion|entropy|
|max_depth|15|
|max_features|log2|
|min_samples_leaf|7|
|min_samples_split|4|
|n_estimators|1000

#### KNN
|Hyperparameter|Value|
|--|--|
|algorithm|brute|
|leaf_size|20|
|n_neighbors|98|
|p|1|
|weights|uniform|

#### Gradient Boosting
|Hyperparameter|Value|
|--|--|
|learning_rate|0.03589451606571555|
|loss|log_loss|
|max_depth|4|
|max_features|log2|
|n_estimators|936|
|subsample|0.8033808791659816|

#### XGBoost
|Hyperparameter|Value|
|--|--|
|alpha|10|
|colsample_bytree|0.6758151134813088|
|eval_metric|rmsle|
|grow_policy|lossguide|
|lambda|0.4652332574590495|
|learning_rate|0.16017846170784672|
|max_depth|3|
|n_estimators|316|
|subsample|0.8|

## Acknowledgments
Project is built with:
* [Jeff Sackmann's ATP data repository](https://github.com/JeffSackmann/tennis_atp)
* [Scikit-Learn](https://scikit-learn.org/stable/)
* [Scikit-Optimize](https://scikit-optimize.github.io/stable/)
* [XGBoost for Python](https://xgboost.readthedocs.io/en/stable/python/python_intro.html)
* [Flask](https://flask.palletsprojects.com/)
* [Vue.js](https://vuejs.org/)
* [Pandas](https://pandas.pydata.org/)
* [NumPy](https://numpy.org/)
* [Joblib](https://joblib.readthedocs.io/en/stable/)
* [Flask-Cors](https://pypi.org/project/Flask-Cors/)
* [Seaborn](https://seaborn.pydata.org/)
* [Matplotlib](https://matplotlib.org/)

Inspirated by: [Ahlem Jouidi's Notebook](https://www.kaggle.com/code/ahlemj/predict-atp-tennis/notebook).

## License
<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1" alt=""></a><br /><a property="dct:title" rel="cc:attributionURL" href="https://github.com/ziusz/tennis-predictor">Tennis Predictor</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/ziusz">Ziusz</a> is licensed under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-NC-SA 4.0</a>.<br />Attribution of this project and <a href="">Jeff Sackmann's repository</a> is required. <br />Only noncommercial use of this project is permitted.<br />Adaptations must be shared under the same terms.</p>