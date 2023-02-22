<template>
  <q-layout view="lHh Lpr lFf">
    <q-header bordered>
      <div class="row no-wrap">
        <q-toolbar shrink class="bg-grey-3" style="max-width:240px">
          <q-btn flat round dense icon="apps" class="text-grey-6" @click="drawerMenu = !drawerMenu">
            <q-avatar square size="28px">
              <img src="~assets/spaceNXT.svg" class="responsive" alt = "login-image" >
            </q-avatar>
            <q-toolbar-title>
              <span class="text-h6 text-grey-6">Space</span><span class="text-orange-5">.NXT</span>
            </q-toolbar-title>
          </q-btn>
        </q-toolbar>
        <q-toolbar class="bg-grey-5">
          <q-toolbar-title>
            <span class="gt-sm text-subtitle2 text-h6 text-grey-6 vertical-middle">Social Media Content Generator</span>

          </q-toolbar-title>
          <q-btn
            class="q-mr-xs"
            flat
            round
            @click="$q.dark.toggle()"
            :icon="$q.dark.isActive ? 'nights_stay' : 'wb_sunny'"
          />
        </q-toolbar>
      </div>
    </q-header>
    <q-footer bordered>
      <q-bar class="bg-grey-3 text-h6 text-grey-6 q-pa-sm">
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
      content-class="bg-primary text-white">
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
          <q-item  v-ripple class="text-grey-6" :to="{name:'home'}" active-class="menu-link">
            <q-item-section avatar>
              <q-icon name="crop_din" />
            </q-item-section>
            <q-item-section>Home</q-item-section>
          </q-item>

          <q-item  v-ripple class="text-grey-6" to="/StableDiffusionUI" active-class="menu-link">
            <q-item-section avatar>
              <q-icon name="crop_din" />
            </q-item-section>
            <q-item-section>SD UI</q-item-section>
          </q-item>

          <q-item  v-ripple class="text-grey-6" to="/TwitterView" active-class="menu-link">
            <q-item-section avatar>
              <q-icon name="crop_din" />
            </q-item-section>
            <q-item-section>Twitter Page</q-item-section>
          </q-item>
        </q-list>



      </q-scroll-areac>

    </q-drawer>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'


export default defineComponent({
  name: 'MainLayout',
  data: () => ({
    drawerMenu: true,
    essentialLinks: [
      {
        name: 'Home',
        icon: 'home',
        to: '/'
      },
      {
        name: 'SD UI',
        icon: 'home',
        to: '/StableDiffusionUI'
      },
      {
        name: 'Twitter Page',
        icon: 'home',
        to: '/TwitterView'
      }
    ]
  }),
})
</script>
