<template>
  <q-page class="flex flex-center">
    <img
      alt="Quasar logo"
      src="~assets/quasar-logo-vertical.svg"
      style="width: 200px; height: 200px"
    >
    <q-btn class="text-center full-width" color="blue" icon="fa-brands fa-facebook" label="sign in with facebook" type="submit" @click="login" rounded></q-btn>
    <v-facebook-login app-id="645161304039045">
      <q-btn class="text-center full-width" color="blue" icon="fa-brands fa-facebook" label="sign in with facebook" type="submit"  rounded></q-btn>
    </v-facebook-login>
    <FaceBook @login="handleFacebookLogin"></FaceBook>

  </q-page>
</template>

<script>
import VFacebookLogin from 'vue-facebook-login-component-next'
import { defineComponent } from 'vue'
import FaceBook from 'components/FaceBook'
import { getAuth, signInWithPopup, FacebookAuthProvider } from 'firebase/auth'
const provider = new FacebookAuthProvider()
export default defineComponent({
  components: {
    FaceBook,
    VFacebookLogin
  },
  name: 'IndexPage',
  data () {
    return {
      fb: '',
      text: '',
      image: '',
      accessToken: '',
      displayName: ''
    }
  },
  methods: {
    handleFacebookLogin (user) {
      this.displayName = user.displayName
    },
    async login () {
      const auth = getAuth()
      const fb = await signInWithPopup(auth, provider)
        .then((result) => {
          const credential = result.credential
          const token = credential.accessToken
          const user = result.user
          console.log(token)
          console.log(user)
        }).catch((error) => {
          console.log(error.code)
          console.log(error.message)
        })
      this.fb = fb
    },
    logout () {
      const auth = getAuth()
      auth.signOut()
        .then(() => {
          console.log('Logout Successful')
        })
    }
  }
})

</script>
