<template>
  <div>
    <div class="flex flex-center">
      <q-btn class="text-center full-width" color="blue" icon="fa-brands fa-facebook" label="sign in with facebook" type="submit" @click="FaceBookLogin" rounded></q-btn>
      </div>
  </div>
</template>

import axios from 'axios'

<script>
export default {
  name: "FaceBookLogin",

  data() {
    return {
      message: '',
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
