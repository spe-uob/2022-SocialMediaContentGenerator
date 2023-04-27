<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <q-layout view="hHh Lpr FfF">
    <q-header style="height:100px" class="bg-white" reveal bordered>
      <div class="row items-center justify-around">
        <div class="col"></div>
        <div class="col-2">
          <q-btn flat>
            <img src="~/assets/spaceNXT.png" style="height:5.5rem" @click="hyperlink"/>
          </q-btn>
        </div>
        <div class="col-6">
          <q-btn label="Home" to="/" style="color:#031629" flat class="text-grey-5"/>
          <q-btn label="Stable Diffusion UI" to="/stablediffusionUI" style="color:#031629" flat class="text-grey-5"/>
        </div>
        <div class="col"></div>
        <div class="col">
          <q-btn dense flat size="1rem">
            <q-avatar size="2rem" class="fa-solid fa-user text-grey-5"/>
            <q-menu
              transition-show="scale"
              transition-hide="scale"
              anchor="top right"
              self="top left"
              style="min-width:300px"
            >
              <q-list>
                <q-item>
                  <AuthComponent v-if="!signedIn"/>
                  <q-btn disabled ref="button" class="flex justify-center full-width" color="light-blue" icon="fa-brands fa-twitter" type="submit" rounded @click="twitter" style="min-height:50px; min-width:270px;">
                    <span class="q-pa-xs">
                      Signed in as {{ name }}
                    </span>
                  </q-btn>
                </q-item>
                <q-item>
                  <FBAuthComponent></FBAuthComponent>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
          <q-btn
            dense
            flat
            @click="$q.dark.toggle()"
            class="q-pl-lg"
          >
            <q-avatar size="2rem" :class="!$q.dark.isActive ? 'fa-regular fa-moon text-grey-5' : 'fa-solid fa-moon text-grey-5'"/>
          </q-btn>
        </div>
      </div>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
  </template>

  <script>
  import AuthComponent from "components/AuthComponent.vue";
  import LinkedInLogin from "components/LinkedInLogin.vue";
  import { getAuth } from "firebase/auth";
  import FBAuthComponent from "components/FBAuthComponent.vue";
  import { openURL } from 'quasar';
  const auth = getAuth()

  export default {
    components: {FBAuthComponent, AuthComponent},
    data(){
      return{
        drawerMenu: true,
        rightDrawerMenu: true,
        name: '',
        signedIn: false,
      }
    },
    mounted() {
      this.checkTwitterStatus()
    },
    methods: {
      hyperlink() {
        openURL("https://spacenxtlabs.com")
      },
      async checkTwitterStatus() {
        console.log("checking twitter status")
        const url = `http://127.0.0.1:8888/api/v1/twitterSignInCheck`
        const response = await fetch(url, {
          method: 'GET',
          mode: 'cors',
        })
        // eslint-disable-next-line no-unused-vars
        const data = await response.json()
        if (data['status'] === "signedIn") {
          console.log("signed in", data['name'])
          this.name = data['name']
          this.signedIn = true
        }
        else {
          console.log("not signed in")
          this.name = ''
          this.signedIn = false
          return false
        }
      },
      signOut() {
        auth.signOut().then(async function() {
          const url = `http://127.0.0.1:8888/api/v1/twitterSignOut`
          const response = await fetch(url, {
            method: 'GET',
            mode: 'cors',
          })
          console.log('Signed Out')
          location.reload()
        }, function(error) {
          console.error('Sign Out Error', error);
        });
      },
    }
  }
  </script>

  <style lang="stylus">
  .menu-link
    color #1da1f2
    //background #2f353a
  </style>
