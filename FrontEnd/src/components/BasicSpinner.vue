<template>
  <div class="q-pa-md">
    <div class="q-gutter-md row">
      <q-spinner
        color="primary"
        size="3em"
        :thickness="10"
      />
    </div>
  </div>
</template>

<script>
import {defineComponent} from "vue";
export default defineComponent({
  name: "BasicSpinner"
})
</script>

<style scoped>

</style>
