<template>
  <q-page class="flex flex-center">
    <div class="column" style="width: 100vw">
      <div class="col flex flex-center">
        <div class="row" style="width: 80%">
          <div class="col-12 ">
            <q-card>
              <q-card-section>
                <q-select filled bottom-slots v-model="model" :options="models" label="Models" counter maxlength="12" :loading="loading_model" @update:model-value="load_model">
                  <template v-slot:hint>
                    model loader
                  </template>
                  <template v-slot:after>
                    <q-btn round dense flat icon="refresh" @click="syncModelList"/>
                  </template>
                </q-select>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>
      <div class="col flex flex-center">
        <div class="row q-pa-xl q-mr-xl" style="width: 80%">
          <div class="col-4 q-pa-sm">
            <q-card>

              <q-card-section>
                <div class="text-h7">Control Area</div>
              </q-card-section>

              <q-card-section>
                <div class="text-h9">Prompt:</div>
                <q-input
                  v-model="prompt"
                  filled
                  autogrow
                />
              </q-card-section>

              <q-card-section>
                <div class="text-h8">Seed:</div>
                <q-input
                  v-model="seed"
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
                <q-btn color="primary" label="generate" :disable="generating" @click="generate,showImageLoading"/>
              </q-card-section>
            </q-card>

          </div>
          <div class="col-8 q-pa-sm">
            <q-card>
              <q-card-section>
                <div class="text-h3">Image Show</div>
              </q-card-section>

              <q-card-section>
                <transition
                  appear
                  enter-active-class="animated fadeIn"
                  leave-active-class="animated fadeOut"
                >

                    <q-img v-show="showSimulatedReturnData" :src="image" style="max-width: 40vw"></q-img>

                </transition>
              </q-card-section>

              <q-inner-loading
                :showing="visible"
                label="Please wait..."
                label-class="text-teal"
                label-style="font-size: 1.1em"
              />

            </q-card>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
let PromptID = 0

import {defineComponent,ref} from 'vue'
export default defineComponent({
  name: 'NewUI',
  setup(){
    const visible = ref(false)
    const showSimulatedReturnData = ref(false)
    return {
      visible,
      showSimulatedReturnData,

      showImageLoading () {
        visible.value = true
        showSimulatedReturnData.value = false

        setTimeout(() => {
          visible.value = false
          showSimulatedReturnData.value = true
        }, 3000)
      }
    }
  },
  data() {
    return {
      model: null,
      models: [],
      loading_model: false,
      prompt:'',
      seed:'',
      generating: false,
      image: '',
      step: 20,
      cfg: 7.5,
      width: 512,
      height: 512,
    }
  },
  methods: {
    async sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    },
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
          seed: this.seed,
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
    },
    async syncModelList() {
      this.loading_model = true
      await this.sleep(300);
      let request = await fetch('http://localhost:8888/api/v1/model_list', {method: 'GET', mode: 'cors'});
      let response = await request.json();
      console.log(response)
      this.models = response['mode_list'];
      this.loading_model = false
    },
    async load_model() {
      this.loading_model = true
      const dismiss = this.$q.notify({
        spinner: true,
        message: `loading model ${this.model}...`,
        position: "top",
        timeout: 0,
      })
      let request = await fetch(`http://localhost:8888/api/v1/load_model?ModelName=${this.model}`, {method: 'GET', mode: 'cors'});
      let response = await request.json();
      dismiss()
      if (response['status'] === 0)
        this.$q.notify({
          spinner: true,
          message: `loading model ${this.model} complete!`,
          timeout: 3000,
          color: "positive",
          position: "top"
        })
      else
        this.$q.notify({
          spinner: true,
          message: `loading model ${this.model} failed!\n ${response['error']}`,
          timeout: 3000,
          color: "negative",
          position: "top"
        })
      this.loading_model = false
    },
    async getCurrentModel() {
      let info = await this.getInfo();
      this.model = info['current_model']
    },
    async getInfo() {
      let request = await fetch('http://localhost:8888/api/v1/get_info', {method: 'GET', mode: 'cors'});
      return request.json();
    },

    addNewPrompt(){
      this.Prompts.push({
        id: PromptID++,
        name: this.newPrompt
      })
      this.newPrompt = ''
    },

    removePrompt(prompt) {
      this.Prompts = this.Prompts.filter((t) => t !== prompt)
    },

    onSubmit (evt) {
      console.log('@submit - do something here', evt)
      evt.target.submit()
    },

  },
  async beforeMount() {
    await this.syncModelList()
    await this.getCurrentModel();
  },
  beforeUnmount() {
    this.$q.loading.hide()
  },
})
</script>

<style scoped>

</style>
