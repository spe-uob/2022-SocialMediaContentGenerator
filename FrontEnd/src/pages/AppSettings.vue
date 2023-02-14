<template>
  <div>

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

      //watch(() => $q.dark.isActive, val => {
        //console.log(val ? 'On dark mode' : 'On light mode')
      //})
    },


}
</script>


<style scoped>

</style>
