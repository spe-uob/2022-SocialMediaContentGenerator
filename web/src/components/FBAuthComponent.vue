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
import axios from "axios";
const provider = new FacebookAuthProvider();
export default {
  name: "FBAuthComponent",

  data() {
    return {
      fb:"",
      appID:"645161304039045",
      version:"v16.0",
    };
  },

  methods: {
    async login () {
      const auth = getAuth()
      //const pageId = '119057271096466'
      await signInWithPopup(auth, provider)
        .then((result) => {
          const credential = FacebookAuthProvider.credentialFromResult(result)
          const userAccessToken = credential.accessToken
          const user = result.user
          const uid = user.uid
          axios.get(`https://graph.facebook.com/${this.version}/me/accounts?access_token=${userAccessToken}`)
            .then((response) => {
                const pages = response.data.data
                const page = pages.find((page) => page.tasks.includes('ADMIN'))
                const pageId = page.id
              fetch(`https://graph.facebook.com/${pageId}?fields=access_token&access_token=${userAccessToken}`)
                .then(response => response.json())
                .then(data => {
                  const pageAccessToken = data.access_token
                  const url = `http://127.0.0.1:8888/api/v1/facebookAuth`
                  const response = fetch(url, {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                      pageId:pageId,
                      userAccessToken:userAccessToken,
                      pageAccessToken:pageAccessToken
                    }),
                    mode: 'cors',
                  })
                  const res = response.json()
                  //this.$router.push("/FaceBookPost")
                  location.reload()
                })
                .catch(error => {
                  console.error('Error:', error);
                });
              }).catch((error) => {
            console.error('Error:', error)
          })
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
