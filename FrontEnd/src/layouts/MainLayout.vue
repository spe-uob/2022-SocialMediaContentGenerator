<template>
  <q-layout view="hhh lpR lFf" container style="height: 900px" class="shadow-2 rounded-borders">

    <q-header elevated class="bg-indigo-7 text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          <q-avatar>
            <img src="~/assets/drone-svgrepo-com.svg">
          </q-avatar>
           Social Media Content Generator Ver 0.0
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" side="left"
      show-if-above
      :width="200"
      :breakpoint="500"
      overlay bordered
      class="bg-light-blue-2">
      <q-scroll-area class="fit">
                <q-list padding class="menu-list">
                  <q-item clickable v-ripple>
                    <q-item-section avatar>
                      <q-icon name="send" />
                    </q-item-section>

                    <q-item-section>
                      Item 1
                    </q-item-section>
                  </q-item>

                  <q-item active clickable v-ripple>
                    <q-item-section avatar>
                      <q-icon name="send" />
                    </q-item-section>

                    <q-item-section>
                      Item 2
                    </q-item-section>
                  </q-item>

                  <q-item clickable v-ripple>
                    <q-item-section avatar>
                      <q-icon name="send" />
                    </q-item-section>

                    <q-item-section>
                      Item 3
                    </q-item-section>
                  </q-item>

                  <q-item clickable v-ripple>
                    <q-item-section avatar>
                      <q-icon name="send" />
                    </q-item-section>

                    <q-item-section>
                      Item 4
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-scroll-area>
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
    const leftDrawerOpen = ref(false)

    return {
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  }
}
</script>
