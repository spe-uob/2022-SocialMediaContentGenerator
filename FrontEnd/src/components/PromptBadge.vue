<template>
  <li>
    <q-badge color="Blue">
      {{ tag }}
    </q-badge>
    <button @click="$emit('remove')">Delete</button>
  </li>
</template>

<script>
export default {
  name:"PromptBadge.vue",
  props:['tag'],
  emits: ['delete']
}
</script>

<style scoped>

</style>
