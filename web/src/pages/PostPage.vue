<template>
  <q-img
    :src=this.image
    spinner-color="white"
    style="height: 140px; max-width: 150px"
  />
</template>

<script>
export default {
  name: "PostPage",
  data() {
    return{
      image:""
    }
}
}
</script>

<style scoped>

</style>
