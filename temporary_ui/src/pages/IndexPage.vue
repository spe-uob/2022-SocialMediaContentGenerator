<template>
  <q-page class="flex flex-center">
    <div class="row" style="width: 80%">
      <div class="col-4">
        <q-card>
          <q-card-section>
            <div class="text-h6">Control Area</div>
          </q-card-section>
          <q-card-section>
            <div class="text-h6">Prompt:</div>
            <q-input
              v-model="prompts"
              filled
              autogrow
            />
          </q-card-section>
          <q-card-section>
            <q-badge color="secondary">
              Steps: {{ step }} (0 to 150)
            </q-badge>
            <q-slider v-model="step" :min="0" :max="150"/>
            <q-badge color="warning"> CFG: {{ cfg }} (1 to 30)</q-badge>
            <q-slider v-model="cfg" :min="1.0" :max="30.0" :step="0.5"/>
          </q-card-section>
          <q-card-section>
            <q-badge color="positive"> width: {{ width }}</q-badge>
            <q-slider v-model="width" :min="64" :max="2048" :step="64"/>
            <q-badge color="positive"> height: {{ height }}</q-badge>
            <q-slider v-model="height" :min="64" :max="2048" :step="64"/>
          </q-card-section>
          <q-card-section>
            <q-btn color="primary" label="generate" :disable="generating" @click="generate"/>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-8">
        <q-card>
          <q-card-section>
            <div class="text-h6">Image</div>
            <q-img :src="image" style="max-width: 40vw"></q-img>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import {defineComponent, onBeforeUnmount} from 'vue'

export default defineComponent({
  name: 'IndexPage',
  data() {
    return {
      prompts: '',
      generating: false,
      image: '',
      step: 20,
      cfg: 7.5,
      width: 512,
      height: 512,
    }
  },
  methods: {
    async generate() {
      this.generating = true
      this.$q.loading.show()
      let request = await fetch('http://localhost:8888/api/v1/sample', {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          prompt: this.prompts,
          sample: "dpm",
          batch_size: 1,
          step: this.step,
          cfg: this.cfg,
          width: this.width,
          height: this.height,
        }),
      })
      let response = await request.json()
      this.image = response.image
      this.$q.loading.hide()
      console.log("generate complete")
      console.log(response)
      this.generating = false
    }
  },
  beforeUnmount() {
    this.$q.loading.hide()
  },
})
</script>
