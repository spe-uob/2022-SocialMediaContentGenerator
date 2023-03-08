<template>
  <q-page>
    <q-card class="q-mb-md">
      <q-card-section>
        <h2 class="q-ma-none">Publish a post on LinkedIn</h2>
      </q-card-section>
      <q-card-section>
        <q-form @submit="publishPost">
          <q-input v-model="post.subject" label="Post subject"></q-input>
          <q-input v-model="post.text.text" label="Post text" type="textarea"></q-input>
          <q-btn type="submit" label="Publish post"></q-btn>
        </q-form>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
import axios from 'axios';
export default {
  name: "MyLinkedInPage",
  data () {
    return {
      post: {
        subject: '',
        text: {
          text: ''
        }
      },
      accessToken: 'AQWhwY2PZI0VfUx-N_q9_zmV4QExn0X7UKOd1gXSKEZeunjyVtRMhNyipliSAuLHIcyeexoNvh3WwuG2WTH1fCtJ9ndMnE2meViNNa56mma5G-jfH4s1WKqEargNUNN205Lw65w5wfdidR2k3kDH8eY9-dK3snyM4Ki_RB9hRCBuwMAbLeeDhQDOHU46RFV4PUn6_7V9hWO35oN43Z7j1hADJyOE3aLrcbKHohTH9z5__ALvTvlkw2X4l8gYJA9K6cJyd4oGXZIJ3cFkGJZgz7ij31inj5HoULfrVZ68H7T3OWywPkBinewQgtohhtzTpmsFFY1njDZ6JcUEWT4A74wHDYicTA'
    }
  },
  methods: {
    publishPost () {
      const shareEndpoint = 'https://api.linkedin.com/v2/shares';
      const postData = {
        owner: 'urn:li:person:USER_ID',
        subject: this.post.subject,
        text: {
          text: this.post.text.text
        }
        // Add any other relevant parameters here, such as visibility settings or image attachments
      };
      axios.post(shareEndpoint, postData, {
        headers: {
          Authorization: `Bearer ${this.accessToken}`
        }
      }).then(response => {
        console.log('Post published:', response.data);
      }).catch(error => {
        console.error('Failed to publish post:', error.response.data);
      });
    }
  }
}
</script>

<style scoped>

</style>
