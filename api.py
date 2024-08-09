from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
from scripts.cli import load_helpers, preprocess_input, predict, evaluate

app = Flask(__name__)
CORS(app)

@app.route('/evaluate/<model_name>', methods=['GET'])
def evaluate_model(model_name):
	metrics = evaluate(model_name)
	return jsonify(metrics)

@app.route('/predict', methods=['POST'])
def predict_match():
	data = request.json
	player1 = data['player1']
	player2 = data['player2']
	surface = data['surface']
	tourney_level = data['tourney_level']
	tourney_round = data['round']
	predictions = predict(player1, player2, surface, tourney_level, tourney_round)
	predictions_cleared = {model: float(pred) for model, pred in predictions.items()}
	return jsonify(predictions_cleared)

@app.route('/players', methods=['GET'])
def players():
	players_df = pd.read_csv('data/raw/JeffSackmann@tennis_atp/atp_players.csv')
	rankings_df = pd.read_csv('data/raw/JeffSackmann@tennis_atp/atp_rankings_current.csv')
	final_df = pd.read_csv('data/processed/final.csv')
	
	valid_player_ids = set(final_df['player_id']).union(set(final_df['opponent_id']))
	players_df = players_df[players_df['player_id'].isin(valid_player_ids)]
	players_df = players_df.merge(rankings_df, left_on='player_id', right_on='player', how='left')

	players_df = players_df.drop_duplicates(subset='player_id')

	players_df = players_df.replace({np.nan: None})
	
	result = players_df.to_dict(orient='records')
	return jsonify(result)

if __name__ == '__main__':
	app.run(debug=True, port=7771)
