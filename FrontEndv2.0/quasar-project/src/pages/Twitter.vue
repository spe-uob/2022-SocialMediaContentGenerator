<template>
  <div>
    <q-input
      rounded
      outlined
      v-model="text"
      class="q-pa-md"
      autogrow
      maxlength="100"
      >
      <template v-slot:append>
            <q-icon name="close" @click="text = ''" class="cursor-pointer" />
      </template>
      <template v-slot:after>
            <q-icon name="send" @click="addNewTweet" color="primary" class="cursor-pointer" :disable="!text" />
      </template>
    </q-input>
  </div>
</template>

<script>
import { data } from 'browserslist';
import { defineComponent } from 'vue'
import AuthComponent from '../components/AuthComponent.vue'

export default defineComponent({
  name: "Twitter",
  data() {
    return {
      text: ''
    }
  },
  methods: {
    async addNewTweet() {
    console.log(AuthComponent.data())
    let tweet = this.text
    const url = `http://localhost:5000/tweet?status=${encodeURIComponent(tweet)}&consumer_key=${encodeURIComponent(AuthComponent.data().apiKey)}&consumer_secret=${encodeURIComponent(AuthComponent.data().apiSecret)}&access_token=${encodeURIComponent(AuthComponent.data().token)}&access_token_secret=${encodeURIComponent(AuthComponent.data().secret)}`
    const response = await fetch(url)
    const data = await response.json()
    console.log(data)

    let newTweet = {
    content: this.text,
      date: Date.now()
    }
    this.text = ''
    },
  }
})
</script>

<style scoped>

</style>
