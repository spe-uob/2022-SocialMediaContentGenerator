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
      image:"",
      imageUrl:"https://images.app.goo.gl/Pezq2abNj8EP7SKr8",
      user_token:"",
      page_token:""
    }
  },
  methods: {
    async postToFacebook() {
      console.log("user access token:", this.$route.query.user_token)
      console.log("page access token:", this.$route.query.page_token)
      this.page_token = this.$route.query.page_token
      this.user_token = this.$route.query.user_token
      const image_path = "src/assets/quasar-logo-vertical.svg"
      const caption = this.message
      //formData.append('source', this.image);
      console.log("message sent", this.message)
      console.log("page token", this.page_token)
      fetch('src/assets/spaceNXT.png')
        .then(response => response.blob())
        .then(blob => {

          // Create a FormData object and append the image blob to it
          const formData = new FormData();
          formData.append('source', blob, 'spaceNXT.png');

          // Make the POST request to Facebook Graph API
          axios.post('https://graph.facebook.com/119057271096466/photos', formData, {
            params: {
              access_token: this.page_token,
              caption: this.message
            },
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
            .then(response => {
              console.log(response.data);
            })
            .catch(error => {
              console.log(error);
            });
        })
        .catch(error => {
          console.log(error);
        });





      /*axios.post(`https://graph.facebook.com/${page_id}/photos`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
        .then(response => {
          console.log(response.data);
        })
        .catch(error => {
          console.log(error);
        });*/
      /*const result = await fetch(`https://graph.facebook.com/${page_id}/photos`, {
        method: 'POST',
        body: formData
      }).then(response => response.json())
      console.log(result)*/

     /* axios.post(`https://graph.facebook.com/${page_id}/photos`, {
        //message: this.message,
        url: "https://unsplash.com/photos/tJxu4j4-T4o",
        caption: this.message,
        access_token: this.page_token
      })
        .then(response => {
          console.log('Response:', response);
        })
        .catch(error => {
          console.error('Error:', error);
        });*/
    },
  }
}
</script>

<style scoped>

</style>
