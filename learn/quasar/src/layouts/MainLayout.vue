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
          Test
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
      <q-item clickable v-ripple>
        <q-item-section avatar>
          <q-icon color="secondary" name="fa-solid fa-minus" />
        </q-item-section>
        <q-item-section>Home</q-item-section>
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
import EssentialLink from 'components/EssentialLink.vue'

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
    EssentialLink
  },

  setup () {
    const leftDrawerOpen = ref(false)

    return {
      essentialLinks: linksList,
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  }
})
</script>
