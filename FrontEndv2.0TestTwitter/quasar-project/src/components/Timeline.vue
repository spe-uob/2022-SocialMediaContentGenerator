<template>
  <Tweet
    tweet-id="1370027087818461184"
    cards="visible"
    conversation="all"
    lang="en"
    theme="light"
    align="left"
    :width="400"
    :dnt="false"
    @tweet-load-error="onTweetLoadError"
    @tweet-load-success="onTweetLoadSuccess"
  >
    <template v-slot:loading>
      <span>Loading...</span>
    </template>

    <template v-slot:error>
      <span>Sorry, that tweet doesn’t exist!</span>
    </template>
  </Tweet>
</template>

<script>
import { defineComponent } from 'vue'
import Tweet from 'vue-tweet'

export default defineComponent({
  components: {
    Tweet
  },
  setup() {
    function onTweetLoadSuccess(embedNode) {
      console.log(embedNode)
    }

    function onTweetLoadError() {
      console.log("Ops... an error has occurred")
    }

    return { onTweetLoadSuccess, onTweetLoadError }
  }
})
</script>
