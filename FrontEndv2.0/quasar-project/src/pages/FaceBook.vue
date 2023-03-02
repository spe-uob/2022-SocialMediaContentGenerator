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
  methods: {
    postToFacebook() {
      const access_token='EAAJKxVJZAnoUBANeAl5XZCZCp0BN0PMAkUZABYzodsOXZCKY10Eqy5czitMf0gzp7ouMBcO3ZCCw938pkF3lnVEjSGT42T6LIibuZAauMZBNrx2IS6WTXM2vPll17y04X5uh0bF4iVqQp4qaRE1pm9fg90WrRsE6axycks5lyI2NJ2dDRnWa5qLxCkboTBUrFmfEWKxBlYS8zm4nutQqrjWelD1WVWJTHxMZD'
      axios.post('https://graph.facebook.com/me/feed?message=${message}&access_token=${access_token}'
      )
        .then(response => {
          console.log(response);
        })
        .catch(error => {
          console.log(error);
        });
    },
  },
}

</script>

<style scoped>

</style>
