<template>
  <q-page>
    <div class="col flex justify-center">
      <div class="row q-pa-lg" style="width: 90%;">
        <div class="col-4 q-pa-sm">
          <q-card>
            <q-card-section>
              <div class="text-h6">Generator arguments:</div>
            </q-card-section>
            <q-separator inset/>
            <q-card-section v-if="!template_mode">
              <q-toggle v-model="template_mode">Use fast template mode</q-toggle>
              <q-input v-model="prompt" filled autogrow hint="prompt"/>
              <q-badge color="secondary">
                Degrees of freedom: {{ freedom }} (0 to 1)
              </q-badge>
              <q-slider v-model="freedom" :min="0" :max="1" :step="0.1"/>
            </q-card-section>
            <q-card-section v-else>
              <q-toggle class="q-ma-none" v-model="template_mode">Use fast template mode</q-toggle>
              <q-input class="q-my-sm" label="number of generate lines" v-model="number_line" type="number"></q-input>
              <q-input class="q-my-sm" label="the key words about the topic" v-model="key_words"/>
              <q-input class="q-my-sm" v-model="prompt" filled autogrow disable hint="prompt"/>
            </q-card-section>
            <q-card-section>
              <q-btn label="Generate" color="primary" @click="generate"/>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-8 q-pa-sm">
          <q-card>
            <q-card-section>
              <div class="text-h6">Generated result:</div>
              <div class="text-subtitle2"></div>
            </q-card-section>
            <q-separator inset/>
            <q-card-section style="min-height: 231px">
              <span v-html="generator_output"></span>
              <q-inner-loading
                :showing="loading"
                label="Please wait..."
                label-class="text-teal"
                label-style="font-size: 1.1em"
              />
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  name: "TextGenerator",
  data() {
    return {
      base_url: '',
      prompt: '',
      generator_output: '',
      freedom: 0.5,
      number_line: 1,
      key_words: '',
      loading: false,
      template_mode: false,
      template: {
        part1: "please give me ",
        part2_1: " group of prompt for generate image by Stable Diffusion about ",
        part2_2: " groups of prompt for generate image by Stable Diffusion about "
      }
    };
  },
  watch: {
    number_line: function () {
      this.update_template()
    },
    key_words: function () {
      this.update_template()
    }
  },
  methods: {
    getUrl(path) {
      return this.base_url + path;
    },
    update_template() {
      if (this.number_line === 1) {
        this.prompt = this.template.part1 + this.number_line + this.template.part2_1 + this.key_words
      } else {
        this.prompt = this.template.part1 + this.number_line + this.template.part2_2 + this.key_words
      }
    },
    async generate() {
      this.loading = true;
      let response = await fetch(this.getUrl('/api/v1/text_generator'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        mode: 'cors',
        body: JSON.stringify({
          prompt: this.prompt,
          temp: this.freedom
        })
      });
      let data = await response.json();
      if (data['status'] === 'ok') {
        this.generator_output = data.text.replaceAll('\n', '<br />');
      } else {
        this.$q.notify({
          message: "Error generating text" + data['message'],
          color: 'negative',
          icon: 'report_problem'
        })
      }
      this.loading = false;
    },
  },
  mounted() {
    console.log("debug type:", this.$DEBUG)
    this.debug = this.$DEBUG;
    this.base_url = this.$BASEURL;
  }
}
</script>

<style scoped>
</style>
