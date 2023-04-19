<template>
<q-layout view="hHh Lpr FfF">
  <q-header bordered>
    <div class="row no-wrap">
      <q-toolbar shrink
                 :class="$q.dark.isActive ? 'bg-grey-2' : 'bg-white'" style="max-width:240px">
        <q-btn flat icon="apps" class="text-grey-6" @click="drawerMenu = !drawerMenu">
        <q-toolbar-title>
          <span class="text-h6 text-grey-5">Space</span><span class="text-orange-5">.NXT</span>
        </q-toolbar-title>
        </q-btn>
      </q-toolbar>
      <q-toolbar :class="$q.dark.isActive ? 'bg-grey-2' : 'bg-white'">
        <q-toolbar-title>
          <span class="gt-sm text-h4 text-grey-5 q-pa-md">Social Media Content Generator</span>
        </q-toolbar-title>
        <q-btn dense flat class="q-pa-md text-grey-5"
        @click="rightDrawerMenu = !rightDrawerMenu">
          <q-avatar class="fa-solid fa-user"/>
        </q-btn>
        <q-btn
          class="bg-grey-5 q-mx-xs"
          flat
          round
          @click="$q.dark.toggle()"
          :icon="$q.dark.isActive ? 'nights_stay' : 'wb_sunny'"
        />
      </q-toolbar>
    </div>
  </q-header>
  <q-footer bordered>
    <q-bar :class="$q.dark.isActive ? 'bg-grey-3' : 'bg-white'" class="text-h6 text-grey-5 q-pa-sm">
      <span class="text caption">Social Media Content Generator: Benjamin, Gene, David, Stephen</span>
    </q-bar>
  </q-footer>
  <q-page-container>
    <router-view />
  </q-page-container>

  <q-drawer
    v-model="drawerMenu"
    :width="240"
    no-swipe-open
    bordered
    :class="$q.dark.isActive ? 'bg-grey-1' : 'bg-white'"
    content-class="bg-primary text-white">
    <q-scroll-areac class="fit">
      <q-list dense>
        <q-item>
          <q-item-section class="text-grey-5 text-weight-medium">
            MAIN MENU
          </q-item-section>
        </q-item>
      </q-list>
      <q-list dense>
        <q-item clickable v-ripple class="text-grey-5" to="/" active-class="menu-link">
          <q-item-section avatar>
            <q-icon name="fa-solid fa-house" />
          </q-item-section>
          <q-item-section>Home</q-item-section>
        </q-item>

        <q-item clickable @click="signOut()" v-ripple class="text-grey-5" to="/signin" active-class="menu-link">
          <q-item-section avatar>
            <q-icon name="fa-solid fa-user" />
          </q-item-section>
          <q-item-section>Sign In</q-item-section>
        </q-item>

        <q-item clickable v-ripple class="text-grey-5" to="/stablediffusionUI" active-class="menu-link">
          <q-item-section avatar>
            <q-icon name="fa-solid fa-sliders" />
          </q-item-section>
          <q-item-section>SD UI</q-item-section>
        </q-item>

        <q-item clickable v-ripple class="text-grey-5" to="/LinkedInPost" active-class="menu-link">
          <q-item-section avatar>
            <q-icon name="fa-brands fa-linkedin" />
          </q-item-section>
          <q-item-section>LinkedIn Post</q-item-section>
        </q-item>

        <q-item clickable v-ripple class="text-grey-5" to="/TextGenerator" active-class="menu-link">
          <q-item-section avatar>
            <q-icon name="article" />
          </q-item-section>
          <q-item-section>Text Generator</q-item-section>
        </q-item>
      </q-list>
    </q-scroll-areac>
  </q-drawer>


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
            <AuthComponent v-if="!checkTwitterStatus"/>
            <q-btn v-else class="flex justify-center full-width" color="light-blue" icon="fa-brands fa-twitter" rounded>
              <span class="q-pa-sm">
                Signed in as ...
              </span>
            </q-btn>
          </q-item-section>
        </q-item>
      </q-list>
    </q-scroll-areac>
  </q-drawer>

</q-layout>
</template>

<script>
import AuthComponent from "components/AuthComponent.vue"
import LinkedInLogin from "components/LinkedInLogin.vue";
import FBAuthComponent from "components/FBAuthComponent.vue";
export default {
  components: {FBAuthComponent, AuthComponent, LinkedInLogin },
  data(){
    return{
      drawerMenu: true,
      rightDrawerMenu: true,
    }
  },
  name: "Index",
  methods: {
    async checkTwitterStatus() {
      const url = `http://127.0.0.1:8888/api/v1/twitterSignInCheck`
      const response = await fetch(url, {
        method: 'GET',
        mode: 'cors',
      })
      // eslint-disable-next-line no-unused-vars
      const data = await response.json()
      if (data['status'] == "signedIn") return true
      else return false
    },
    signOut() {
      auth.signOut().then(function() {
        console.log('Signed Out')
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
