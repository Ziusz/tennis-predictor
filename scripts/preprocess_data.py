import pandas as pd
import glob
import os

def load_and_process_data(path_pattern):
	files = glob.glob(path_pattern)
	data_frames = []
	
	for file in files:
		df = pd.read_csv(file)
		
		winners = df[['tourney_id', 'tourney_name', 'surface', 'tourney_date', 'winner_id', 'winner_name', 'winner_hand', 
					  'winner_ht', 'winner_ioc', 'winner_age', 'winner_rank', 
					  'winner_rank_points', 'loser_id', 'loser_name', 'loser_hand', 'loser_ht', 'loser_ioc', 
					  'loser_age', 'loser_rank', 'loser_rank_points', 'tourney_level', 'round']].copy()
		winners.loc[:, 'result'] = 1
		
		losers = df[['tourney_id', 'tourney_name', 'surface', 'tourney_date', 'loser_id', 'loser_name', 'loser_hand', 
					 'loser_ht', 'loser_ioc', 'loser_age', 'loser_rank', 
					 'loser_rank_points', 'winner_id', 'winner_name', 'winner_hand', 'winner_ht', 'winner_ioc', 
					 'winner_age', 'winner_rank', 'winner_rank_points', 'tourney_level', 'round']].copy()
		losers.loc[:, 'result'] = 0
		
		winners.columns = losers.columns = ['tourney_id', 'tourney_name', 'surface', 'tourney_date', 'player_id', 
											'player_name', 'player_hand', 'player_ht', 'player_ioc', 'player_age', 
											'player_rank', 'player_rank_points', 
											'opponent_id', 'opponent_name', 'opponent_hand', 'opponent_ht', 
											'opponent_ioc', 'opponent_age', 'opponent_rank', 
											'opponent_rank_points', 'tourney_level', 'round', 'result']
		
		data_frames.append(winners)
		data_frames.append(losers)
	
	data = pd.concat(data_frames, ignore_index=True)
	os.makedirs('data/processed', exist_ok=True)
	data.to_csv('data/processed/final.csv', index=False)

load_and_process_data('data/raw/JeffSackmann@tennis_atp/atp_matches_2*.csv')
