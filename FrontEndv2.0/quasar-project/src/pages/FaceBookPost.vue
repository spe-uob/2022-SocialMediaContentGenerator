<template>
  <div class="q-pa-md">
    <div class="q-gutter-md" style="max-width: 1800px">
      <q-input rounded outlined v-model="message" label="Text" >
        <template v-slot:append>
          <q-icon name="close" @click="message = ''" class="cursor-pointer"/>
        </template>
        <template v-slot:after>
          <q-icon name="send"  @click="postToFacebook" :color="primary" class="cursor-pointer" :disable="!message"/>
        </template>
      </q-input>
    </div>
  </div>
</template>

<script>
import axios from "axios";
const page_id = '119057271096466'
export default {
  name: "FaceBookPost",
  data(){
    return{
      message:"",
      picture:"~src/quasar-logo-vertical.svg",
      user_token:"",
      page_token:""
    }
  },
  methods: {
    postToFacebook(){
      console.log("user access token:", this.$route.query.user_token)
      console.log("page access token:", this.$route.query.page_token)
      this.page_token = this.$route.query.page_token
      this.user_token = this.$route.query.user_token
      const formData = new FormData();
      formData.append('message', 'Hello, World!');
      formData.append('source', '~assets/quasar-logo-vertical.svg');
      console.log("message sent", this.message)
      console.log("page token", this.page_token)
      axios.post(`https://graph.facebook.com/${page_id}/feed`, {
        message: this.message,
        access_token: this.page_token,
        picture:this.picture
      })
        .then(response => {
          console.log('Response:', response);
        })
        .catch(error => {
          console.error('Error:', error);
        });
    }
  }
}
</script>

<style scoped>

</style>
