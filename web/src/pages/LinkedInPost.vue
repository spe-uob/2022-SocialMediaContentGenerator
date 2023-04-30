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
          <q-btn type="submit" label="Publish post"></q-btn>
        </q-form>
      </q-card-section>
    </q-card>
  </q-page>

  <div class="container">
    <div class="container">
      <h1>Upload Image</h1>
      <div class="upload">
        <input type="file" @change="onFileChange">
<!--        <label for="file">{{ fileName }}</label>-->
      </div>
      <button class="btn" @click="uploadImage">Upload</button>
    </div>
  </div>

  <input type="file" @change="onFileChange">


  <q-btn class="q-ma-sm" color="red" @click="signOut">
    Sign Out
  </q-btn>
</template>

<script>

import axios from 'axios';


const client_id =  '78sme225fsy5by'
const redirect_uri = 'http://localhost:9000'
const scope =  'r_liteprofile r_emailaddress w_member_social'
const state = Math.random().toString(36).substring(7)
const linkedinAuthUrl = `https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=${client_id}&redirect_uri=${encodeURIComponent(redirect_uri)}&state=${state}&scope=${scope}`



export default {
  name: "LinkedInPost",
  data () {
    return {
      url: linkedinAuthUrl,
      inputText: '',
      fileName: 'choose file',
      file: null
    }
  },
  methods: {
    onFileChange(event) {
      this.file = event.target.files[0];
      this.fileName = this.file.name;
    },
    uploadImage() {
      const formData = new FormData()
      formData.append('image', this.file)
      formData.append('message', this.inputText)

      axios.post("http://localhost:8888/api/LinkedInApiPostImage", formData)
        .then(response=>{
          const upUrl = response.data.url
          console.log(upUrl)

        })
        .catch(error =>{
          console.log(error)
        })
    },
    signOut() {
      axios.post("http://localhost:8888/api/v1/linkedinSignOut")
        .then(response=>{
          console.log(response)
        })
        .catch(error =>{
          console.log(error)
        })
    },
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

.container {
  font-family: Arial, Helvetica, sans-serif;
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f2f2f2;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

h1 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.upload {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.inputFile {
  display: none;
}

label {
  padding: 10px;
  background-color: #fff;
  border: 1px solid #333;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 10px;
  color: #333;
  font-weight: bold;
  font-size: 16px;
  transition: all 0.2s ease-in-out;
}

label:hover {
  background-color: #333;
  color: #fff;
}

span {
  font-size: 16px;
  color: #333;
}

.btn {
  background-color: #333;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.2s ease-in-out;
}

.btn:hover {
  background-color: #fff;
  color: #333;
  border: 1px solid #333;
}


</style>
