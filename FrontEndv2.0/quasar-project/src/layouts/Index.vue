<template>
<q-layout view="hHh Lpr FfF">
  <q-header bordered>
    <div class="row no-wrap">
      <q-toolbar shrink class="bg-grey-3" style="max-width:240px">
        <q-btn flat round dense icon="apps" class="text-grey-6" @click="drawerMenu = !drawerMenu">
          <q-avatar square size="28px">
            <img src="'statics/image/vue.png'">
          </q-avatar>
        <q-toolbar-title>
          <span class="text-h6 text-grey-6">Vue.</span><span class="text-orange-5">js</span>
        </q-toolbar-title>
        </q-btn>
      </q-toolbar>
      <q-toolbar class="bg-grey-5">
        <q-toolbar-title>
          <span class="gt-sm text-subtitle2 text-grey-6 vertical-middle">Quasar Framework</span>

        </q-toolbar-title>
      </q-toolbar>
    </div>
  </q-header>
  <q-footer bordered>
    <q-bar class="bg-grey-3 text-grey-6 q-pa-sm">
      <span class="text caption">Vue Quasar Framework</span>
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
    content-class="bg-grey-2 text-grey-6">
    <q-scroll-areac class="fit">
      <q-list dense>
        <q-item>
          <q-item-section class="text-grey-5 text-weight-medium">
            MAIN MENU
          </q-item-section>
          <q-item-section avatar>
            <q-icon name="crop_din" class="text-grey-5"/>
          </q-item-section>
        </q-item>
      </q-list>
      <q-list dense>
        <q-item clickable v-ripple class="text-grey-6" :to="{name:'home'}" active-class="menu-link">
          <q-item-section avatar>
            <q-icon name="crop_din" />
          </q-item-section>
          <q-item-section>Home</q-item-section>
        </q-item>
      </q-list>
    </q-scroll-areac>

  </q-drawer>

</q-layout>
</template>

<script>
export default {
  data(){
    return{
      drawerMenu: true
    }
  },
  name: "Index"
}
</script>

<style lang="stylus">
.menu-link
  color #1da1f2
  background #2f353a


</style>
