<template>
  <q-layout view="lHh LpR lFf">

    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" aria-label="Menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg">
          </q-avatar>
          Social Media Content Generator
        </q-toolbar-title>
        <q-space/>
        <div class="q-gutter-sm row items-center no-wrap">
          v1.0
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer show-if-above v-model="leftDrawerOpen"  bordered class="bg-primary text-white" side="left" elevated>
      <q-scroll-area style="height: calc(100% - 150px); margin-top: 150px">
        <q-list>
          <q-item to="/" active-class="q-item-no-link-highlighting">
            <q-item-section avatar>
              <q-icon name="home" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Home</q-item-label>
            </q-item-section>
          </q-item>

          <q-item to="/LoginPage"  active-class="q-item-no-link-highlighting">
            <q-item-section avatar>
              <q-icon name="person" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Login</q-item-label>
            </q-item-section>
          </q-item>

          <q-item to="/LabStation" active-class="q-item-no-link-highlighting">
            <q-item-section avatar>
              <q-icon name="dashboard" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Lab</q-item-label>
            </q-item-section>
          </q-item>


          <q-item to="/TestPage" active-class="q-item-no-link-highlighting">
            <q-item-section avatar>
              <q-icon name="dashboard" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Test</q-item-label>
            </q-item-section>
          </q-item>

          <q-item to="/StableDiffusionUI" active-class="q-item-no-link-highlighting">
            <q-item-section avatar>
              <q-icon name="dashboard" />
            </q-item-section>
            <q-item-section>
              <q-item-label>SD UI</q-item-label>
            </q-item-section>
          </q-item>

          <q-item to="/StatisticsData" active-class="q-item-no-link-highlighting">
            <q-item-section avatar>
              <q-icon name="insert_chart" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Statistics</q-item-label>
            </q-item-section>
          </q-item>


          <!-- <q-item to="/Login" active-class="" -->

          <q-separator class="bg-grey-7" size="2px" inset></q-separator>

          <q-item to="/AboutUs" active-class="q-item-no-link-highlighting">
            <q-item-section avatar>
              <q-icon name="person" />
            </q-item-section>
            <q-item-section>
              <q-item-label>About Us</q-item-label>
            </q-item-section>
          </q-item>

          <q-item to="/AppInfo" active-class="q-item-no-link-highlighting">
            <q-item-section avatar>
              <q-icon name="info" />
            </q-item-section>
            <q-item-section>
              <q-item-label>App Info</q-item-label>
            </q-item-section>
          </q-item>

          <q-item to="/AppSettings" active-class="q-item-no-link-highlighting">
            <q-item-section avatar>
              <q-icon name="settings" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Settings</q-item-label>
            </q-item-section>
          </q-item>

        </q-list>
      </q-scroll-area>

      <q-img class="absolute-top" src="https://cdn.quasar.dev/img/material.png" style="height: 150px">
        <div class="absolute-bottom bg-transparent">
          <q-avatar size="56px" class="q-mb-sm">
            <img src="~assets/Benjamine_Avatar.png" />
          </q-avatar>
          <q-avatar size="56px" class="q-mb-sm">
            <img src="~assets/David_Avatar.png" />
          </q-avatar>
          <q-avatar size="56px" class="q-mb-sm">
            <img src="~assets/Gene_Avatar.png" />
          </q-avatar>
          <q-avatar size="56px" class="q-mb-sm">
            <img src="~assets/DuskXi_Avatar.jpeg" />
          </q-avatar>
          <div class="text-weight-bold">
            Space NXT Labs
          </div>
          <div class="text-weight-bold">
            University of Bristol
          </div>
          <div>2022 SPE</div>
        </div>
      </q-img>
    </q-drawer>

    <q-page-container class="bg-grey-2">
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'

export default defineComponent({
  name: 'MainLayout',
  components: {
   // EssentialLink,
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
