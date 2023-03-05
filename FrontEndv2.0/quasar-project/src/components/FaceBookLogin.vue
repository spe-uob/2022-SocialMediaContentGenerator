<template>
  <div>
    <div class="flex flex-center">
      <q-btn class="text-center full-width" color="blue" icon="fa-brands fa-facebook" label="sign in with facebook" type="submit" @click="FaceBook" rounded></q-btn>
      </div>
  </div>
</template>


<script>
import {getAuth,  FacebookAuthProvider, signInWithPopup} from "firebase/auth"
const provider = new FacebookAuthProvider();
export default {
  name: "FaceBookLogin",

  data() {
    return {
      isConnected:false,
      message: '',
    };
  },

  methods: {
    async FaceBook(){
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
  }
}
</script>

<style scoped>

</style>
