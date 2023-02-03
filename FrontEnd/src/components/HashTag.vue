<template>
  <li>
    {{ name }}
    <button @click="$emit('remove')">Delete</button>
  </li>
</template>

<script>
export default {
  name: "HashTag.vue",
  props:['name'],
  emits:['delete']
}
</script>

<style scoped>

</style>
