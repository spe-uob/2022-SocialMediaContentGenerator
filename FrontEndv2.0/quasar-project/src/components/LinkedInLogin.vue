<template>
  <div>
    <!--<h1>LinkedIn API Authorization</h1>-->
    <div v-if="!authorized">
      <!--<p>Click the button to authorize this app to access your LinkedIn profile:</p>-->
      <q-btn class="flex justify-center full-width" color="light-blue" icon="fa-brands fa-linkedin" label="sign in with LinkedIn" @click="retrieveAccessToken" rounded/>
    </div>
    <div v-else>
      <p>You are authorized to access the LinkedIn API.</p>
      <p>Your access token is: {{ access_token }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import {myData, retrieveAccessToken, postToLinkedIn} from "app/LinkedInTest";
import qs from 'qs'

const client_id = '78sme225fsy5by'
const client_secret = 'J3xg14qRTV87viVq'
const redirect_uri = 'http://localhost:9000'
const scope = 'r_liteprofile r_emailaddress'
export default {
  name: "linkedInLogin",
  data() {
    return {
      authorized: false,
      access_token: '',
    }
  },
  methods: {
    retrieveAccessToken,
    /*authorize() {
      const state = Math.random().toString(36).substring(7)
      const linkedinAuthUrl = `https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=${client_id}&redirect_uri=${encodeURIComponent(redirect_uri)}&state=${state}&scope=${scope}`
      window.location.href = linkedinAuthUrl
    },*/
  }

}
</script>

<style scoped>

</style>
