<template>
  <q-layout view="hHh LpR fff">

    <q-header elevated class="bg-accent text-white" height-hint="98">
      <q-toolbar>
        <q-toolbar-title>
          <q-avatar>
            <img src="~assets/drone-svgrepo-com.svg">
          </q-avatar>
          Social Media Content Generator
        </q-toolbar-title>

        <q-btn dense flat round icon="menu" @click="toggleRightDrawer" />
      </q-toolbar>

      <q-tabs align="left">
        <q-route-tab to="/page1" label="Page 1" />
        <q-route-tab to="/page2" label="Page 2" />
        <q-route-tab to="/page3" label="Page 3" />
        <q-route-tab to="/page1" label="Page 4" />
        <q-route-tab to="/page2" label="Page 5" />
        <q-route-tab to="/page3" label="Page 6" />
      </q-tabs>
    </q-header>

    <q-drawer show-if-above v-model="rightDrawerOpen" side="right" bordered>
      <!-- drawer content -->
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>


<script>
import { ref } from 'vue'

export default {
  setup () {
    const rightDrawerOpen = ref(false)

    return {
      rightDrawerOpen,
      toggleRightDrawer () {
        rightDrawerOpen.value = !rightDrawerOpen.value
      }
    }
  }
}
</script>
