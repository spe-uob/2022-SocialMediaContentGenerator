<template>
  <!--<div class="q-pa-none">
    <q-toolbar class="bg-grey-2 text-grey-8" style="min-height:50px">
      <q-toolbar-title class="text-subtitle2 text-grey-5">Twitter Page</q-toolbar-title>
    </q-toolbar>
  </div>-->
  <q-page class="q-pa-sm">
    <!--<img src="~assets/undraw_flying_drone_u3r2.svg" class="wave" >-->
    <div class="row q-col-gutter-lg" style="height: 90vh">
      <div class="col-0 col-md-6 flex justify-center content-center">
        <img src="~assets/undraw_flying_drone_u3r2.svg" class="responsive" alt = "login-image" >
      </div>
      <div v-bind:class="{'justify-center': $q.screen.md || $q.screen.sm || $q.screen.xs}" class="col-12 col-md-6 flex content-center">
        <q-card v-bind:style="$q.screen.lt.sm ? {'width': '80%'} : {'width': '50%'} ">
          <q-card-section>
            <q-avatar size="103px" class="absolute-center shadow-10">
              <img src="~assets/undraw_male_avatar_g98d.svg" alt="avatar">
            </q-avatar>
          </q-card-section>
          <q-card-section>
            <div class="q-pt-lg">
              <div class="col text-h6 ellipsis flex justify-center"/>
              <h2 class="text-h2 text-uppercase q-my-none text-weight-regular">Login</h2>
            </div>
          </q-card-section>
          <q-card-section>
            <q-form class="q-gutter-md" @submit.prevent="submitForm">
              <q-input label="Username" v-model="login.username">

              </q-input>
              <q-input label="Password" type="password" v-model="login.password">

              </q-input>
              <div>
                <q-btn class="full-width" color="primary" label="login" type="submit" rounded></q-btn>
                <div class="text-center q-mt-sm q-gutter-lg">
                  <router-link class="text-blue" to="/">Forgotten password?</router-link>
                  <router-link class="text-blue" to="/">sign up</router-link>
<!--                  <q-btn class="text-center full-width" color="light-blue" label="sign in with twitter" type="submit" rounded></q-btn>-->
<!--                  <div>
                    <button>
                      <img src="~assets/MicrosoftTeams-image.png" width="240">
                    </button>
                  </div>-->
                </div>
                <div class="q-pa-sm"></div>
                <AuthComponent />
                <div class="q-pa-sm"></div>
                <q-btn class="text-center full-width" color="red" icon="fa-brands fa-instagram" label="sign in with instagram" type="submit" rounded></q-btn>
                <div class="q-pa-sm"></div>
                <q-btn class="text-center full-width" color="blue" icon="fa-brands fa-facebook" label="sign in with facebook" type="submit" rounded></q-btn>
                <div class="q-pa-sm"></div>
                <!--<q-btn class="text-center full-width" color="blue" icon="fa-brands fa-linkedin" label="sign in with linkedIn" type="submit" rounded></q-btn>-->
                <div>
                  <!-- Render the LinkedIn login button component -->
                  <linked-in-login-button></linked-in-login-button>
                <!--https://www.linkedin.com/oauth/v2/authorization?response_type=code&state=987654321&scope=r_liteprofile%20r_emailaddress&client_id=78sme225fsy5by-->
                <!--/auth/linkedin-->
                </div>
                <a href="https://www.linkedin.com/oauth/v2/authorization?response_type=code&state=987654321&scope=r_liteprofile%20r_emailaddress&client_id=78sme225fsy5by&redirect_uri=http%3A%2F%2Flocalhost%3A9000">
                  <img src="/path/to/linkedin-icon.png" alt="Log in with LinkedIn" />
                </a>
                </div>

              <q-page class="q-pa-md">
                <div>
                  <button v-on:click="$auth.login('linkedin')">Login with LinkedIn</button>
                </div>
              </q-page>



            </q-form>
          </q-card-section>

        </q-card>

      </div>
    </div>
  </q-page>
</template>

<script>
import AuthComponent from "components/AuthComponent.vue"
import LinkedInLoginButton from 'components/LinkedInLoginButton.vue';
//import VueLinkedinLogin from 'vue-linkedin-login'

import firebase from 'boot/firebase.js'
/*var request = require('request');

var access_token =

function callAPI(accessToken, done){

  request.get({url:"https://api.lindedin.com/v2/me", headers:{"Authorization": "Bearer" + accessToken }}, function (err, res, responseBody){
    if(err){
      console.log(err);
      done(err, null);
    }else{
      done(null, JSON.parse(responseBody));
    }
  });
}*/
export default {
  name: "TwitterView",
  components: { AuthComponent, LinkedInLoginButton},
 /* data() {
    return{
      login:{
        username: '',
        password: ''
      }
    }
  },
  methods: {
    onAuthSuccess({provider, res}) {
      // Handle the successful login response
      console.log('LinkedIn login successful', res);
    },
    onAuthError({provider, err}) {
      // Handle the login error
      console.log('LinkedIn login error', err);
    },


    submitForm() {
      if (!this.login.username || !this.login.password) {
        console.log('error')
      } else {
        console.log('login')
      }
    }
  }*/

}
</script>

<style scoped>

</style>
