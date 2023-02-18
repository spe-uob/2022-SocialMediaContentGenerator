<template>
  <div>
    <div class="flex flex-center">
      <!--<q-btn class="flex flex-center q-px-lg q-py-sm q-mb-md" color="primary" size="md"  label="Twitter"
        @click="twitter"
      />-->
      <q-btn ref="button" class="text-center full-width" color="light-blue" icon="fa-brands fa-twitter" label="sign in with twitter" type="submit" rounded @click="twitter"/>
    </div>
  </div>
</template>

<script>
  import { getAuth, signInWithPopup, TwitterAuthProvider } from "firebase/auth"
  const provider = new TwitterAuthProvider()
  const apiKey = 'EzoH0w73hC3naY84U6NBHZHyz'
  const apiSecret = 'qjFQ5WPxqJD7C0JZtMiORkzbhYAXjNNfX0WyMdx5GWz1IiZxFw'
  var token = ''
  var secret = ''

  export default {
    name: "AuthComponent",
    props: [],
    data: function(){
      return {
      apiKey: apiKey,
      apiSecret: apiSecret,
      token: token,
      secret: secret,
    }
    },
    methods: {
      async twitter () {
        const auth = getAuth()
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
            this.$router.push("/twitter")
            return [token,secret]
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
    }
  }
</script>
