<template>
  <!--<div class="container">-->
    <div class="left_container">
      <q-card>
        <q-bar :class="$q.dark.isActive ? 'bg-blue-grey-14' : 'bg-blue-grey-2'">
          <q-card-section>

            <div class="text-white text-h7">Control Area</div>

          </q-card-section>
        </q-bar>
        <q-card-section>
          <div class="text-h9">Prompt:</div>
          <q-input
            v-model="prompt"
            square outlined
            filled
            autogrow
          />
        </q-card-section>



        <q-card-section>
          <label for="temperature-toggle">Temperature: {{temperature}}</label>
          <input id="temperature-toggle" type="range" min="0" max="1" step="0.1" v-model="temperature">
          <!--<q-badge color="primary"> Temperature: {{ temperature }} (0 to 1)</q-badge>
          <input id="temperature-toggle" type="range" min="0" max="1" step="0.1" v-model="temperature">
          <q-slider color="primary" type="range" v-model="temperature" min="0" max="1" step="0.1"/>-->
        </q-card-section>




      </q-card>

    </div>
  <div class="right_container">
  <div class="chat_container">
    <form @submit.prevent="generateText">
      <textarea
        rows="1"
        cols="1"
        placeholder="generate content..."
        v-model="prompt">
    ></textarea>
      <button @click="generateText"><img src="~assets/send.svg"></button>
      <!--<p>{{ generatedText }}</p>-->
    </form>
    <p>{{ generatedText }}</p>
  </div>
  </div>
  <!--</div>-->
 <div>
    <label for="prompt-input">Enter a prompt:</label>
    <input id="prompt-input" type="text" v-model="prompt">
    <label for="temperature-toggle">Temperature:</label>
    <input id="temperature-toggle" type="range" min="0" max="1" step="0.1" v-model="temperature">
    <button @click="generateText">Generate Text</button>
    <p>{{ generatedText }}</p>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: "TextGenerator",
  data() {
    return {
      prompt: '',
      generatedText: '',
      temperature: 0.5

    };
  },
  methods: {
    async generateText() {
      const prompt = this.prompt;
      const apiKey = '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';
      //GPT-2 'https://api.openai.com/v1/engines/davinci-codex/completions'
      //GPT-3 'https://api.openai.com/v1/engines/davinci/completions'
      const url = 'https://api.openai.com/v1/engines/davinci-codex/completions';

      try {
        const response = await axios.post(url, {
          model: 'text-davinci-003' ,
          prompt: prompt,
          max_tokens: 50,
          n: 1,
          stop: '\n',
          temperature: this.temperature
        }, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`
          }
        });

        this.generatedText = response.data.choices[0].text;
      } catch (error) {
        console.log(error);
      }
    }
  }
}
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@100;300;400;500;700;800;900&display=swap");

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Poppins", sans-serif;
}

body {
  background: #343541;
}

#app {
  width: 100vw;
  height: 100vh;
  background: #343541;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
}

.container {
  position: fixed;
  left: 350px;
  padding: 0;
  margin: 0;
}

.left_container{
  display: inline-block;
  float: left;
  width: 30%;
  height:30%;
  padding-left: 10px;
  padding-top: 10px;
  padding-right: 10px;
}

.right_container{
  display: inline-block;
  float: right;
  width: 70%;
  height: 70%;
  padding-top: 10px;
  padding-right: 10px;
}

.chat_container {
  flex: 1;
  width: 100%;
  height: 100%;
  //width: 100%;
  //height: 100%;
  overflow-y: scroll;

  display: flex;
  flex-direction: column;
  gap: 10px;

  -ms-overflow-style: none;
  scrollbar-width: none;

  padding-bottom: 20px;
  scroll-behavior: smooth;
}

/* hides scrollbar */
#chat_container::-webkit-scrollbar {
  display: none;
}
main {
  width: 100%;
  height: calc(100% - 80px);
}
.wrapper {
  width: 100%;
  padding: 15px;
}

.ai {
  background: #40414f;
}

.chat {
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;

  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 10px;
}

.profile {
  width: 36px;
  height: 36px;
  border-radius: 5px;

  background: #5436da;

  display: flex;
  justify-content: center;
  align-items: center;
}

.ai .profile {
  background: #10a37f;
}

.profile img {
  width: 60%;
  height: 60%;
  object-fit: contain;
}

.message {
  flex: 1;
  color: #dcdcdc;
  font-size: 20px;
  max-width: 100%;
  overflow-x: scroll;
  white-space: pre-wrap;
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.message::-webkit-scrollbar {
  display: none;
}
form {
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 10px;
  background: #40414f;
  display: flex;
  flex-direction: row;
  gap: 10px;
}
@media (max-width: 1280px) {
  form {
    max-width: calc(100% - 40px);
  }
}
textarea {
  width: 100%;

  color: #fff;
  font-size: 18px;

  padding: 10px;
  background: transparent;
  border-radius: 5px;
  border: none;
  outline: none;
}

button {
  outline: 0;
  border: 0;
  cursor: pointer;
  background: transparent;
}

form img {
  width: 30px;
  height: 30px;
}

</style>
