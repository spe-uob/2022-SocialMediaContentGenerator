<template>
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
import axios from "axios";

export default {
  name: "TextG",
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
         // model: 'text-davinci-003' ,
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

</style>
