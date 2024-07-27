<template>
	<div>
		<h3>Predictions</h3>
		<div v-for="(value, model) in predictions" :key="model">
			<div class="model">
				<div class="model-name">
					<h4>{{ model }}</h4>
					<button @click="evaluateModel(model)">Evaluate</button>
				</div>
				<div class="model-result">
					<p>{{ (value * 100).toFixed(2) }}%</p>
					<div class="progress-bar">
						<div class="progress" :style="{ width: (value * 100) + '%' }"></div>
					</div>
					<p>{{ (100 - (value * 100)).toFixed(2) }}%</p>
				</div>
			</div>
		</div>

		<div v-if="showModal" class="modal">
			<div class="modal-content">
				<span class="close" @click="closeModal">&times;</span>
				<h2>Evaluation Results for {{ selectedModel }}</h2>
				<div v-if="evaluationResults">
					<p><strong>Accuracy:</strong> {{ evaluationResults.accuracy.toFixed(6) }}</p>
					<p><strong>F1 Score:</strong> {{ evaluationResults.f1_score.toFixed(6) }}</p>
					<p><strong>Precision:</strong> {{ evaluationResults.precision.toFixed(6) }}</p>
					<p><strong>Recall:</strong> {{ evaluationResults.recall.toFixed(6) }}</p>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from '@/axios';
import { ref } from 'vue';
export default {
	props: {
		predictions: {
			type: Object,
			required: true
		}
	},
	setup() {
	const showModal = ref(false);
	const selectedModel = ref('');
	const evaluationResults = ref('');

	const evaluateModel = async (model) => {
		selectedModel.value = model;
		try {
		const response = await axios.get(`/evaluate/${model}`);
		evaluationResults.value = response.data;
		showModal.value = true;
		} catch (error) {
		console.error('Error evaluating model:', error);
		}
	};

	const closeModal = () => {
		showModal.value = false;
		evaluationResults.value = '';
	};

	return {
		evaluateModel,
		showModal,
		selectedModel,
		evaluationResults,
		closeModal
	};
	}
};
</script>

<style scoped>
.progress-bar {
	width: 100%;
	background-color: #333333;
	border-radius: 5px;
	margin: 0 10px;
}

.progress {
	height: 15px;
	background-color: #6200ea;
	border-radius: 20px;
}

.model {
	display: flex;
	align-items: center;
}

.model > * {
	flex: 1;
}

.model-name {
	display: flex;
	column-gap: 30px;
	align-items: center;
}

.model-name button {
	width: fit-content;
	padding: 7px 13px;
	height: 30px;
}

.model-result {
	display: flex;
	align-items: center;
}

h3 {
	text-align: center;
}

.modal {
	display: flex;
	position: fixed;
	z-index: 1;
	left: 0;
	top: 0;
	width: 100%;
	height: 100%;
	overflow: auto;
	background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
	margin: auto;
	padding: 20px;
	border: 2px solid #3700b3;
	width: fit-content;
	background-color: #080707;
	border-radius: 10px;
}

.close {
	color: #bbb;
	float: right;
	font-size: 28px;
	font-weight: bold;
}

.close:hover,
.close:focus {
	color: #fff;
	text-decoration: none;
	cursor: pointer;
}
</style>
