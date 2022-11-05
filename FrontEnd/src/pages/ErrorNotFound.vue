<template>
  <div class="fullscreen bg-warning text-white text-center q-pa-md flex flex-center">
    <div>
      <div style="font-size: 30vh">
        404 Not Found
      </div>

      <div class="text-h2" style="opacity:.4">
        Sorry, here's nothing
      </div>

      <q-btn
        class="q-mt-xl"
        color="white"
        text-color="blue"
        unelevated
        to="/"
        label="Go Home"
        no-caps
      />
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ErrorNotFound'
})
</script>
