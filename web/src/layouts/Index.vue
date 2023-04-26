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
          <q-btn dense flat size="1rem"
          @click="rightDrawerMenu = !rightDrawerMenu">
            <q-avatar class="fa-solid fa-user text-grey-5"/>
          </q-btn>
          <q-btn
            class="q-mx-lg text-grey-5"
            size="1rem"
            flat
            round
            @click="$q.dark.toggle()"
            :icon="!$q.dark.isActive ? 'nights_stay' : 'wb_sunny'"
          />
        </div>
      </div>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-drawer
      side="right"
      v-model="rightDrawerMenu"
      :width="240"
      no-swipe-open
      bordered
      :class="$q.dark.isActive ? 'bg-grey-1' : 'bg-white'"
      content-class="bg-primary text-white">
      <q-scroll-areac class="fit">
        <q-list>
          <q-item>
            <q-item-section>
              <div class="q-pa-sm"></div>
              <AuthComponent v-if="!signedIn"/>
              <div v-else class="q-col row items-center justify-center q-mt-md" >
                  <q-btn class="q-ma-sm" color="light-blue" icon="fa-brands fa-twitter" rounded no-caps disable>
                    <span>
                      Signed in as {{ name }}
                    </span>
                  </q-btn>
                  <q-btn class="q-ma-sm" color="red" @click="this.signOut()">
                    Sign Out
                  </q-btn>
              </div>
              <FBAuthComponent/>
            </q-item-section>
          </q-item>
        </q-list>
      </q-scroll-areac>
    </q-drawer>

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
