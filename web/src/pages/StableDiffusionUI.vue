<template>
  <q-page class="flex flex-center">
    <div class="column" style="width: 100vw; margin-top: 20px; margin-bottom: 40px">
      <div class="col flex flex-center">
        <div class="row q-px-xl q-pb-md" style="width: 85%">
          <q-card style="width: 100%">
            <q-card-section>
              <div class="row">
                <div class="col-6 q-pr-sm">
                  <q-select :loading="loading_model" v-model="model" :options="models" label="Model" label-color="red" class="hint-grey" filled bottom-slots
                            :disable="task_rows.length > 0 || loading_vae" @update:model-value="load_model">
                    <template v-slot:hint>
                      model loader
                    </template>
                    <template v-slot:after>
                      <q-btn round dense flat icon="refresh" @click="syncModelList"/>
                    </template>
                  </q-select>
                </div>
                <div class="col-6 q-pl-sm">
                  <q-select :loading="loading_vae" v-model="vae" :options="vae_list" label="VAE" label-color="blue" class="hint-grey" filled bottom-slots
                            :disable="task_rows.length > 0 || model === null || model === undefined || loading_model" @update:model-value="load_model">
                    <template v-slot:hint>
                      vae loader
                    </template>
                    <template v-slot:after>
                      <q-btn round dense flat icon="refresh" @click="syncVaeList"/>
                    </template>
                  </q-select>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
        <div class="row q-px-xl q-pb-md" style="width: 85%">

          <q-card style="width: 100%">
            <q-inner-loading :showing="loading_lora" label="Loading..." label-class="text-teal" label-style="font-size: 1.1em"/>
            <q-card-section>
              <div class="text-h6">Lora network:</div>
              <q-chip class="q-py-lg" color="white" v-for="(model, index) in lora_models" :key="index">
                <q-btn icon="remove" class="q-pa-sm q-mr-sm" @click="remove_lora(index)">
                  <q-tooltip>
                    remove this lora model
                  </q-tooltip>
                </q-btn>
                {{ model.name }} :
                <q-circular-progress show-value font-size="12px" :value="model.weight * 100" hint="weight" size="40px" :thickness="0.22" color="teal" track-color="grey-3" class="q-ml-md">
                  {{ model.weight }}
                </q-circular-progress>
                <q-menu>
                  <div class="row q-px-md q-py-sm" style="width: 15vw">
                    Weight:
                    <q-slider v-model="model.weight" :min="0.0" :max="1.0" :step="0.05" markers></q-slider>
                  </div>
                </q-menu>
                <q-badge color="red" rounded floating v-if="!lora_diff && !current_lora.find((lora) => lora['name'] === model.name)">
                  <q-tooltip>unloaded</q-tooltip>
                </q-badge>
                <q-badge color="green" rounded floating v-if="!lora_diff && current_lora.find((lora) => lora['name'] ===  model.name)">
                  <q-tooltip>loaded</q-tooltip>
                </q-badge>
              </q-chip>
              <q-btn icon="add" class="q-px-sm q-ml-sm">
                <q-menu>
                  <q-list style="min-width: 100px">
                    <q-item clickable v-close-popup v-for="(model, index) in lora_model_list" :key="index" :disable="lora_models.map(x=>x.name).includes(model)">
                      <q-item-section @click="lora_models.map(x=>x.name).includes(model) ? ()=>{} :lora_models.push({name: model, weight: 1.0})">{{ model }}</q-item-section>
                    </q-item>
                  </q-list>
                </q-menu>
              </q-btn>
            </q-card-section>
            <q-card-section>
              <q-btn label="load model" color="primary" @click="load_lora_model()" :disable="loading_lora"/>
            </q-card-section>
          </q-card>
        </div>
        <div class="row q-px-xl q-pb-sm" style="width: 85%" v-if="device_total>0">
          <q-card style="width: 100%">
            <q-card-actions>
              <div class="text-h5">VRAM Usage:</div>
            </q-card-actions>
            <q-card-section>
              <div class="text-h6">usage / cache:</div>
              <q-linear-progress size="25px" :value="allocated / cached" stripe color="positive">
                <div class="absolute-full flex flex-center">
                  <q-badge color="white" text-color="accent" :label="allocated+' GB/'+cached+' GB'"/>
                </div>
              </q-linear-progress>
              <div class="text-h6">cache / device memory:</div>
              <q-linear-progress size="25px" :value="cached / device_total" stripe color="amber">
                <div class="absolute-full flex flex-center">
                  <q-badge color="white" text-color="accent" :label="cached+' GB/'+device_total+' GB'"/>
                </div>
              </q-linear-progress>
            </q-card-section>
          </q-card>
        </div>
        <div class="row q-px-xl q-pb-sm" style="width: 85%">
          <div class="col-4 q-pr-sm">
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
          <div class="col-8 q-pl-sm">
            <q-card>
              <q-bar :class="$q.dark.isActive ? 'bg-blue-grey-14' : 'bg-blue-grey-2'">
                <q-card-section>
                  <div class="text-white text-h7">Image Show</div>
                </q-card-section>
              </q-bar>
              <q-card-section>
                <q-img :src="images.length > 0 ? images[currentImageIndex-1].url:''" style="max-height: 60vh; background-color: white" fit="contain">
                  <div class="text-h6" v-if="images.length > 0 ">Seed: {{ images[currentImageIndex - 1].seed }}</div>
                </q-img>
                <router-link v-if="images.length > 0 " :to="{path: '/twitter', query: {image:images[currentImageIndex - 1].path, url: images[currentImageIndex-1].url }}">
                  <q-btn color="blue" class="full-width" style="margin-top: 20px">
                    Send {{ images[currentImageIndex - 1].path }} to twitter page
                  </q-btn>
                </router-link>
                <q-pagination v-model="currentImageIndex" :max="images.length" :min="1" input/>
                <!--                <q-linear-progress :value="task_progress" class="q-mt-md" />-->
                <q-linear-progress size="25px" :value="task_progress" stripe color="positive">
                  <div class="absolute-full flex flex-center">
                    <q-badge color="white" text-color="accent" :label="task_progress"/>
                  </div>
                </q-linear-progress>
                <q-linear-progress v-if="current_task.hasOwnProperty('sub_progress')" size="25px" :value="current_task['sub_progress']" stripe color="positive">
                  <div class="absolute-full flex flex-center">
                    <q-badge color="white" text-color="accent" :label="(current_task['sub_progress'] * 100).toFixed(2) + '%'"/>
                  </div>
                </q-linear-progress>
              </q-card-section>
              <q-card-section class="self-center">
                <q-btn color="positive" class="q-mr-md" label="generate" :disable="generating || loading_model" @click="generate()"/>
                <q-btn color="positive" class="q-ml-md" label="save" @click="saveImage"/>

              </q-card-section>

            </q-card>
          </div>
        </div>
        <div class="row q-px-xl q-pb-sm" style="width: 85%">
          <q-table title="Tasks" :rows="task_rows" style="width: 100%" :columns="task_columns" row-key="uuid"/>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
let PromptID = 0

import {computed, defineComponent, ref} from 'vue'


export default defineComponent({
  name: 'StableDiffusionUI',
  setup() {
    const visible = ref(false)
    const showSimulatedReturnData = ref(false)
    return {
      visible,
      showSimulatedReturnData,

      showImageLoading() {
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
      debug: false,
      model: null,
      models: [],
      vae: null,
      vae_list: [],
      lora_models: [],
      current_lora: [],
      lora_model_list: [],
      lora_diff: computed(() => {
        return this.compare_loaded_lora()
      }),
      loading_model: false,
      loading_vae: false,
      loading_lora: false,
      prompt: '',
      negative_prompts: '',
      seed: '',
      generating: false,
      image: '',
      images: [],
      currentImageIndex: 0,
      image_name: '',
      step: 20,
      cfg: 7.5,
      width: 512,
      height: 512,
      n_iter: 1,
      batch_size: 1,
      base_url: 'http://localhost:8888',
      sampler: 'DDIM',
      sampler_options: ["DDIM", "PLMS", "Euler A", "Euler", "LMS", "Heun", "DPM2", "DPM2 a", "DPM++ 2S a", "DPM++ 2M", "DPM++ SDE", "DPM fast", "DPM adaptive"],
      images_buffer: [],
      sample_task_uuid: null,
      task_images_length: 0,
      task_progress: 0,
      current_task: {},
      current_tasks: [],
      task_columns: [
        {name: 'this', label: 'is your task?', align: 'center', field: 'this', sortable: true},
        {name: 'progress', label: 'progress', align: 'center', field: 'progress', sortable: true},
        {name: 'sub_progress', label: 'sub_progress', align: 'center', field: 'sub_progress', sortable: true},
        {name: 'uuid', label: 'uuid', align: 'left', field: 'uuid', sortable: true},
        {name: 'n_iter', align: 'center', label: 'n_iter', field: 'n_iter', sortable: true},
        {name: 'batch_size', label: 'batch_size', field: 'batch_size', sortable: true},
        {name: 'sampler', label: 'sampler', field: 'sampler'},
        {name: 'width', label: 'width', field: 'width'},
        {name: 'height', label: 'height', field: 'height'},
        {name: 'step', label: 'step', field: 'step', sortable: true},
        {name: 'cfg', label: 'cfg', field: 'cfg', sortable: true},
        {name: 'prompt', label: 'prompt', field: 'prompt', sortable: true},
        {name: 'negative_prompt', label: 'negative_prompt', field: 'negative_prompt', sortable: true},
      ],
      task_rows: [],
      current_progress: 0,
      allocated: 0,
      cached: 0,
      device_total: 0,
    }
  },
  methods: {

    getUrl(path) {
      return this.debug ? "http://localhost:8888" + path : path;
    },
    saveImage() {
      const link = document.createElement('a')
      link.setAttribute('href', this.images[this.currentImageIndex - 1])
      link.setAttribute('download', 'image.jpg')
      link.click()
    },
    async sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    },
    async generate() {
      this.generating = true
      // this.$q.loading.show()
      let request = await fetch(this.getUrl('/api/v1/sample'), {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          prompt: this.prompt,
          "prompts": this.prompt,
          negative_prompt: this.negative_prompts,
          seed: this.seed,
          sample: this.sampler !== null ? this.sampler : "DDIM",
          n_iter: this.n_iter,
          batch_size: this.batch_size,
          step: this.step,
          cfg: this.cfg,
          width: this.width,
          height: this.height,
        }),
      })
      let response = await request.json()
      this.sample_task_uuid = response['uuid'];
      this.task_images_length = response['length'];
      this.images_buffer = [];
      this.checkTaskStatus().then(null);
      // this.$q.loading.hide()

    },
    async checkTaskStatus() {
      while (this.images_buffer.length < this.task_images_length) {
        let request = await fetch(this.getUrl(`/api/v1/get_sample_result?uuid=${this.sample_task_uuid}&length=${this.task_images_length}&loaded=${this.images_buffer.length}`), {
          method: 'GET',
          mode: 'cors'
        });
        let response = await request.json();
        let images = response['images'];
        for (let i = 0; i < images.length; i++) {
          images[i] = {
            url: this.getUrl(`/api/v1/cached_image?path=${encodeURIComponent(images[i][0])}`),
            seed: images[i][2],
            path: images[i][0],
          }
        }
        this.images_buffer = this.images_buffer.concat(images);
        if (this.images_buffer.length > 0) {
          if (this.images_buffer.length < this.images.length)
            this.currentImageIndex = 1;
          if (this.images_buffer.length > this.images.length) {
            this.$q.notify({
              message: `New image generated(${this.images_buffer.length})`,
              color: 'positive',
              position: 'top',
              timeout: 1000
            })
            this.currentImageIndex = this.images_buffer.length;
          }
          this.images = this.images_buffer;
          this.task_progress = (this.images_buffer.length / this.task_images_length * 100).toFixed(2) + "%";
        }
        await this.sleep(1000);
      }
      this.$q.notify({
        message: `All images generated`,
        color: 'positive',
        position: 'top',
        timeout: 1000
      })
      this.generating = false
    },
    async syncTasks() {
      let request = await fetch(this.getUrl(`/api/v1/get_txt2img_task_info`), {
        method: 'GET',
        mode: 'cors'
      });
      let response = await request.json();
      this.current_task = {};
      for (let i = 0; i < response['tasks'].length; i++)
        if (response['tasks'][0]['uuid'] === this.sample_task_uuid)
          this.current_task = response['tasks'][0];
      this.current_tasks = response['tasks'];
      this.task_rows = this.current_tasks.map((task) => {
        return {
          'this': task['uuid'] === this.sample_task_uuid,
          progress: (task['progress'] * 100).toFixed(2) + "%",
          sub_progress: (task['sub_progress'] * 100).toFixed(2) + "%",
          uuid: task['uuid'],
          n_iter: task['n_iter'],
          batch_size: task['batch_size'],
          sampler: task['sampler'],
          width: task['width'],
          height: task['height'],
          step: task['step'],
          cfg: task['cfg'],
          prompt: task['prompt'].length > 50 ? task['prompt'].substring(0, 50) + '...' : task['prompt'],
          negative_prompt: task['negative_prompt'].length > 50 ? task['negative_prompt'].substring(0, 50) + '...' : task['negative_prompt'],
        }
      })
    },
    async syncGPUInfo() {
      let request = await fetch(this.getUrl('/api/v1/vram'), {method: 'GET', mode: 'cors'});
      let response = await request.json();
      this.allocated = response['allocated'].toFixed(3);
      this.cached = response['cached'].toFixed(3);
      this.device_total = response['device_total'].toFixed(3);
    },
    async syncModelList() {
      this.loading_model = true
      await this.sleep(300);
      let request = await fetch(this.getUrl('/api/v1/model_list'), {method: 'GET', mode: 'cors'});
      let response = await request.json();
      console.log(response)
      this.models = response['mode_list'];
      await this.getCurrentModel()
      this.loading_model = false
    },
    async syncVaeList() {
      this.loading_vae = true
      await this.sleep(300);
      let request = await fetch(this.getUrl('/api/v1/vae_list'), {method: 'GET', mode: 'cors'});
      let response = await request.json();
      console.log(response)
      this.vae_list = response['mode_list'];
      await this.getCurrentVae()
      this.loading_vae = false
    },
    async syncLoraList() {
      let request = await fetch(this.getUrl('/api/v1/lora_list'), {method: 'GET', mode: 'cors'});
      this.lora_model_list = await request.json();
    },
    remove_lora(index) {
      this.lora_models.splice(index, 1)
    },
    async load_lora_model() {
      this.loading_lora = true
      let request = await fetch(this.getUrl('/api/v1/load_lora'), {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          lora_networks: this.lora_models
        })
      });
      await this.load_current_lora()
      this.loading_lora = false
    },
    async load_current_lora() {
      this.loading_lora = true
      await this.sleep(100);
      let request = await fetch(this.getUrl('/api/v1/current_lora'), {method: 'GET', mode: 'cors'});
      this.current_lora = await request.json();
      this.loading_lora = false
    },
    copy_current_lora() {
      for (let i = 0; i < this.current_lora.length; i++)
        this.lora_models.push(this.current_lora[i])
    },
    compare_loaded_lora() {
      let current_lora_sorted = this.current_lora.sort((a, b) => {
        return a['name'] > b['name'] ? 1 : -1
      })
      let lora_models_sorted = this.lora_models.sort((a, b) => {
        return a['name'] > b['name'] ? 1 : -1
      })
      if (current_lora_sorted.length !== lora_models_sorted.length)
        return false
      for (let i = 0; i < current_lora_sorted.length; i++)
        if (current_lora_sorted[i]['name'] !== lora_models_sorted[i]['name'])
          return false
      return true
    },
    async syncSamplerList() {
      let request = await fetch(this.getUrl('/api/v1/sampler_list'), {method: 'GET', mode: 'cors'});
      let response = await request.json();
      this.sampler_options = response['sampler_list'];
    },
    async load_model() {
      this.loading_model = true
      const dismiss = this.$q.notify({
        spinner: true,
        message: `loading model ${this.model}...`,
        position: "top",
        timeout: 0,
      })
      let request = await fetch(this.getUrl(`/api/v1/load_model?ModelName=${this.model}&${this.vae}`), {method: 'GET', mode: 'cors'});
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
    async getCurrentVae() {
      let request = await fetch(this.getUrl('/api/v1/current_model'), {method: 'GET', mode: 'cors'});
      let info = request.json();
      this.vae = info['current_vae']
    },
    async getInfo() {
      let request = await fetch(this.getUrl('/api/v1/current_model'), {method: 'GET', mode: 'cors'});
      return request.json();
    },

    addNewPrompt() {
      this.Prompts.push({
        id: PromptID++,
        name: this.newPrompt
      })
      this.newPrompt = ''
    },

    removePrompt(prompt) {
      this.Prompts = this.Prompts.filter((t) => t !== prompt)
    },

    onSubmit(evt) {
      console.log('@submit - do something here', evt)
      evt.target.submit()
    },

  },
  mounted() {
    console.log("debug type:", this.$DEBUG)
    this.debug = this.$DEBUG;
  },
  async beforeMount() {
    this.loading_lora = true;
    await this.syncModelList()
    await this.syncVaeList()
    await this.syncLoraList()
    await this.load_current_lora()
    this.copy_current_lora()
    await this.getCurrentModel();
    await this.syncSamplerList();
    window.setInterval(this.syncTasks, 500);
    window.setInterval(this.syncGPUInfo, 200);

  },
  beforeUnmount() {
    this.$q.loading.hide()
  },
})
</script>

<style>
.hint-white {
  color: white;
}
</style>
