import { ref } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'
<template>
  <q-layout view="LHh lpR fFf" container style="height: 900px" class="shadow-2 rounded-borders">

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
      :width="300"
      :breakpoint="600"
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
                    <div class="q-pa-md">
                      <q-ajax-bar
                        hijack-filter="myFilterFn"
                        ref="bar"
                        position="bottom"
                        color="accent"
                        size="10px"
                        skip-hijack
                      />

                      <q-btn color="primary" label="Start" @click="trigger" />
                    </div>
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

                  <q-item clickable v-ripple>
                    <q-item-section avatar>
                      <q-icon name="send" />
                    </q-item-section>

                    <q-item-section>
                      Item 5
                    </q-item-section>
                  </q-item>

                  <q-item clickable v-ripple>
                    <q-item-section avatar>
                      <q-icon name="send" />
                    </q-item-section>
                      <q-ajax-bar :hijack-filter="myFilterFn" />
                    <q-item-section>
                      Item 6
                    </q-item-section>
                  </q-item>

                  <q-item clickable v-ripple>
                    <q-item-section avatar>
                      <q-icon name="send" />
                    </q-item-section>

                    <q-item-section>
                      Item 7
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
  name: "get-request",
  data() {
    return {
      totalVuePackages: null
    };
  },
  created() {
    fetch("127.1.1.0.8030")
      .then(response => response.json())
      .then(data => (this.totalVuePackages = data.total));
  },
  setup () {
    const leftDrawerOpen = ref(false)
    return {
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      },
    }
  }
}
</script>
