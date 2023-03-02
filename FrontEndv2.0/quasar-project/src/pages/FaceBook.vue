<template>
 <div class="q-pa-md">
  <div class="q-gutter-md" style="max-width: 300px">
    <q-input rounded outlined v-model="message" label="Rounded outlined" />
  </div>
 </div>
</template>

<script>
import axios from 'axios'
import {ref} from 'vue'
export default {
  name: "FaceBook",


  data() {
    return {
      message: ref(''),
    };
  },
  methods: {
    postToFacebook() {
      axios.post('https://graph.facebook.com/me/feed', {
        message: this.message,
        access_token: 'your-access-token',
      })
        .then(response => {
          console.log(response);
        })
        .catch(error => {
          console.log(error);
        });
    },
  },
}

</script>

<style scoped>

</style>
