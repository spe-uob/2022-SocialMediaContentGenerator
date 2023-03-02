<template>
 <div class="q-pa-md">
  <div class="q-gutter-md" style="max-width: 1800px">
    <q-input rounded outlined v-model="message" label="Text" >
      <template v-slot:append>
        <q-icon name="close" @click="message = ''" class="cursor-pointer"/>
      </template>
      <template v-slot:after>
        <q-icon name="send" @click="postToFacebook" color="primary" class="cursor-pointer" :disable="!message"/>
      </template>
      </q-input>
  </div>
 </div>
</template>

<script>
import axios from 'axios'
export default {
  name: "FaceBook",


  data() {
    return {
      message: ''
    };
  },
  methods: {}
}

</script>

<style scoped>

</style>
