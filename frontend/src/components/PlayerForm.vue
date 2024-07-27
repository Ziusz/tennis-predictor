<template>
	<div>
		<div class="player-select-container">
			<PlayerSelect class="player-select" ref="player1" />
			<PlayerSelect class="player-select" ref="player2" />
		</div>
		<div class="match-settings-container">
			<h3>Match Settings</h3>
			<MatchSettings
				v-model:surface="surface"
				v-model:tourneyLevel="tourneyLevel"
				v-model:round="round"
			/>
			<button @click="predict">PREDICT</button>
		</div>
		<div class="predictions-container">
			<PredictionResults v-if="predictions" :predictions="predictions" />
		</div>
	</div>
</template>



<script>
import PlayerSelect from './PlayerSelect.vue';
import PredictionResults from './PredictionResults.vue';
import MatchSettings from './MatchSettings.vue';
import axios from '@/axios';
import { ref } from 'vue';

export default {
	components: { PlayerSelect, PredictionResults, MatchSettings },
	setup() {
		const player1 = ref(null);
		const player2 = ref(null);
		const surface = ref('Hard');
		const tourneyLevel = ref('A');
		const round = ref('F');
		const predictions = ref(null);

		const predict = async () => {
			const player1Data = player1.value?.selectedPlayerData;
			const player2Data = player2.value?.selectedPlayerData;
			const data = {
				player1: {
					hand: player1Data?.hand || 'R',
					height: player1Data?.height || '180',
					age: player1Data?.age || 27,
					rank: player1Data?.rank || '1000',
					rank_points: player1Data?.points || '0'
				},
				player2: {
					hand: player2Data?.hand || 'R',
					height: player2Data?.height || '180',
					age: player2Data?.age || 27,
					rank: player2Data?.rank || '1000',
					rank_points: player2Data?.points || '0'
				},
				surface: surface.value,
				tourney_level: tourneyLevel.value,
				round: round.value
			};

			try {
				const response = await axios.post('/predict', data);
				predictions.value = response.data;
			} catch (error) {
				console.error('Error making prediction:', error);
			}
		};

		return {
			player1,
			player2,
			predictions,
			surface,
			tourneyLevel,
			round,
			predict
		};
	}
};
</script>

<style scoped>
	.player-select-container {
		display: flex;
		justify-content: space-between;
		gap: 20px;
	}

	.player-select {
		flex: 1;
	}

	.match-settings-container {
		display: flex;
		flex-direction: column;
		width: 600px;
		margin: 0 auto;
	}

	.match-settings-container h3 {
		text-align: center;
	}

	.predictions-container {
		margin-top: 40px;
	}
</style>