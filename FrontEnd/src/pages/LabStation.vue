<template>
  <div class="q-pa-md q-gutter-sm">
    <q-img
      :src="url"
      spinner-color="white"
      style="height: 700px; max-width: 750px"
    />
    <q-btn push color="teal" label="Generate Image" @click="refresh" />
  </div>
</template>

<script>
import { ref,defineComponent } from 'vue'

export default defineComponent({
  name:"LabStation",
  setup () {
    const url = ref('https://placeimg.com/500/300/nature')

    return {
      url,
      refresh () {
        url.value = 'https://placeimg.com/500/300/nature?t=' + Math.random()
      }
    }
  }
})
</script>
