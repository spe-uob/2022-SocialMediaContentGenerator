<template>
 <div class="q-pa-md">
  <div class="q-gutter-md" style="max-width: 1800px">
    <q-input rounded outlined v-model="message" label="Text" >
      <template v-slot:append>
        <q-icon name="close" @click="message = ''" class="cursor-pointer"/>
      </template>
      <template v-slot:after>
        <q-icon name="send" @click="postToFacebook" color="primary" class="cursor-pointer" :disable="!message"/>
      </template>
      </q-input>
  </div>
 </div>
</template>

<script>
import axios from 'axios'
export default {
  name: "FaceBook",


  data() {
    return {
      message: ''
    };
  },
  methods: {
    async logInWithFacebook() {
      await this.loadFacebookSDK(document, "script", "facebook-jssdk");
      await this.initFacebook();
      window.FB.login(function(response) {
        if (response.authResponse) {
          alert("login successfully");
        } else {
          alert("login failed");
        }
      });
      this.$router.push("/twitter")
      return false;
    },
    async initFacebook() {
      window.fbAsyncInit = function() {
        window.FB.init({
          appId: "645161304039045",
          cookie: true,
          version: "v16.0"
        });
      };
    },
    async loadFacebookSDK(d, s, id) {
      let js,
        fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) {
        return;
      }
      js = d.createElement(s);
      js.id = id;
      js.src = "https://connect.facebook.net/en_UK/sdk.js";
      fjs.parentNode.insertBefore(js, fjs);
    }
  }
}

</script>

<style scoped>

</style>
