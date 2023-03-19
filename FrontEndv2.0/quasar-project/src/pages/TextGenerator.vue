<template>
  <div>
    <label for="prompt-input">Enter a prompt:</label>
    <input id="prompt-input" type="text" v-model="prompt">
    <button @click="generateText">Generate Text</button>
    <p>{{ generatedText }}</p>
    <!--<p v-if="generatedText">{{ generatedText }}</p>-->
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: "TextGenerator",
  data() {
    return {
      prompt: '',
      generatedText: ''
    };
  },
  methods: {
    async generateText() {
      const prompt = this.prompt;
      const apiKey = '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';
      const url = 'https://api.openai.com/v1/engines/davinci-codex/completions';

      try {
        const response = await axios.post(url, {
          prompt: prompt,
          max_tokens: 50,
          n: 1,
          stop: '\n',
          temperature: 0.5
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
