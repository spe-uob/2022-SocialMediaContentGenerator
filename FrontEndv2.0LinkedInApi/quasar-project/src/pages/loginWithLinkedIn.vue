<template>
  <q-btn label="Login with LinkedIn" @click="authorize" />
</template>

<script>
import { linkedinAuthUrl, getAccessToken } from '../boot/linkedin.js'
export default {

  name: "loginWithLinkedIn",
  methods: {
    authorize() {
      // Redirect the user to the LinkedIn authorization page
      window.location.href = linkedinAuthUrl
    },
    retrieveAccessToken() {
      const code = new URLSearchParams(window.location.search).get('code')
      if (code) {
        getAccessToken(code)
          .then(access_token => {
            // Use the access token to make API requests
            axios.get('https://api.linkedin.com/v2/me', {
              headers: {
                'Authorization': `Bearer ${access_token}`,
                'cache-control': 'no-cache',
                'X-Restli-Protocol-Version': '2.0.0',
              }
            })
              .then(response => {
                // Handle the API response
                console.log(response.data)
              })
              .catch(error => {
                // Handle the API error
                console.error(error)
              })
          })
          .catch(error => {
            // Handle the access token retrieval error
            console.error(error)
          })
      }
    }
  },
  mounted() {
    this.retrieveAccessToken()
  }
}


</script>

<style scoped>

</style>
