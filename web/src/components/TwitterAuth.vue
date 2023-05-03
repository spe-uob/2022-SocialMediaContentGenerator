<template>
  <div>
    <div class="flex flex-center">
      <q-btn ref="button" class="flex justify-center full-width" color="light-blue" icon="fa-brands fa-twitter" type="submit" rounded @click="twitter" style="min-height:50px; min-width:270px;">
        <span class="q-pa-xs">
          Sign in with Twitter
        </span>
      </q-btn>
    </div>
  </div>
</template>

<script>
import {getAuth, signInWithPopup, TwitterAuthProvider, onAuthStateChanged} from "firebase/auth"
import {auth} from "./../boot/firebase.js"

const provider = new TwitterAuthProvider
export default {
  name: "TwitterAuth",
  data: function () {
    return {
      base_url: '',
    }
  },
  methods: {
    getUrl(path) {
      return this.base_url + path;
    },
    getKey(key) {

    },
    async twitter() {
      await signInWithPopup(auth, provider)
        .then(async (result) => {
          // This gives you a the Twitter OAuth 1.0 Access Token and Secret.
          // You can use these server side with your app's credentials to access the Twitter API.
          const credential = TwitterAuthProvider.credentialFromResult(result);
          const token = credential.accessToken;
          const secret = credential.secret;
          //const displayName = result.additionalUserInfo
          // The signed-in user info.
          // ...
          const url = this.getUrl(`/api/v1/Login`)
          const response = await fetch(url, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              platform: 'twitter',
              access_token: token,
              access_token_secret: secret
            }),
            mode: 'cors',
          })
          // eslint-disable-next-line no-unused-vars
          const data = await response.json()
          //this.$router.push("/twitter")
          //location.reload()
        }).catch((error) => {
          // Handle Errors here.
          const errorCode = error.code;
          const errorMessage = error.message;
          console.log(errorCode, errorMessage)
          // The email of the user's account used.
          //const email = error.customData.email;
          // The AuthCredential type that was used.
          const credential = TwitterAuthProvider.credentialFromError(error);
          // ...
        })
    },
  }, mounted() {
    console.log("debug type:", this.$DEBUG)
    this.debug = this.$DEBUG;
    this.base_url = this.$BASEURL;
  }
}
</script>
