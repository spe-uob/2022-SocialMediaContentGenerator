<!--<template>
  <div>
    <a :href="'https://twitter.com/' + 'Flgodd'" target="_blank">
      <i class="fab fa-twitter"></i> Follow @{{ screenName }}
    </a>
    <div v-if="tweets">
      <div v-for="tweet in tweets" :key="tweet.id">
        <div>{{ tweet.text }}</div>
      </div>
    </div>
  </div>
</template>-->
<template>

  <div class="q-pa-none">
    <q-toolbar class="bg-grey-2 text-grey-8" style="min-height:50px">
      <q-toolbar-title class="text-subtitle2 text-grey-5">Timeline {{temp}}</q-toolbar-title>
    </q-toolbar>

  </div>

  <a class="twitter-timeline"
      href="https://twitter.com/DavidYa56963667"
     data-aria-polite="rude">
     <!--data-chrome="nofooter"-->
    Tweets by you.
  </a>
</template>

<script>
import AuthComponent from '../components/AuthComponent.vue'
import authComponent from "components/AuthComponent.vue";

const f = "Flgodd";

const d = AuthComponent.data().apiKey;
AuthComponent.methods.twitter()
const nName = AuthComponent.data().displayName;

console.log(AuthComponent.data().displayName);
console.log(AuthComponent.data().secret);
//console.log(AuthComponent.methods.twitter())


console.log("https://twitter.com/" + AuthComponent.data().displayName);
const temp = "https://twitter.com/" + AuthComponent.data().displayName;
export default {
  components: { },
  name: "TimelineView",
  props: ['screenName', temp],
  data() {
    return {
      tweets: null,
      // screenName: temp,
      //displayUser: ''
    };
  },
  setup(){
    return {
      temp,
    }
  }

  /*created() {
    this.getTweets();
  },*/
  /*methods: {
    async getTweets() {
      const response = await fetch(
        `https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=${screenName}`,
        {
          headers: {
            Authorization: `Bearer ${d}`,
          },
        }
      );
      const data = await response.json();
      this.tweets = data;
    },
  },*/
};
</script>

<style scoped>

</style>
