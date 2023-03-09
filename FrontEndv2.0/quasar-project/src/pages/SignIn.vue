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
              <div>
                <div class="q-pa-sm"></div>
                <AuthComponent />
                <div class="q-pa-sm"></div>
                <q-btn class="text-center full-width" color="red" icon="fa-brands fa-instagram" label="sign in with instagram" type="submit" rounded></q-btn>
                <div class="q-pa-sm"></div>
                <FaceBookLogin />
                </div>

            </q-form>
          </q-card-section>

        </q-card>

      </div>
    </div>
  </q-page>
</template>

<script>
import AuthComponent from "components/AuthComponent.vue"
import firebase from 'boot/firebase.js'
import FaceBookLogin from "components/FaceBookLogin.vue";
export default {
  name: "SignIn",
  components: { AuthComponent,FaceBookLogin },
  data() {
    return{
      login:{
        username: '',
        password: ''
      }
    }
  },
  methods: {
  }
}
</script>

<style scoped>

</style>
