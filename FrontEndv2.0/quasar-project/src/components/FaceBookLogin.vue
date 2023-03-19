<template>
  <div>
    <div class="flex flex-center">

      <q-btn class="text-center full-width" color="blue" icon="fa-brands fa-facebook" label="sign in with facebook" type="submit" @click="login" rounded></q-btn>

      </div>
  </div>
</template>


<script>
import {getAuth,  FacebookAuthProvider, signInWithPopup} from "firebase/auth"
import firebase from "firebase/compat/app"

const provider = new FacebookAuthProvider();
export default {
  name: "FaceBookLogin",

  data() {
    return {
      fb:"",
      appID:"645161304039045",
      version:"v16.0",
      isConnected:false,
      message: '',
      access_token:''
    };
  },

  methods: {
    async login () {
      const auth = getAuth()
      const fb = await signInWithPopup(auth, provider)
        .then((result) => {
          const credential = result.credential
          const token = credential.accessToken
          const user = result.user
          console.log(token)
          console.log(user)
        }).catch((error) => {
          console.log(error.code)
          console.log(error.message)
        })
      this.fb = fb
    },
  }
}
</script>

<style scoped>

</style>
