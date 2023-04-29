<template>
  <div>
    <!--<h1>LinkedIn API Authorization</h1>-->
    <div v-if="!authorized">
      <!--<p>Click the button to authorize this app to access your LinkedIn profile:</p>-->
      <q-btn class="flex justify-center full-width" color="blue-2" icon="fa-brands fa-linkedin" @click="authorize" rounded style="min-height:50px; min-width:270px">
        <span class="q-pl-xs">
          Sign in with LinkedIn
        </span>
      </q-btn>
    </div>
    <div v-else>
      <p>You are authorized to access the LinkedIn API.</p>
      <p>Your access token is: {{ access_token }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import qs from 'qs'

const client_id = '78sme225fsy5by'
const client_secret = 'J3xg14qRTV87viVq'
const redirect_uri = 'http://localhost:9000/PostPage'
const scope = 'r_liteprofile r_emailaddress'
export default {
  name: "linkedInLogin",
  data() {
    return {
    }
  },
  methods: {
    authorize() {
      const state = Math.random().toString(36).substring(7)
      const linkedinAuthUrl = `https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=${client_id}&redirect_uri=${encodeURIComponent(redirect_uri)}&state=${state}&scope=${scope}`
      window.location.href = linkedinAuthUrl
      //this.$router.push("/LinkedInPost")
    },
    retrieveAccessToken() {
      const code = new URLSearchParams(window.location.search).get('code')
      if (code) {
        const data = {
          grant_type: 'authorization_code',
          code,
          redirect_uri,
          client_id,
          client_secret,
        }

        const headers = {
          'Content-Type': 'application/x-www-form-urlencoded',
        }

        axios.post('https://www.linkedin.com/oauth/v2/accessToken', qs.stringify(data), { headers })
          .then(response => {
            const access_token = response.data.access_token
            const url = `http://localhost:8888/api/v1/Login`
            fetch(url, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                platform:'linkedin',
                code:code
              }),
              mode: 'cors',
            })
          })
          .catch(error => console.error(error))
      }
    },
  },
  mounted() {
    this.retrieveAccessToken()
  },
}
</script>

<style scoped>

</style>
