//EzoH0w73hC3naY84U6NBHZHyz
//qjFQ5WPxqJD7C0JZtMiORkzbhYAXjNNfX0WyMdx5GWz1IiZxFw

//OVpMRGw2bVhLY1ZqWURvQnN4bEw6MTpjaQ
//5aUjY10-VyHPzeC0vRJP9MpgOXhyQXkXAAecHwWEe8QojiegGj

<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          round color="secondary"
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
          dense
        />
        <q-toolbar-title>
          <span class="float-left text-h4">Test</span>
        </q-toolbar-title>

        <div>Quasar v{{ $q.version }}</div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
    <q-list bordered>
      <q-icon
        class="q-pa-lg"
        name="fa-brands fa-twitter"
        color="primary"
        size="lg"/>
      <q-item clickable v-ripple to="/">
        <q-item-section avatar>
          <q-icon color="secondary" name="fa-solid fa-minus" />
        </q-item-section>
        <q-item-section class="text-h6">Index</q-item-section>
      </q-item>
      <q-item clickable v-ripple to="/home">
        <q-item-section avatar>
          <q-icon color="secondary" name="fa-solid fa-minus" />
        </q-item-section>
        <q-item-section class="text-h6">Home</q-item-section>
      </q-item>
    </q-list>
    </q-drawer>
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'

const linksList = [
  {
    title: 'Docs',
    caption: 'quasar.dev',
    icon: 'school',
    link: 'https://quasar.dev'
  },
]

export default defineComponent({
  name: 'MainLayout',

  components: {
  },

  setup () {
    const leftDrawerOpen = ref(false)

    return {
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  }
})
</script>
