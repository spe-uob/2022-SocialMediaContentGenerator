<template>
 <div class="q-pa-md">
  <div class="q-gutter-md" style="max-width: 1800px">
    <q-input rounded outlined v-model="message" label="Text" >
      <template v-slot:append>
        <q-icon name="close" @click="message = ''" class="cursor-pointer"/>
      </template>
      <template v-slot:after>
        <q-icon name="send"  color="primary" class="cursor-pointer" :disable="!message"/>
      </template>
      </q-input>
  </div>
 </div>
</template>

<script>
import FaceBookLogin from "components/FaceBookLogin";
import axios from 'axios'
export default {
  name: "FaceBook",
  data() {
    return {
      access_token:FaceBookLogin.data().access_token,
      message: ''
    };
  },
  methods:{
    async postToFacebook() {
      const params = {
        access_token: this.accessToken,
        message: this.message
      };

      try {
        const response = await axios.post('https://graph.facebook.com/v16.0/me/feed', params);
        console.log('Post was successful!');
      } catch (error) {
        console.error(error);
      }
    }
  }

}

</script>


<style scoped>

</style>
