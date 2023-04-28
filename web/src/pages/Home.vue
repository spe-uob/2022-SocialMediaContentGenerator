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
      <div id="twitter-timeline-feed" class="embedded-twitter-feed">
        <v-container fluid>
        <a class="twitter-timeline" data-theme='dark' href="https://twitter.com/SpacenxtLabs?ref_src=twsrc%5Etfw">
          Loading...
        </a>
        </v-container>
      </div>
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
  methods: {
    twitter() {
      location.reload()
    }
  }
}
window.twttr = (function (d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0],
    t = window.twttr || {};
  if (d.getElementById(id)) return t;
  js = d.createElement(s);
  js.id = id;
  js.src = "https://platform.twitter.com/widgets.js";
  fjs.parentNode.insertBefore(js, fjs);

  t._e = [];
  t.ready = function (f) {
    t._e.push(f);
  };

  return t;
}(document, "script", "twitter-wjs"));

</script>

<style scoped>

</style>
