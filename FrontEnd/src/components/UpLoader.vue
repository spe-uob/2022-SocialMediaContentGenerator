<template>
  <div class="q-pa-md">
    <div class="q-gutter-md row items-start">
      <q-uploader
        style="max-width: 300px"
        url="http://localhost:4444/upload"
        label="Restricted to images"
        max-file-size="4096"
        accept=".jpg, image/*"
        @rejected="onRejected"
      />
    </div>
  </div>
</template>

<script>
import {defineComponent} from "vue";
export default defineComponent({
name: "UpLoader",
})
</script>

<style scoped>

</style>
