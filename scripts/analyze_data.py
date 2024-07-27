import pandas as pd
import glob
import seaborn as sns
import matplotlib.pyplot as plt

def load_data(path_pattern):
	files = glob.glob(path_pattern)
	data_frames = []
	
	for file in files:
		df = pd.read_csv(file)
		data_frames.append(df)
	
	data = pd.concat(data_frames, ignore_index=True)
	return data

def eda(data):
	print("Basic information about the data:")
	print(data.info())
	
	print("\nMissing data in each column:")
	missing_data_count = data.isnull().sum()
	missing_data_percentage = (missing_data_count / len(data)) * 100
	missing_data = pd.DataFrame({
		'Missing Count': missing_data_count,
		'Missing Percentage (%)': missing_data_percentage
	})
	print(missing_data)
	missing_data.to_csv('data/processed/statistics/missing_data.csv', index=True)
	
	print("\nDescriptive statistics:")
	descriptive_stats = data.describe(include='all')
	print(descriptive_stats)
	descriptive_stats.to_csv('data/processed/statistics/descriptive.csv', index=True)
	
	print("\nCorrelation matrix:")
	numerical_data = data.select_dtypes(include=['number'])
	correlation_matrix = numerical_data.corr()
	print(correlation_matrix)
	correlation_matrix.to_csv('data/processed/statistics/correlation_matrix.csv', index=True)

	plt.figure(figsize=(20, 12.5))
	sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm')
	plt.title('Correlation matrix of features')
	plt.savefig('data/processed/statistics/correlation_heatmap.png')
	plt.show()

	numerical_data.hist(figsize=(20, 12.5), bins=20, edgecolor='black')
	plt.title('Features distribution')
	plt.tight_layout()
	plt.savefig('data/processed/statistics/features_distribution.png')
	plt.show()

	filtered_data = data[data['w_ace'] != 113] # Remove a anomalous match of Isner vs Mahut on Wimbledon 2010
	filtered_numerical_data = filtered_data.select_dtypes(include=['number'])
	filtered_numerical_data.hist(figsize=(20, 12.5), bins=20, edgecolor='black')
	plt.title('Features distribution without Isner - Mahut match on Wimbledon 2010')
	plt.tight_layout()
	plt.savefig('data/processed/statistics/features_distribution_filtered.png')
	plt.show()

data = load_data('data/raw/JeffSackmann@tennis_atp/atp_matches_2*.csv')
eda(data)
