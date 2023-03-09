<template>
  <div>
    <div class="flex flex-center">
      <q-btn class="text-center full-width" color="blue" icon="fa-brands fa-facebook" label="sign in with facebook" type="submit" @click="FB_firebase" rounded></q-btn>
      </div>
  </div>
</template>


<script>
import {getAuth,  FacebookAuthProvider, signInWithPopup} from "firebase/auth"
import {FBLogin, getFBLoginStatus, loadFBSDK} from "boot/FB"
const provider = new FacebookAuthProvider();
export default {
  name: "FaceBookLogin",

  data() {
    return {
      appID:"645161304039045",
      version:"v16.0",
      isConnected:false,
      message: '',
    };
  },

  methods: {
    async FB_firebase(){
      const auth = getAuth();
      signInWithPopup(auth, provider)
        .then((result) => {
          const user = result.user;
          const credential = FacebookAuthProvider.credentialFromResult(result);
          const accessToken = credential.accessToken;
        })
        .catch((error) => {
          const errorCode = error.code;
          const errorMessage = error.message;
          const email = error.customData.email;
          const credential = FacebookAuthProvider.credentialFromError(error);
        },
      this.$router.push("/FaceBook"));

    },
    FB_fbsdk(){
      FBLogin(this.loginOptions)
        .then(response => {
          if (response.status === 'connected') {
            this.isConnected = true;
          } else {
            this.isConnected = false;
          }
          this.$emit('login', {
            response,
            FB: window.FB
          })
        });


    },

    mounted() {
      loadFBSDK(this.appId, this.version)
        .then(loadingResult => {
        })
        .then(() => getLoginStatus())
        .then(response => {
          if (response.status === 'connected') {
            this.isConnected = true;
          }
          this.$emit('get-initial-status', response);
          this.$emit('sdk-loaded', {
            isConnected: this.isConnected,
            FB: window.FB
          })
        });
    }
  }
}
</script>

<style scoped>

</style>
