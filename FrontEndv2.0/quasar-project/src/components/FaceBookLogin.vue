<template>
  <div>
    <div class="flex flex-center">
      <q-btn class="text-center full-width" color="blue" icon="fa-brands fa-facebook" label="sign in with facebook" type="submit" @click="logInWithFacebook" rounded></q-btn>
      </div>
  </div>
</template>

import axios from 'axios'

<script>
export default {
  name: "FaceBookLogin",

  data() {
    return {
      message: '',
    };
  },
  methods: {
    redirect() {
      this.$router.push("/FaceBook")
    },
    async logInWithFacebook() {
      await this.loadFacebookSDK(document, "script", "facebook-jssdk");
      await this.initFacebook();
      window.FB.login(function (response) {
        if (response.authResponse) {
          alert("login successfully");
        } else {
          alert("login failed");
        }
      });
      this.$router.push("/FaceBook")
      return false;
    },
    async initFacebook() {
      window.fbAsyncInit = function () {
        window.FB.init({
          appId: "645161304039045",
          cookie: true,
          version: "v16.0"
        });
      };
    },
    async loadFacebookSDK() {
      return new Promise(resolve => {
        window.fbAsyncInit = function () { // eslint-disable-line func-names
          FB.init({
            appId,
            xfbml: false,
            version,
            cookie: true
          });
          FB.AppEvents.logPageView();
          resolve('SDK Loaded!');
        };
        (function (d, s, id) { // eslint-disable-line func-names
          const fjs = d.getElementsByTagName(s)[0];
          if (d.getElementById(id)) { return; }
          const js = d.createElement(s); js.id = id;
          js.src = '//connect.facebook.net/en_US/sdk.js';
          fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));
      });
    }
  }
}
</script>

<style scoped>

</style>
