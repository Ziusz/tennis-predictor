<template>
	<div>
		<label for="surface-select">Surface:</label>
		<select id="surface-select" v-model="selectedSurface" @change="updateSurface">
			<option v-for="option in surfaceOptions" :key="option.value" :value="option.value">
				{{ option.text }}
			</option>
		</select>

		<label for="tourney-level-select">Tourney Level:</label>
		<select id="tourney-level-select" v-model="selectedTourneyLevel" @change="updateTourneyLevel">
			<option v-for="option in tourneyLevelOptions" :key="option.value" :value="option.value">
				{{ option.text }}
			</option>
		</select>

		<label for="round-select">Round:</label>
		<select id="round-select" v-model="selectedRound" @change="updateRound">
			<option v-for="option in roundOptions" :key="option.value" :value="option.value">
				{{ option.text }}
			</option>
		</select>
	</div>
</template>

<script>
import { ref } from 'vue';

export default {
	props: {
		surface: {
			type: String,
			required: true,
		},
		tourneyLevel: {
			type: String,
			required: true,
		},
		round: {
			type: String,
			required: true,
		}
	},
	setup(props, { emit }) {
		const surfaceOptions = [
			{ value: 'Hard', text: 'Hard' },
			{ value: 'Clay', text: 'Clay' },
			{ value: 'Grass', text: 'Grass' },
			{ value: 'Carpet', text: 'Carpet' },
		];

		const tourneyLevelOptions = [
			{ value: 'G', text: 'Grand Slam (G)' },
			{ value: 'M', text: 'Masters 1000 (M)' },
			{ value: 'A', text: 'Normal-level ATP (A)' },
			{ value: 'F', text: 'Tour Final (F)' },
			{ value: 'D', text: 'Davis Cup (D)' },
		];

		const roundOptions = [
			{ value: 'F', text: 'Final (F)' },
			{ value: 'SF', text: 'Semi-final (SF)' },
			{ value: 'QF', text: 'Quarter-final (QF)' },
			{ value: 'R16', text: 'Round of 16 (R16)' },
			{ value: 'R32', text: 'Round of 32 (R32)' },
			{ value: 'R64', text: 'Round of 64 (R64)' },
			{ value: 'R128', text: 'Round of 128 (R128)' },
		];

		const selectedSurface = ref(props.surface);
		const selectedTourneyLevel = ref(props.tourneyLevel);
		const selectedRound = ref(props.round);

		const updateSurface = () => {
			emit('update:surface', selectedSurface.value);
		};

		const updateTourneyLevel = () => {
			emit('update:tourneyLevel', selectedTourneyLevel.value);
		};

		const updateRound = () => {
			emit('update:round', selectedRound.value);
		};

		return {
			surfaceOptions,
			tourneyLevelOptions,
			roundOptions,
			selectedSurface,
			selectedTourneyLevel,
			selectedRound,
			updateSurface,
			updateTourneyLevel,
			updateRound,
		};
	}
};
</script>
