<template>
  <div>
    <q-toolbar
    :class="$q.dark.isActive ? 'bg-grey-2' : 'bg-white'">
      <div class="col"></div>
      <div>
        <span class="text-grey-5"> Signed in as {{ this.displayName }}</span>
        <q-btn class="q-mx-md text-grey-5" flat to="/signin" v-ripple @click="signOut()">
          <q-icon name="fa-solid fa-sign-out" class="q-mr-xs"/>
          Sign Out
        </q-btn>
      </div>
    </q-toolbar>
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
    <!--<q-img :src="image" style="max-width: 40vw"></q-img>-->
    <q-file color="purple-12" @update:model-value="uploadImage($event)" label="Add images">
      <template v-slot:prepend>
        <q-icon name="attach_file"/>
      </template>
    </q-file>
    <img
    class="col justify-end"
    :src="`data:image/png;base64,${this.image}`"/>
  </div>
  <a class="twitter-timeline"
     href = "https://twitter.com/${this.twitterUsername}"
     data-aria-polite="assertive">
    Tweets by @{{this.screenName}}
  </a>

</template>

<script >
import {defineComponent} from 'vue'
import AuthComponent from '../components/AuthComponent.vue'
import { getAuth, onAuthStateChanged } from "firebase/auth"

const token = localStorage.getItem('token')
const secret = localStorage.getItem('secret')
const displayName = localStorage.getItem('displayName')
const screenName = localStorage.getItem('screenName')
console.log("name:" + name)

const auth = getAuth()
onAuthStateChanged(auth, (user) => {
  if (user) {
    console.log(user)
  }
  else {
    console.log("No user")
    this.$router.push("/signin")
  }
})

export default defineComponent({
  name: "Twitter",
  data() {
    return {
      text: '',
      image: '',
      displayName: displayName,
      screenName: screenName,
    }
  },
  methods: {
    signOut() {
      auth.signOut().then(function() {
        console.log('Signed Out')
        localStorage.removeItem('token')
        localStorage.removeItem('secret')
        localStorage.removeItem('displayName')
        localStorage.removeItem('screenName')
      }, function(error) {
        console.error('Sign Out Error', error);
      });
    },
    async addNewTweetPost(){
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
          access_token: token,
          access_token_secret: secret,
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
      var s = await this.getBase64(files)
      var base64result = s.split(',')[1];
      this.image = base64result
    }
  },
})
</script>

<style scoped>

</style>
