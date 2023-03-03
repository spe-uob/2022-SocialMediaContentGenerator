<template>
  <div>
    <div class="flex flex-center">
      <q-btn class="text-center full-width" color="blue" icon="fa-brands fa-facebook" label="sign in with facebook" type="submit" @click="logInWithFacebook" rounded></q-btn>
      </div>
  </div>
</template>


<script>
import {getFBLoginStatus, loadFBSDK} from "boot/FB";
export default {
  name: "FaceBookLogin",

  data() {
    return {
      isConnected:false,
      message: '',
    };
  },
  mounted() {
    loadFBSDK()
      .then(getFBLoginStatus)
      .then(response => {
        if (response.status === 'connected') {
          this.isConnected = true
        }
      })
  },
  methods: {
    redirect() {
      this.$router.push("/FaceBook")
    },
    logInWithFacebook(){
      this.redirect()
    }

  }
}
</script>

<style scoped>

</style>
