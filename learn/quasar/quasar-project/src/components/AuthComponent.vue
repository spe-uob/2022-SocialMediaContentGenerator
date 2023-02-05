<template>
  <div>
    <template v-if="tab === 'register'">
      <div class="text-center q-mb-lg">Sign up with</div>
    </template>
    <template v-else>
      <div class="text-center q-mb-lg">Sign in with</div>
    </template>
    <div class="flex flex-center">
      <q-btn class="flex flex-center q-px-lg q-py-sm q-mb-md" color="primary" size="md"  label="Twitter"
        @click="twitter"
      />
    </div>
    <template v-if="tab === 'register'">
      <p class="text-center">Sign up with credentials</p>
    </template>
    <template v-else>
      <p class="text-center">Sign in with credentials</p>
    </template>

    <q-form @submit="submitForm">
      <q-input outlined class="q-mb-md" type="email" label="Email" v-model="formData.email" />
      <q-input outlined class="q-mb-md" type="password" label="Password" v-model="formData.password" />
      <div class="row">
        <q-space />
        <q-btn type="submit" color="primary" :label="tab" />
      </div>
    </q-form>
    <div class="text-center q-my-md">
      <q-btn flat label="Forgot Password?" color="green" class="text-capitalize rounded-borders"
        v-if="tab !== 'register'" @click="forgotPassword" />
    </div>
  </div>
</template>

<script>
  import { getAuth, signInWithPopup, TwitterAuthProvider } from "firebase/auth"
  const auth = getAuth();
  const provider = new TwitterAuthProvider()
  const apiKey = 'EzoH0w73hC3naY84U6NBHZHyz'
  const apiSecret = 'qjFQ5WPxqJD7C0JZtMiORkzbhYAXjNNfX0WyMdx5GWz1IiZxFw'
  var token = ''
  var secret = ''

  export default {
    name: "AuthComponent",
    props: ['tab'],
    data: function(){
      return {
        formData: {
        email: '',
        password: '',
      },
      apiKey: apiKey,
      apiSecret: apiSecret,
      token: token,
      secret: secret
    }
    },
    methods: {
      submitForm () {
        if (this.tab === 'login') {
          this.signInExistingUser(this.formData.email, this.formData.password)
        } else {
          this.createUser(this.formData.email, this.formData.password)
        }
      },
      async twitter () {
        var t = await signInWithPopup(auth, provider)
        .then((result) => {
            // This gives you a the Twitter OAuth 1.0 Access Token and Secret.
            // You can use these server side with your app's credentials to access the Twitter API.
            const credential = TwitterAuthProvider.credentialFromResult(result);
            const token = credential.accessToken;
            const secret = credential.secret;
            // The signed-in user info.
            const user = result.user;
            // ...
            this.$router.push("/home")
            return [token, secret]
          }).catch((error) => {
            // Handle Errors here.
            const errorCode = error.code;
            const errorMessage = error.message;
            console.log(errorCode, errorMessage)
            // The email of the user's account used.
            //const email = error.customData.email;
            // The AuthCredential type that was used.
            const credential = TwitterAuthProvider.credentialFromError(error);
            // ...
          })
          token = t[0]
          secret = t[1]
        },
      signInExistingUser (email, password) {
        console.log(email, password)
      },
      createUser(email, password) {
        console.log(email, password)
      },
    }
  }
</script>
