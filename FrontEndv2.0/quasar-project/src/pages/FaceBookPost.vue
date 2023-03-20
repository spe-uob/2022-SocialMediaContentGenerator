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
import FBAuthComponent from "components/FBAuthComponent";
import axios from "axios";
const user_token = FBAuthComponent.data().user_token
const page_token = FBAuthComponent.data().page_token
console.log("hi")
console.log(user_token)
console.log(page_token)
const page_id = '101969492843962'
export default {
  name: "FaceBookPost",
  data(){
    return{
      message:"",
      image:""
    }
  },
  methods: {
    postToFacebook(){
      console.log("hi")
      console.log(user_token)
      console.log(page_token)
      const formData = new FormData();
      formData.append('message', 'Hello, World!');
      formData.append('source', '~assets/quasar-logo-vertical.svg');

      axios.post(`https://graph.facebook.com/${page_id}/photos?access_token=${page_token}`, formData)
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
