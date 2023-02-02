<template>
  <div>
    <q-toggle
      size="xl"
      dark color="black"
      keep-color
      left-label
      v-model="formData.theme"
      false-value="light mode"
      true-value="dark mode"
      label="theme"
      icon="light"
    />

  </div>
</template>

<script>
import { Dark } from 'quasar'
import { useQuasar } from 'quasar'
import { watch } from 'vue'
import DarkMode from "components/DarkMode.vue";
export default {
  name: "AppSettings",
    setup () {
      const $q = useQuasar()

      watch(() => $q.dark.isActive, val => {
        console.log(val ? 'On dark mode' : 'On light mode')
      })
    },
  data(){
    return{
      formData: {
        theme: false
      }
    }
  }

}
Dark.set(true)
console.log(Dark.isActive)
</script>


<style scoped>

</style>
