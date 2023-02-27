<template>
  <div class="q-pa-none">
    <q-toolbar class="bg-grey-2 text-grey-8" style="min-height:50px">
      <q-toolbar-title class="text-subtitle2 text-grey-5">HOME</q-toolbar-title>
    </q-toolbar>
  </div>
  <div class="col-0 col-md-6 flex justify-center content-center">
    <img src="~assets/spaceNXT.png" class="responsive" alt = "login-image" >
  </div>
  <div class="embedded-twitter-feed">
    <a class="twitter-timeline" data-width="1200" data-theme="dark" href="https://twitter.com/SpacenxtLabs?ref_src=twsrc%5Etfw">
      Tweets by SpacenxtLabs
    </a>



  </div>
  <!--<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>-->

</template>

<script>
export default {
  name: "Home",
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
