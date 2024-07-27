<template>
	<div>
		<Select
			v-model="selectedPlayer"
			:options="filteredPlayers"
			:filterable="true"
			:reduce="player => player.player_id"
			label="label"
			placeholder="Search for a player (minimum 3 characters)..."
			@search="handleSearch"
		/>
		<div v-if="selectedPlayerData">
			<h2>{{ selectedPlayerData.name_first }} {{ selectedPlayerData.name_last }} ({{ selectedPlayerData.ioc }})</h2>
			<label>Hand:</label>
			<select v-model="selectedPlayerData.hand">
				<option value="R">Right</option>
				<option value="L">Left</option>
				<option value="U">Unknown</option>
			</select>
			<label>Height:</label>
			<input v-model="selectedPlayerData.height" type="number" />
			<label>Age:</label>
			<input v-model="selectedPlayerData.age" type="number" step="0.1" />
			<label>Points:</label>
			<input v-model="selectedPlayerData.points" type="number" :min="0" />
			<label>Rank:</label>
			<input v-model="selectedPlayerData.rank" type="number" :min="1" />
		</div>
	</div>
</template>

<script>
import axios from '@/axios';
import { ref, watch } from 'vue';
import Select from 'vue3-select';
import 'vue3-select/dist/vue3-select.css';

export default {
	components: { Select },
	setup() {
		const players = ref([]);
		const filteredPlayers = ref([]);
		const selectedPlayer = ref(null);
		const selectedPlayerData = ref(null);

		const fetchPlayers = async () => {
			try {
				const response = await axios.get('/players');
				players.value = response.data.map(player => ({
					...player,
					label: `${player.name_first} ${player.name_last} (${player.ioc})`
				}));
			} catch (error) {
				console.error('Error:', error);
			}
		};

		const handleSearch = (search) => {
			if (search.length < 3) {
				filteredPlayers.value = [];
				return;
			}
			filteredPlayers.value = players.value.filter(player =>
				player.label.toLowerCase().includes(search.toLowerCase())
			);
		};

		const fetchPlayerData = (playerId) => {
			if (!playerId) return;
			const playerData = players.value.find(player => player.player_id === playerId);
			if (playerData) {
				playerData.age = calculateAge(playerData.dob);
				selectedPlayerData.value = playerData;
				selectedPlayerData.value.height = selectedPlayerData.value.height ?? 180;
				selectedPlayerData.value.points = selectedPlayerData.value.points ?? 0;
				selectedPlayerData.value.rank = selectedPlayerData.value.rank ?? 1000;        
			}
		};

		const calculateAge = (dob) => {
			if (!dob) return null;
			const year = Math.floor(dob / 10000);
			const month = Math.floor((dob % 10000) / 100) - 1;
			const day = dob % 100;
			const birthDate = new Date(year, month, day);
			const ageDifMs = Date.now() - birthDate.getTime();
			const ageDate = new Date(ageDifMs);
			const age = Math.abs(ageDate.getUTCFullYear() - 1970 + ageDate.getUTCMonth() / 12);
			return parseFloat(age.toFixed(1));
		};

		watch(selectedPlayer, (newPlayer) => fetchPlayerData(newPlayer));

		fetchPlayers();

		return {
			filteredPlayers,
			selectedPlayer,
			selectedPlayerData,
			handleSearch
		};
	}
};
</script>

<style scoped>
>>> {
	--vs-controls-color: #6200ea;
	--vs-border-color: #6200ea;

	--vs-dropdown-bg: #282c34;
	--vs-dropdown-color: #cc99cd;
	--vs-dropdown-option-color: #cc99cd;

	--vs-selected-bg: #664cc3;
	--vs-selected-color: #eeeeee;

	--vs-search-input-color: #eeeeee;
	--vs-search-input-placeholder-color: #aaa;

	--vs-dropdown-option--active-bg: #664cc3;
	--vs-dropdown-option--active-color: #eeeeee;
}
</style>
