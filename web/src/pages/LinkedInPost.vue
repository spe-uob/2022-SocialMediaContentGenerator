<template>
  <div>
    <a href="https://www.linkedin.com/oauth/v2/authorization?client_id=78sme225fsy5by&redirect_uri=http://localhost:9000&response_type=code&scope=r_emailaddress r_liteprofile w_member_social" @click="getCode">
      <img src="~assets/quasar-logo-vertical.svg" alt="Log in with LinkedIn" />
    </a>
  </div>
  <q-page>
    <q-card class="q-mb-md">
      <q-card-section>
        <h2 class="q-ma-none">Publish a post on LinkedIn</h2>
      </q-card-section>
      <q-card-section>
        <q-form @submit="submitPost">
          <q-input label="Post subject"></q-input>
          <q-input label="Post text" v-model="inputText" type="textarea"></q-input>
          <q-btn type="submit" label="Publish post xxx"></q-btn>
        </q-form>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>

import axios from 'axios';
//https://www.linkedin.com/oauth/v2/authorization?client_id=78sme225fsy5by&redirect_uri=http://localhost:9000&response_type=code&scope=r_emailaddress r_liteprofile w_member_social


// https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=${client_id}&redirect_uri=${encodeURIComponent(redirect_uri)}&state=${state}&scope=${scope}
// https://www.linkedin.com/oauth/v2/authorization?response_type=code&state=987654321&scope=r_liteprofile%20r_emailaddress&client_id=78sme225fsy5by&redirect_uri=http%3A%2F%2Flocalhost%3A9000

const client_id =  '78sme225fsy5by'
const redirect_uri = 'http://localhost:9000'
const scope =  'r_liteprofile r_emailaddress w_member_social'
const state = Math.random().toString(36).substring(7)
const linkedinAuthUrl = `https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=${client_id}&redirect_uri=${encodeURIComponent(redirect_uri)}&state=${state}&scope=${scope}`
//`https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=78sme225fsy5by&redirect_uri=http%3A%2F%2Flocalhost%3A9000&state=987654321&scope=r_liteprofile_r_emailaddress_w_member_social`


export default {
  name: "LinkedInPost",
  data () {
    return {
      url: linkedinAuthUrl,
      inputText: ''
    }
  },
  methods: {
    getCode(){
      const code = new URL(location.href).searchParams.get('code')
      console.log(code)
      if(code){
        axios.post("http://localhost:8888/api/linkedin/access_token", {code: code})
      }
    },
    submitPost(){
      let message = this.inputText
      console.log("submit pressed")
      if(message){
        axios.post("http://localhost:8888/api/linkedin/post", {message: message})
      }
    }
  },
  mounted() {
    this.getCode();
  }

}
</script>

<style scoped>

</style>
