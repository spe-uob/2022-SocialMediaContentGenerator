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
  <a class="twitter-timeline"
     href = "https://twitter.com/${this.twitterUsername}"
     data-aria-polite="assertive">
  <!--:href = "'https://twitter.com/' + temp">{{temp}}-->
    <!--data-chrome="nofooter"-->
    Tweets by @{{temp}}
  </a>
  <a v-html="twitterTimelineLink"></a>

</template>

<script >
import {data} from 'browserslist';
import {defineComponent} from 'vue'
import AuthComponent from '../components/AuthComponent.vue'

console.log(AuthComponent.data().token);
console.log(AuthComponent.data().displayName);
const temp =  AuthComponent.data().displayName;
const test = "https://twitter.com/" + temp;
console.log(test)

export default defineComponent({
  name: "Twitter",
  props: [test, temp],
  data() {
    return {
      text: '',
      image: '',
      consumer_key: AuthComponent.data().apiKey,
      consumer_secret: AuthComponent.data().apiSecret,
      access_token: AuthComponent.data().token,
      access_token_secret: AuthComponent.data().secret,
      twitterUsername: AuthComponent.data().displayName,
    }
  },
  methods: {


    async addNewTweetPost(){
      /*let tweet = this.text
      const url = `http://localhost:5000/tweet?status=${encodeURIComponent(tweet)}&consumer_key=${encodeURIComponent(AuthComponent.data().apiKey)}&consumer_secret=${encodeURIComponent(AuthComponent.data().apiSecret)}&access_token=${encodeURIComponent(AuthComponent.data().token)}&access_token_secret=${encodeURIComponent(AuthComponent.data().secret)}`
      const response = await fetch(url)
      const data = await response.json()
      console.log(data)*/

      let tweet = this.text
      const url = `http://localhost:8888/api/v1/twitter`
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
  },

  setup(){
    return {
      test,
      temp,
    }
  }

})
</script>

<style scoped>

</style>
