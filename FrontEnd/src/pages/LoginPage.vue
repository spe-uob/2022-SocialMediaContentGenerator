<template>
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
                </div>
              </div>
            </q-form>
          </q-card-section>
        </q-card>

      </div>
    </div>
  </q-page>

</template>

<script>
export default {
  name: "LoginPage",
  data() {
    return{
      login:{
        username: '',
        password: ''
      }
    }
  },
  methods: {
    submitForm(){
      if(! this.login.username || ! this.login.password){
        console.log('error')
      }else{
        console.log('login')
      }

    }
  },
  components: {

  }
}
</script>



<style scoped>
.wave{
  position: fixed;
  height: 100%;
  left: 0;
  bottom: 0;
  z-index: -1;

}

</style>
