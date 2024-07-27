import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, LabelBinarizer
import xgboost as xgb
from sklearn.impute import SimpleImputer
from skopt import BayesSearchCV
from skopt.space import Real, Categorical, Integer
import joblib
import sys
import os

data = pd.read_csv('data/processed/final.csv')

features = ['surface', 'player_hand', 'player_ht', 'player_age',
			'player_rank', 'player_rank_points', 'opponent_hand', 'opponent_ht', 'opponent_age',
			'opponent_rank', 'opponent_rank_points', 'tourney_level', 'round']
X = data[features]
y = data['result']

player_hand_encoder = LabelEncoder().fit(X['player_hand'].astype(str))
opponent_hand_encoder = LabelEncoder().fit(X['opponent_hand'].astype(str))
surface_binarizer = LabelBinarizer().fit(X['surface'].astype(str))
tourney_level_encoder = LabelEncoder().fit(X['tourney_level'].astype(str))
round_encoder = LabelEncoder().fit(X['round'].astype(str))

joblib.dump(player_hand_encoder, 'models/helpers/player_hand_encoder.joblib')
joblib.dump(opponent_hand_encoder, 'models/helpers/opponent_hand_encoder.joblib')
joblib.dump(surface_binarizer, 'models/helpers/surface_binarizer.joblib')
joblib.dump(tourney_level_encoder, 'models/helpers/tourney_level_encoder.joblib')
joblib.dump(round_encoder, 'models/helpers/round_encoder.joblib')

surface_binarized = surface_binarizer.transform(X['surface'].astype(str))
surface_df = pd.DataFrame(surface_binarized, columns=surface_binarizer.classes_)

X = X.drop(columns=['surface'])
X = pd.concat([X, surface_df], axis=1)

X['player_hand'] = player_hand_encoder.transform(X['player_hand'].astype(str))
X['opponent_hand'] = opponent_hand_encoder.transform(X['opponent_hand'].astype(str))
X['tourney_level'] = tourney_level_encoder.transform(X['tourney_level'].astype(str))
X['round'] = round_encoder.transform(X['round'].astype(str))

imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)

joblib.dump(imputer, 'models/helpers/imputer.joblib')

X_train, y_train = X, y

param_spaces = {
	'logistic_regression': {
		'C': Real(0.1, 10.0, prior='log-uniform'),
		'max_iter': Integer(500, 1500),
		'solver': Categorical(['liblinear', 'saga', 'newton-cg', 'lbfgs']),
	},
	'svm': {
		'C': Real(0.1, 10.0, prior='log-uniform'),
		'max_iter': Integer(500, 1000),
		'kernel': Categorical(['rbf', 'poly', 'sigmoid']),
		'gamma': Categorical(['scale', 'auto']),
		'coef0': Real(0, 1)
	},
	'random_forest': {
		'n_estimators': Integer(100, 1000),
		'max_depth': Integer(10, 100),
		'criterion': Categorical(['gini', 'entropy', 'log_loss']),
		'min_samples_split': Integer(2, 10),
		'min_samples_leaf': Integer(1, 10),
		'max_features': Categorical(['sqrt', 'log2'])
	},
	'knn': {
		'n_neighbors': Integer(10, 100),
		'weights': Categorical(['uniform', 'distance']),
		'algorithm': Categorical(['ball_tree', 'kd_tree', 'brute']),
		'leaf_size': Integer(20, 50),
		'p': Categorical([1, 2])
	},
	'gradient_boosting': {
		'n_estimators': Integer(100, 1000),
		'max_depth': Integer(3, 10),
		'loss': Categorical(['log_loss', 'exponential']),
		'learning_rate': Real(0.01, 0.3),
		'subsample': Real(0.8, 1.0),
		'max_features': Categorical([None, 'sqrt', 'log2'])
	},
	'xgboost': {
		'n_estimators': Integer(100, 1000),
		'max_depth': Integer(3, 10),
		'grow_policy': Categorical(['depthwise', 'lossguide']),
		'eval_metric': Categorical(['rmse', 'rmsle', 'mae', 'mape', 'mphe', 'logloss', 'error', 'auc', 'aucpr', 'ndcg', 'map', 'gamma-deviance', 'cox-nloglik']),
		'learning_rate': Real(0.01, 0.3),
		'subsample': Real(0.8, 1.0),
		'colsample_bytree': Real(0.1, 1.0),
		'lambda': Real(0, 10),
		'alpha': Real(0, 10)
	}
}

models = {
	'logistic_regression': LogisticRegression(),
	'svm': SVC(probability=True),
	'random_forest': RandomForestClassifier(),
	'knn': KNeighborsClassifier(),
	'gradient_boosting': GradientBoostingClassifier(),
	'xgboost': xgb.XGBClassifier()
}

for model_name, model in models.items():
	print(f"Tuning hyperparameters for {model_name}...", end=" ")
	sys.stdout.flush()
	
	param_space = param_spaces[model_name]
	bayes_search = BayesSearchCV(model, param_space, n_iter=100, cv=4, n_jobs=-1, verbose=2, random_state=42, return_train_score=True)
	bayes_search.fit(X_train, y_train)
	
	best_model = bayes_search.best_estimator_
	joblib.dump(best_model, f'models/{model_name}.joblib')
	
	print("DONE!")

	results = bayes_search.cv_results_
	results_df = pd.DataFrame(results)
	results_df.to_csv(f'data/processed/bayes/{model_name}.csv', index=False)