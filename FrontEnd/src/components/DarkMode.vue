<template>
<div>
  <q-toggle
    size="xl"
    dark color="teal"
    keep-color
    left-label
    v-model="formData.theme"
    false-value="light mode"
    true-value="dark mode"
    label="theme"
    icon="moon"
  />

</div>

</template>

<script>
import { defineComponent } from "vue";

export default {
  name: "DarkMode",
  data(){
    return{
      formData: {
        theme: false
      }
    }
  }
}
</script>

<style scoped>

</style>
