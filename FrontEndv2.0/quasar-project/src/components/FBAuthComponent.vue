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
  name: "FBAuthComponent",

  data() {
    return {
      fb:"",
      appID:"645161304039045",
      version:"v16.0",
      user_token:'',
      page_token:''
    };
  },

  methods: {
    async login () {
      const auth = getAuth()
      const pageId = '101969492843962'
      let fb = await signInWithPopup(auth, provider)
        .then((result) => {
          const credential = FacebookAuthProvider.credentialFromResult(result)
          const token = credential.accessToken
          const user = result.user
          console.log(token)
          this.user_token = token
          fetch(`https://graph.facebook.com/${pageId}?fields=access_token&access_token=${token}`)
            .then(response => response.json())
            .then(data => {
              const pageAccessToken = data.access_token
              console.log('Page access token:', pageAccessToken)
              this.page_token = pageAccessToken
            })
            .catch(error => {
              console.error('Error:', error);
            });
          this.$router.push("/FaceBookPost")
        }).catch((error) => {
          console.log(error.code)
          console.log(error.message)
        })
    }
  },
  mounted() {

  }
}
</script>

<style scoped>

</style>
