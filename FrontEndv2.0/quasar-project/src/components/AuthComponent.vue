<template>
  <div>
    <div class="flex flex-center">
      <q-btn ref="button" class="flex justify-center full-width" color="light-blue" icon="fa-brands fa-twitter" label="sign in with twitter" type="submit" rounded @click="twitter"/>
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
  var displayName = ''

  export default {
    name: "AuthComponent",
    props: ['tab', 'screenName'],
    data: function(){
      return {
        formData: {
        email: '',
        password: '',
          displayName:'',
      },
      apiKey: apiKey,
      apiSecret: apiSecret,
      token: token,
      secret: secret,
      displayName: displayName
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
            //const displayName = result.additionalUserInfo
            // The signed-in user info.
            const user = result.user;
            console.log(user.displayName)

            displayName = user.displayName
            console.log(displayName)
            console.log(secret)
            // ...
            this.$router.push("/twitter")
            return [token, secret, displayName]
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
          console.log(displayName);
          token = t[0]
          secret = t[1]
          //displayName = t[2]
        },
    }
  }
</script>
