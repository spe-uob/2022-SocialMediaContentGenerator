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
const user_token = 'EAAJKxVJZAnoUBAOCAT1gMW6XieimRCjMAEnYS2ZACH0iolQJe6Hbc9X7rWyN15UyGJVIZClKHADXRavPcpDljROcCaef3UihisvTyZA2hbDZCBkpCTjezzB0IuuAcXE834Q6ipa7FQojMBjWdRGK3lThQUHB5yiYFeqgXlf4ZAd6ePni2m7wTnmXJa7KaURQQtHYbOLw7iE4z29MXW1TvG'
const page_token = 'EAAJKxVJZAnoUBAGbp87KcGG7wXX9voeP4diFHtgitKKDhVVWDLCPhfUK3i9dMfweA8ronmukO0pZCeuQXhpWZAnfJznXWYRQK50t0oBQZCtjusSUFSr90ylFBQxUNH62Yld8OrJwrUX3tstVD3AWyep2jTJoNxqp7wxqxucsafMpyTXFnsrvwMZCjIBDL4MOdZAZArscpxuwi0woRokIuuc'
const page_id = '101969492843962'
export default {
  name: "FBAuthComponent",

  data() {
    return {
      fb:"",
      appID:"645161304039045",
      version:"v16.0",
      message: '',
      access_token:''
    };
  },

  methods: {
    async login () {
      const auth = getAuth()
      let fb = await signInWithPopup(auth, provider)
        .then((result) => {
          const credential = FacebookAuthProvider.credentialFromResult(result)
          const token = credential.accessToken
          const user = result.user
          console.log(token)
          console.log(user)
          this.$router.push("/FaceBookPost")
        }).catch((error) => {
          console.log(error.code)
          console.log(error.message)
        })
    }
  }
}
</script>

<style scoped>

</style>
