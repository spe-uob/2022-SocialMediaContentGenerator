<template>
  <q-btn @click="saveImage">Save Image </q-btn>
</template>

<script>
import FileSaver from 'file-saver'
import {defineComponent} from "vue";

export default defineComponent({
  name:'TestPage',
  data () {
    return {
      imageDataURI:''
    }
  },
  created () {
    // Fetch the image data from a URL
    fetch('https://cdn.quasar.dev/img/material.png')
      .then(response => response.blob())
      .then(blob => {
        this.imageDataURI = URL.createObjectURL(blob)
      })
  },
  methods:{
    saveImage () {
      const link = document.createElement('a')
      link.href = this.imageDataURI
      link.target='_blank'
      link.download = 'image.jpeg'
      link.click()
    }
  }

})
</script>

