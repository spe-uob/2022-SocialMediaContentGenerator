<template>
  <q-btn label="Login with LinkedIn" @click="loginWithLinkedIn" />
</template>

<script>
import axios from 'axios';
export default {
  name: "loginWithLinkedIn",
  methods: {
    async loginWithLinkedIn() {
      try {
        const response = await axios.post('https://www.linkedin.com/oauth/v2/accessToken', {
          grant_type: 'authorization_code',
          code: 'AUTHORIZATION_CODE',
          redirect_uri: 'REDIRECT_URI',
          client_id: 'CLIENT_ID',
          client_secret: 'CLIENT_SECRET'
        });

       // const accessToken = response.data.access_token;
        const accessToken ='AQWhwY2PZI0VfUx-N_q9_zmV4QExn0X7UKOd1gXSKEZeunjyVtRMhNyipliSAuLHIcyeexoNvh3WwuG2WTH1fCtJ9ndMnE2meViNNa56mma5G-jfH4s1WKqEargNUNN205Lw65w5wfdidR2k3kDH8eY9-dK3snyM4Ki_RB9hRCBuwMAbLeeDhQDOHU46RFV4PUn6_7V9hWO35oN43Z7j1hADJyOE3aLrcbKHohTH9z5__ALvTvlkw2X4l8gYJA9K6cJyd4oGXZIJ3cFkGJZgz7ij31inj5HoULfrVZ68H7T3OWywPkBinewQgtohhtzTpmsFFY1njDZ6JcUEWT4A74wHDYicTA';


        // Use the access token to make API requests and retrieve user data
        await this.retrieveUserData(accessToken);
      } catch (error) {
        console.error(error);
      }
    },

    async retrieveUserData(accessToken) {
      try {
        const response = await axios.get('https://api.linkedin.com/v2/me', {
          headers: {
            Authorization: `Bearer ${accessToken}`
          }
        });

        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    }
  }
}
</script>

<style scoped>

</style>
