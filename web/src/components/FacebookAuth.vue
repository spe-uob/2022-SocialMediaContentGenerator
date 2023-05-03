<template>
  <div>
    <div class="flex flex-center">
      <q-btn class="flex justify-center full-width" color="blue" icon="fa-brands fa-facebook" type="submit" @click="login" rounded style="min-height:50px; min-width:270px;">
        <span class="q-pl-xs">
          Sign in with Facebook
        </span>
      </q-btn>
    </div>
  </div>
</template>


<script>
import {getAuth, FacebookAuthProvider, signInWithPopup} from "firebase/auth"
import firebase from "firebase/compat/app"
import axios from "axios";

const provider = new FacebookAuthProvider();
export default {
  name: "FacebookAuth",

  data() {
    return {
      appID: "",
      version: "v16.0",
      base_url: '',
    };
  },

  methods: {
    getUrl(path) {
      return this.base_url + path;
    },
    async getAppid() {
      let response = await fetch(this.getUrl("/api/v1/Key"));
      let data = await response.json();
      this.appID = data['facebook_auth'].appid;
    },
    async login() {
      const auth = getAuth()
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
              const pageId = page.Page.id
              //const pageId = '119057271096466'
              fetch(`https://graph.facebook.com/${pageId}?fields=access_token&access_token=${userAccessToken}`)
                .then(response => response.json())
                .then(data => {
                  const pageAccessToken = data.access_token
                  const url = this.getUrl("api/v1/Login")
                  const response = fetch(url, {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                      platform: 'facebook',
                      pageId: pageId,
                      userAccessToken: userAccessToken,
                      pageAccessToken: pageAccessToken
                    }),
                    mode: 'cors',
                  })
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
    console.log("debug type:", this.$DEBUG)
    this.debug = this.$DEBUG;
    this.base_url = this.$BASEURL;
    this.getAppid();
  }
}
</script>

<style scoped>

</style>
