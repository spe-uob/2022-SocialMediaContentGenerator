<template>
  <q-page class="q-pa-sm">
    <div class="row q-col-gutter-lg">
      <div class="col-lg-4 col-md-4 col-xs-12 col-sm-12" v-for="data in card_data" :key="data.id">
        text
      </div>
    </div>
  </q-page>
</template>

<script>
import {defineComponent, defineAsyncComponent} from 'vue'
const card_data = [
  {
    id:1,
    name: 'Benjamine_Aram',
    avatar: '~assets/Benjamine_Avatar.png',
    contact: 'test@gmail.com',
    disc:'text',
  },
  {
    id:2,
    name: 'David_Yan',
    avatar: '~assets/David_Avatar.png',
    contact: 'test@gmail.com',
    disc:'text',
  },

];
export default defineComponent({
  name: "AboutUs",
  components: {
  },
  setup() {
    return {
      card_data
    }
  }
})
</script>

<style scoped>
</style>
