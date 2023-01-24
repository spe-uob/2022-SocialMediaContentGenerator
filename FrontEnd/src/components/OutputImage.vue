<template>
  <div class="q-pa-md q-gutter-sm">
    <q-btn push color="teal" label="Generate Image" @click="refresh" />
    <q-img
      :src="url"
      spinner-color="white"
      style="height: 140px; max-width: 150px"
    />
  </div>
</template>

<script>
import { ref,defineComponent } from 'vue'

export default defineComponent({
  name:"OutputImage",
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

<style scoped>

</style>
