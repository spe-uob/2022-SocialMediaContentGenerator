<template>
  <div>
    <!--<q-toolbar
    :class="$q.dark.isActive ? 'bg-grey-2' : 'bg-white'">
      <div class="col"></div>
      <div>
        <span class="text-grey-5"> Signed in as {{ this.displayName }}</span>
        <q-btn class="q-mx-md text-grey-5" flat to="/signin" v-ripple @click="signOut()">
          <q-icon name="fa-solid fa-sign-out" class="q-mr-xs"/>
          Sign Out
        </q-btn>
      </div>
    </q-toolbar> -->
    <q-input
      rounded
      outlined
      v-model="text"
      class="q-pa-md"
      autogrow
      maxlength="100"
    >
      <template v-slot:append>
        <q-icon name="close" @click="text = ''" class="cursor-pointer"/>
      </template>
      <template v-slot:after>
        <q-icon name="send" @click="addNewTweetPost" color="primary" class="cursor-pointer" :disable="!text"/>
      </template>
    </q-input>
    <!--<q-img :src="image" style="max-width: 40vw"></q-img>-->
    <q-file color="purple-12" @update:model-value="uploadImage($event)" label="Add images">
      <template v-slot:prepend>
        <q-icon name="attach_file"/>
      </template>
    </q-file>
    <div class="row">
      <span class="col"></span>
      <img
        class="col"
        :src="`data:image/png;base64,${this.image}`"/>
      <span class="col"></span>
    </div>
  </div>
  <a class="twitter-timeline"
     href="https://twitter.com/${this.twitterUsername}"
     data-aria-polite="assertive">
    Tweets by @{{this.screenName}}
  </a>

</template>

<script>
import {defineComponent} from "vue";
export default defineComponent({
  name: "PostPage",
  data() {
    return{
      image:""
    }
}
})
</script>

<style scoped>

</style>
