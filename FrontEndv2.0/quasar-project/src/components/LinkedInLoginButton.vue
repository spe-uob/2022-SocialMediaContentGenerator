<template>
 <!-- <q-btn @click="handleLinkedInLogin" label="Login with LinkedIn" />-->
  <q-btn class="text-center full-width" @click="handleLinkedInLogin" color="blue" icon="fa-brands fa-linkedin" label="sign in with linkedIn" type="submit" rounded></q-btn>

</template>


<script>
import axios from 'axios'
export default {
  name: "LinkedInLoginButton",
  methods: {
    handleLinkedInLogin() {
      // Set the access token received from LinkedIn after authentication
      const accessToken = 'AQWhwY2PZI0VfUx-N_q9_zmV4QExn0X7UKOd1gXSKEZeunjyVtRMhNyipliSAuLHIcyeexoNvh3WwuG2WTH1fCtJ9ndMnE2meViNNa56mma5G-jfH4s1WKqEargNUNN205Lw65w5wfdidR2k3kDH8eY9-dK3snyM4Ki_RB9hRCBuwMAbLeeDhQDOHU46RFV4PUn6_7V9hWO35oN43Z7j1hADJyOE3aLrcbKHohTH9z5__ALvTvlkw2X4l8gYJA9K6cJyd4oGXZIJ3cFkGJZgz7ij31inj5HoULfrVZ68H7T3OWywPkBinewQgtohhtzTpmsFFY1njDZ6JcUEWT4A74wHDYicTA';

      // Define the API endpoint URL and query parameters
      const apiUrl = 'https://api.linkedin.com/v2/me';
      const queryParams = {
        projection: '(id,firstName,lastName,profilePicture(displayImage~:playableStreams))',
      };

      // Set the headers with the access token and Content-Type
      const headers = {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      };

      // Send the GET request to the LinkedIn API
      axios.get(apiUrl, {
        params: queryParams,
        headers: headers,
      })
        .then(response => {
          console.log(response.data);
          // Handle the response data here
        })
        .catch(error => {
          console.log(error);
          // Handle the error here
        });
    },
  },
};

</script>

<style scoped>

</style>
