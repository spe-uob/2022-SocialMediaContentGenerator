<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <q-layout view="hHh lpR lFf">
    <q-header style="height:100px" :class="$q.dark.isActive ? 'bg-grey-10' : 'bg-white'" reveal bordered>
      <div class="row items-center justify-evenly">
        <div class="col-1">
          <q-btn v-if="$q.screen.lt.md" @click="drawer = !drawer" flat dense class="q-pl-lg">
            <q-avatar size="2rem" class="fa-solid fa-bars text-grey-5"></q-avatar>
          </q-btn>
        </div>
        <div class="col">
          <q-btn flat>
            <img src="~/assets/spaceNXT.png" style="height:5.5rem" @click="hyperlink"/>
          </q-btn>
        </div>
        <div class="col-5" v-if="$q.screen.gt.sm">
          <q-btn to="/" flat @mouseover="select = 1" @mouseleave="select = 0">
            <span :class="select === 1 ? 'text-light-blue-3' : 'text-grey-5'"> Home </span>
          </q-btn>
          <q-btn to="/stablediffusionUI" flat @mouseover="select = 2" @mouseleave="select = 0">
            <span :class="select === 2 ? 'text-light-blue-3' : 'text-grey-5'"> Stable Diffusion UI </span>
          </q-btn>
          <q-btn to="/GeneratedImage" flat @mouseover="select = 3" @mouseleave="select = 0">
            <span :class="select === 3 ? 'text-light-blue-3' : 'text-grey-5'"> Generated Images </span>
          </q-btn>
          <q-btn to="/TextGenerator" flat @mouseover="select = 4" @mouseleave="select = 0">
            <span :class="select === 4 ? 'text-light-blue-3' : 'text-grey-5'"> Text Generator </span>
          </q-btn>
          <q-btn to="/post" flat @mouseover="select = 5" @mouseleave="select = 0">
            <span :class="select === 5 ? 'text-light-blue-3' : 'text-grey-5'"> Post </span>
          </q-btn>
          <q-btn to="/BlogPreview" flat @mouseover="select = 6" @mouseleave="select = 0">
            <span :class="select === 6 ? 'text-light-blue-3' : 'text-grey-5'"> Blog Preview </span>
          </q-btn>
        </div>
        <div class="col-2 q-pr-xl" v-if="$q.screen.gt.sm">
          <div class="row justify-evenly">
          </div>
        </div>
        <div class="col-6" v-if="$q.screen.lt.md"></div>
        <div class="col auto">
          <q-btn dense flat size="1rem">
            <q-avatar size="2rem" :class="select == -1 ? 'fa-solid fa-user text-light-blue-3' : 'fa-solid fa-user text-grey-5'" @mouseover="select = -1" @mouseleave="select = 0"/>
            <q-menu
              transition-show="scale"
              transition-hide="scale"
              anchor="top right"
              self="bottom left"
              style="min-width:300px; min-height: 210px;"
            >
              <q-list>
                <q-item>
                  <TwitterAuth></TwitterAuth>
                </q-item>
                <q-item>
                  <FacebookAuth></FacebookAuth>
                </q-item>
                <q-item>
                  <LinkedinAuth></LinkedinAuth>
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
            <q-avatar size="2rem" :class="select == -2 ? 'text-light-blue-3' : 'text-grey-5'" @mouseover="select = -2" @mouseleave="select = 0"
                      :icon="$q.dark.isActive ? 'fa solid fa-moon' : 'fa-regular fa-moon'"/>
          </q-btn>
        </div>
      </div>
    </q-header>

    <q-drawer
      v-model="drawer"
      bordered
    >
      <q-scroll-area class="fit">
        <q-list>
          <q-item>
            <q-btn to="/" flat @mouseover="select = 1" @mouseleave="select = 0">
              <span :class="select == 1 ? 'text-light-blue-3' : 'text-grey-5'"> Home </span>
            </q-btn>
          </q-item>
          <q-item>
            <q-btn to="/stablediffusionUI" flat @mouseover="select = 2" @mouseleave="select = 0">
              <span :class="select == 2 ? 'text-light-blue-3' : 'text-grey-5'"> Stable Diffusion UI </span>
            </q-btn>
          </q-item>
          <q-item>
            <q-btn to="/GeneratedImage" flat @mouseover="select = 3" @mouseleave="select = 0">
              <span :class="select === 3 ? 'text-light-blue-3' : 'text-grey-5'"> Generated Image </span>
            </q-btn>
          </q-item>
          <q-item>
            <q-btn to="/TextGenerator" flat @mouseover="select = 4" @mouseleave="select = 0">
              <span :class="select === 4 ? 'text-light-blue-3' : 'text-grey-5'"> Text Generator </span>
            </q-btn>
          </q-item>
          <q-item>
            <q-btn to="/post" flat @mouseover="select = 3" @mouseleave="select = 0">
              <span :class="select == 5 ? 'text-light-blue-3' : 'text-grey-5'"> Post </span>
            </q-btn>
          </q-item>
          <q-item>
            <q-btn to="/BlogPreview" flat @mouseover="select = 6" @mouseleave="select = 0">
              <span :class="select === 6 ? 'text-light-blue-3' : 'text-grey-5'"> Blog Preview </span>
            </q-btn>
          </q-item>
        </q-list>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <router-view/>
    </q-page-container>

  </q-layout>
</template>

<script>
import TwitterAuth from "components/TwitterAuth.vue";
import FacebookAuth from "components/FacebookAuth.vue";
import LinkedinAuth from "components/LinkedinAuth.vue";
import {getAuth} from "firebase/auth";
import axios from 'axios'

import {openURL} from 'quasar';

const auth = getAuth()


export default {
  components: {TwitterAuth, FacebookAuth, LinkedinAuth},
  data() {
    return {
      drawer: false,
      name: '',
      signedIn: false,
      select: 0,
      LCode: " "
    }
  },
  mounted() {
    console.log("debug type:", this.$DEBUG)
    this.debug = this.$DEBUG;
    this.base_url = this.$BASEURL;
    this.checkTwitterStatus()
    this.getCode()
  },
  methods: {
    hyperlink() {
      openURL("https://spacenxtlabs.com")
    },
    async checkTwitterStatus() {
      console.log("checking twitter status")
      const url = `/api/v1/twitterSignInCheck`
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
      } else {
        console.log("not signed in")
        this.name = ''
        this.signedIn = false
        return false
      }
    },
    signOut() {
      auth.signOut().then(async function () {
        const url = `/api/v1/twitterSignOut`
        const response = await fetch(url, {
          method: 'GET',
          mode: 'cors',
        })
        console.log('Signed Out')
        location.reload()
      }, function (error) {
        console.error('Sign Out Error', error);
      });
    },
    getUrl(path) {
      return this.base_url + path;
    },
    getCode() {
      if (this.LCode == " ") {
        const code = new URL(location.href).searchParams.get('code')
        this.LCode = code
        console.log(code)
        if (code) {
          axios.post(this.getUrl("/api/v1/Login"), {platform:'linkedin', code: code, url: new URL(window.location.href).origin + '/index.html'})
        }
      }
    }
  }
}
</script>

<!--<style lang="stylus">-->
<!--.menu-link color #1da1f2-->

<!--//background #2f353a-->
<!--</style>-->
