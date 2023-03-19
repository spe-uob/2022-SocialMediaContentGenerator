<template>
  <div>
    <div class="flex flex-center">
      <VFBLogin app-id='645161304039045' @login='handleFacebookLogin' :firebase-provider='facebookAuthProvider'>
        <button>Login with Facebook</button>
      </VFBLogin>
    </div>
  </div>
</template>

<script>
import { getAuth, FacebookAuthProvider } from 'firebase/auth'
import { defineComponent } from 'vue'
import { VFBLogin } from 'vue-facebook-login-component-next'
import firebase from 'firebase/compat/app'

export default defineComponent({
  components: {
    VFBLogin
  },
  name: 'FaceBook',
  data () {
    return {
      facebookAuthProvider: new FacebookAuthProvider(),
      accessToken: ''
    }
  },
  methods: {
    async handleFacebookLogin (response) {
      const auth = getAuth()
      const { accessToken } = response.authResponse
      const credential = auth.FacebookAuthProvider.credential(accessToken)
      try {
        const userCredential = await auth().signInWithCredential(credential)
        const { user } = userCredential
        console.log('Firebase user:', user)
        // Handle the logged-in user here
      } catch (error) {
        console.error('Firebase login error:', error)
        // Handle login error here
      }
    }
  },
  created () {
    const firebaseConfig = {
      apiKey: 'AIzaSyBDwO_OvSwRkQJ66A_OFo4cOR51DdnLHsY',
      authDomain: 'test-b64fd.firebaseapp.com',
      projectId: 'test-b64fd',
      storageBucket: 'test-b64fd.appspot.com',
      messagingSenderId: '888879762179',
      appId: '1:888879762179:web:575028c2a264d7c8efb736',
      measurementId: 'G-JS1VSJ2JEH'
    }
    firebase.initializeApp(firebaseConfig)
    firebase.getCurrentUser = () => {
      return new Promise((resolve, reject) => {
        const unsubscribe = firebase.auth().onAuthStateChanged(user => {
          unsubscribe()
          resolve(user)
        }, reject)
      })
    }
  }
})

</script>

<style scoped>

</style>
