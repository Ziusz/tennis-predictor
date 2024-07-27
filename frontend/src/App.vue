<template>
	<div id="app">
		<div class="container">
			<h1>Tennis Predictor</h1>
			<PlayerForm />
		</div>
	</div>
</template>

<script>
import PlayerForm from './components/PlayerForm.vue';

export default {
	name: 'App',
	components: {
		PlayerForm
	}
};
</script>

<style>
html, body {
	height: 100%;
	margin: 0;
	font-family: 'Helvetica', sans-serif;
	background-color: #121212;
	color: #ffffff;
}

body {
	display: block;
	margin: 0 auto;
}

#app {
	min-width: 900px;
	max-width: 100%;
	padding: 20px;
	box-sizing: border-box;
}

.container {
	width: 1200px;
	max-width: 1200px;
	background-color: #1e1e1e;
	border-radius: 8px;
	padding: 20px;
	margin: 0 auto;
}

h1 {
	text-align: center;
}

label {
	display: block;
	margin-bottom: 8px;
	color: #ffffff;
}

select, input {
	width: 100%;
	padding: 8px;
	margin-bottom: 15px;
	border-radius: 4px;
	border: none;
	background-color: #333333;
	color: #ffffff;
	outline: none;
	box-sizing: border-box
}

button {
	width: 100%;
	padding: 10px;
	background-color: #6200ea;
	border: none;
	border-radius: 4px;
	color: white;
	cursor: pointer;
	font-size: 16px;
	transition: background-color 0.3s;
}

button:hover {
	background-color: #3700b3;
}
</style>
