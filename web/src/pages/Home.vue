<template>
  <q-tabs
    v-model="tab"
    indicator-color="light-blue-3"
    class="text-grey-5"
  >
    <span class="text text-grey-5 col q-ml-md" >Social Media Content Generator</span>
      <q-tab name="twitter" icon="fa-brands fa-twitter" @click="twitter"/>
      <q-tab name="facebook" icon="fa-brands fa-facebook" />
      <q-tab name="linkedin" icon="fa-brands fa-linkedin" />
    <div class="col"></div>



  </q-tabs>
  <q-separator></q-separator>
  <q-tab-panels v-model="tab" animated>
    <q-tab-panel name="twitter">
      <a class="twitter-timeline" href="https://twitter.com/spacenxtlabs?ref_src=twsrc%5Etfw">Tweets by spacenxtlabs</a>
    </q-tab-panel>
    <q-tab-panel name="facebook">
      Facebook timeline
    </q-tab-panel>
    <q-tab-panel name="linkedin">
      LinkedIn timeline
    </q-tab-panel>
  </q-tab-panels>

</template>

<script>
export default {
  name: "HomePage",
  data() {
    return  {
      tab: 'twitter'
    }
  },
  mounted() {
    const script = document.createElement('script');
    script.src = 'https://platform.twitter.com/widgets.js';
    script.async = true;
    script.charset = 'utf-8';
    document.head.appendChild(script);
  },
  methods: {
    twitter() {
      location.reload()
    }
  }
}
</script>

<style scoped>

</style>
