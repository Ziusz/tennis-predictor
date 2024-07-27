import sys
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

def load_helpers():
	encoders = {
		'player_hand': joblib.load('models/helpers/player_hand_encoder.joblib'),
		'opponent_hand': joblib.load('models/helpers/opponent_hand_encoder.joblib'),
		'surface': joblib.load('models/helpers/surface_binarizer.joblib'),
		'tourney_level': joblib.load('models/helpers/tourney_level_encoder.joblib'),
		'round': joblib.load('models/helpers/round_encoder.joblib'),
	}
	imputer = joblib.load('models/helpers/imputer.joblib')
	return encoders, imputer

def preprocess_input(data, encoders, imputer):
	df = pd.DataFrame(data)
	
	for column, encoder in encoders.items():
		if column in df.columns:
			df[column] = encoder.transform(df[column].astype(str))
	
	df = df.rename(str, axis="columns") 
	
	df = pd.DataFrame(imputer.transform(df), columns=df.columns)
	
	return df

def predict(player1, player2, surface, tourney_level, tourney_round):
	models = ['logistic_regression', 'svm', 'random_forest', 'knn', 'gradient_boosting', 'xgboost']
	
	match_data = {
		'surface': surface,
		'player_hand': player1['hand'],
		'player_ht': player1['height'],
		'player_age': player1['age'],
		'player_rank': player1['rank'],
		'player_rank_points': player1['rank_points'],
		'opponent_hand': player2['hand'],
		'opponent_ht': player2['height'],
		'opponent_age': player2['age'],
		'opponent_rank': player2['rank'],
		'opponent_rank_points': player2['rank_points'],
		'tourney_level': tourney_level,
		'round': tourney_round
	}

	encoders, imputer = load_helpers()

	surface_binarized = encoders['surface'].transform([match_data['surface']])
	match_data.update({cls: int(val) for cls, val in zip(encoders['surface'].classes_, surface_binarized[0])})

	del match_data['surface']

	match_df = preprocess_input([match_data], encoders, imputer)
	
	predictions = {}
	
	for model_name in models:
		model = joblib.load(f'models/{model_name}.joblib')
		if model_name != 'xgboost':
			model.feature_names_in_ = match_df.columns
		pred = model.predict_proba(match_df)[0][1]
		predictions[model_name] = pred
	
	return predictions

def evaluate(model_name):
	model = joblib.load(f'models/{model_name}.joblib')
	
	encoders, imputer = load_helpers()
	data = pd.read_csv('data/processed/final.csv')
	features = ['surface', 'player_hand', 'player_ht', 'player_age',
				'player_rank', 'player_rank_points', 'opponent_hand', 'opponent_ht', 'opponent_age',
				'opponent_rank', 'opponent_rank_points', 'tourney_level', 'round']
	
	X = data[features]
	y = data['result']
	
	X = X.copy()
	X['surface'] = X['surface'].astype(str)
	surface_binarized = encoders['surface'].transform(X['surface'])
	surface_df = pd.DataFrame(surface_binarized, columns=encoders['surface'].classes_)
	X = X.drop(columns=['surface']).join(surface_df)

	X_processed = preprocess_input(X.to_dict(orient='records'), encoders, imputer)
	
	if model_name != 'xgboost':
		model.feature_names_in_ = X_processed.columns

	y_pred = model.predict(X_processed)
	
	accuracy = accuracy_score(y, y_pred)
	precision = precision_score(y, y_pred)
	recall = recall_score(y, y_pred)
	f1 = f1_score(y, y_pred)
	
	print(confusion_matrix(y, y_pred))
	print(classification_report(y, y_pred))
	
	return {
		'accuracy': accuracy,
		'precision': precision,
		'recall': recall,
		'f1_score': f1,
	}


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Usage: python main.py [predict/evaluate] [args...]")
	else:
		command = sys.argv[1]
		
		if command == "predict" and len(sys.argv) == 15:
			player1 = {
				'hand': sys.argv[2],
				'height': int(sys.argv[3]),
				'age': float(sys.argv[4]),
				'rank': int(sys.argv[5]),
				'rank_points': int(sys.argv[6])
			}
			player2 = {
				'hand': sys.argv[7],
				'height': int(sys.argv[8]),
				'age': float(sys.argv[9]),
				'rank': int(sys.argv[10]),
				'rank_points': int(sys.argv[11])
			}
			surface = sys.argv[12]
			tourney_level = sys.argv[13]
			tourney_round = sys.argv[14]
			predictions = predict(player1, player2, surface, tourney_level, tourney_round)
			print(predictions)
		
		elif command == "evaluate" and len(sys.argv) == 3:
			model_name = sys.argv[2]
			metrics = evaluate(model_name)
			print(metrics)
		
		else:
			print("Invalid command or arguments.")
