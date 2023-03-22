<template>
  <q-page class="flex flex-left">
    <div class="col-sm-4 q-pa-sm">
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
          <div class="text-h9">Negative Prompt:</div>
          <q-input
            v-model="negative_prompts"
            square outlined
            filled
            autogrow
          />
        </q-card-section>
        <q-card-section>
          <q-select :options="sampler_options" v-model="sampler" hint="sampler">
          </q-select>
        </q-card-section>

        <q-card-section>
          <q-badge color="primary"> Steps: {{ step }} (0 to 150)</q-badge>
          <q-slider color="primary" v-model="step" :min="0" :max="150"/>
          <q-badge color="secondary"> CFG: {{ cfg }} (1 to 30)</q-badge>
          <q-slider color="secondary" v-model="cfg" :min="1.0" :max="30.0" :step="0.5"/>
          <q-badge color="positive"> Number of iterations: {{ n_iter }} (1 to 32)</q-badge>
          <q-slider color="positive" v-model="n_iter" :min="1" :max="32" :step="1"/>
          <q-badge color="positive"> Batch size: {{ batch_size }} (1 to 8)</q-badge>
          <q-slider color="positive" v-model="batch_size" :min="1" :max="8" :step="1"/>
          <div class="text-h6">{{ batch_size * n_iter }} images will be generated</div>
        </q-card-section>

        <q-card-section>
          <q-badge color="accent"> width: {{ width }}</q-badge>
          <q-slider color="accent" v-model="width" :min="64" :max="2048" :step="64"/>
          <q-badge color="accent"> height: {{ height }}</q-badge>
          <q-slider color="accent" v-model="height" :min="64" :max="2048" :step="64"/>
        </q-card-section>


      </q-card>

    </div>

  </q-page>
  <div>
    <label for="prompt-input">Enter a prompt:</label>
    <input id="prompt-input" type="text" v-model="prompt">
    <label for="temperature-toggle">Temperature:</label>
    <input id="temperature-toggle" type="range" min="0" max="1" step="0.1" v-model="temperature">
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
      const url = 'https://api.openai.com/v1/engines/davinci/completions';

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

</style>
