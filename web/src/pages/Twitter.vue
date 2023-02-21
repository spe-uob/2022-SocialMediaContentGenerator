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
        <q-icon name="close" @click="text = ''" class="cursor-pointer"/>
      </template>
      <template v-slot:after>
        <q-icon name="send" @click="addNewTweetPost" color="primary" class="cursor-pointer" :disable="!text"/>
      </template>
    </q-input>
    <q-img :src="image" style="max-width: 40vw"></q-img>
    <q-file color="purple-12" @update:model-value="uploadImage($event)" label="Add images">
      <template v-slot:prepend>
        <q-icon name="attach_file"/>
      </template>
    </q-file>
  </div>
</template>

<script>
import {data} from 'browserslist';
import {defineComponent} from 'vue'
import AuthComponent from '../components/AuthComponent.vue'

export default defineComponent({
  name: "TwitterComp",
  data() {
    return {
      text: '',
      image: ''
    }
  },
  methods: {
    async addNewTweetPost(){
      let tweet = this.text
      const url = `/api/v1/tweet`
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          status: tweet,
          consumer_key: AuthComponent.data().apiKey,
          consumer_secret: AuthComponent.data().apiSecret,
          access_token: AuthComponent.data().token,
          access_token_secret: AuthComponent.data().secret,
          image: this.image
        }),
        mode: 'cors',
      })
      const data = await response.json()
      console.log(data)

      let newTweet = {
        content: this.text,
        date: Date.now()
      }
      this.text = ''
    },
    getBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = () => resolve(reader.result)
        reader.onerror = error => reject(error)
      })
    },
    async uploadImage(files) {
      this.image = await this.getBase64(files)
    },
  }
})
</script>

<style scoped>

</style>
