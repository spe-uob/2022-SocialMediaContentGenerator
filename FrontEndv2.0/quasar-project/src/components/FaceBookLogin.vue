<template>
  <div>
    <div class="flex flex-center">
      <q-btn class="text-center full-width" color="blue" icon="fa-brands fa-facebook" label="sign in with facebook" type="submit" @click="FaceBookLogin" rounded></q-btn>
      </div>
  </div>
</template>

<script>
export default {
  name: "FaceBookLogin",

  data() {
    return {
      FB: window.FB,
      response: {
        status: 'connected',
        authResponse:
          {
            accessToken: '...',
            expiresIn:
              '...',
            signedRequest:
              '...',
            userID:
              '...'
          }
      }
    }
  },

      methods:{
      FaceBookLogin () {
        this.FB.getLoginStatus(function (response) {
          statusChangeCallback(response);
        });


        window.fbAsyncInit = function () {
          this.FB.init({
            appId: '{645161304039045}',
            cookie: true,
            xfbml: true,
            version: '{api-version}'
          });

          FB.AppEvents.logPageView();

        },

          (function (d, s, id) {
            let js, fjs = d.getElementsByTagName(s)[0];
            if (d.getElementById(id)) {
              return;
            }
            js = d.createElement(s);
            js.id = id;
            js.src = "https://connect.facebook.net/en_US/sdk.js";
            fjs.parentNode.insertBefore(js, fjs);
          }(document, 'script', 'facebook-jssdk'));
      }
    },
  }
</script>

<style scoped>

</style>
