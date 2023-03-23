<template>
  <div class="col-0 col-md-6 flex justify-center content-center">
    <q-btn flat>
      <img src="~assets/spaceNXT.png" class="responsive" alt = "login-image" @click="hyperlink"/>
    </q-btn>
  </div>
  <div id="twitter-timeline-feed" class="embedded-twitter-feed">
    <v-container fluid>
    <a class="twitter-timeline" data-theme='dark' href="https://twitter.com/SpacenxtLabs?ref_src=twsrc%5Etfw">
      Tweets by SpacenxtLabs. If timeline fails to load, please refresh the page.
    </a>
    </v-container>
  </div>
  <!--<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>-->

</template>

<script>
import { openURL } from 'quasar'
export default {
  name: "Home",
  methods: {
    hyperlink () {
      openURL("https://spacenxtlabs.com")
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
