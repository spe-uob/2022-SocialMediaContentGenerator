<template>
  <router-view />
</template>

<script>
import { useQuasar } from 'quasar';
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'App',
  setup() {
    const $q = useQuasar()
    $q.dark.set(true)
  }
})
</script>
