<template>
  <div>
    <div class="flex flex-center">
      <q-btn class="text-center full-width" color="blue" icon="fa-brands fa-facebook" label="sign in with facebook" type="submit" @click="redirect" rounded></q-btn>
      </div>
  </div>
</template>

import axios from 'axios'

<script>
export default {
  name: "FaceBookLogin",

  data() {
    return {
      message: '',
    };
  },
  methods: {
    redirect() {
      this.$router.push("/FaceBook")
    }
  }
}
</script>

<style scoped>

</style>
