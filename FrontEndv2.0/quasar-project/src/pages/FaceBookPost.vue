<template>
 <div class="q-pa-md">
  <div class="q-gutter-md" style="max-width: 1800px">
    <q-input rounded outlined v-model="message" label="Text" >
      <template v-slot:append>
        <q-icon name="close" @click="message = ''" class="cursor-pointer"/>
      </template>
      <template v-slot:after>
        <q-icon name="send"  @click="postToFacebook" :color="primary" class="cursor-pointer" :disable="!message"/>
      </template>
      </q-input>
  </div>
 </div>
</template>

<script>
import FBAuthComponent from "components/FBAuthComponent";
import axios from 'axios'
import {defineComponent} from "vue";
const user_token = 'EAAJKxVJZAnoUBAOCAT1gMW6XieimRCjMAEnYS2ZACH0iolQJe6Hbc9X7rWyN15UyGJVIZClKHADXRavPcpDljROcCaef3UihisvTyZA2hbDZCBkpCTjezzB0IuuAcXE834Q6ipa7FQojMBjWdRGK3lThQUHB5yiYFeqgXlf4ZAd6ePni2m7wTnmXJa7KaURQQtHYbOLw7iE4z29MXW1TvG'
const page_token = 'EAAJKxVJZAnoUBAGbp87KcGG7wXX9voeP4diFHtgitKKDhVVWDLCPhfUK3i9dMfweA8ronmukO0pZCeuQXhpWZAnfJznXWYRQK50t0oBQZCtjusSUFSr90ylFBQxUNH62Yld8OrJwrUX3tstVD3AWyep2jTJoNxqp7wxqxucsafMpyTXFnsrvwMZCjIBDL4MOdZAZArscpxuwi0woRokIuuc'
const page_id = '101969492843962'
export default defineComponent({
  name: "FaceBookPost",
  data() {
    return {
      access_token:FBAuthComponent.data().access_token,
      message: ''
    };
  },
  methods:{
    async postToFacebook() {
      const params = {
        access_token: page_token,
        message: this.message
      };

      try {
        const response = await axios.post('https://graph.facebook.com/v16.0/feed', params);
        console.log('Post was successful!');
      } catch (error) {
        console.error(error);
      }
    }
  }

})

</script>


<style scoped>

</style>
