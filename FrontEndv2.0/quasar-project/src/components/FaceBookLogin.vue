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
import {FBLogin,InitSDK} from "../boot/FB"

const provider = new FacebookAuthProvider();
export default {
  name: "FaceBookLogin",

  data() {
    return {
      fb:"",
      appID:"645161304039045",
      version:"v16.0",
      isConnected:false,
      message: '',
      access_token:''
    };
  },

  methods: {
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
  }
}
</script>

<style scoped>

</style>
