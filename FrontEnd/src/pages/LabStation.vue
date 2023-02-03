<template>
  <div class="q-pa-md q-gutter-sm">
    <q-img
      :src="url"
      spinner-color="white"
      style="height: 700px; max-width: 750px"
    />
    <q-btn push color="teal" label="Generate Image" @click="refresh" />
  </div>
  <q-form
    v-on:submit.prevent="addNewHashTags"

    @submit="onSubmit"
    @reset="onReset"
    class="q-gutter-md"
  >
    <!-- action="http://localhost:9000/#/LabStation" method="post" // -->
    <label for="new-hashtag">Add a Hashtag</label>
    <q-input
      filled
      v-model="newHashTag"
      id="new-hashtag"
      label="AddHashTag *"
      hint=""
      lazy-rules
      :rules="[ val => val && val.length > 0 || 'Please type something']"
    />
    <button>Add</button>
  </q-form>
  <ul>
    <HashTag
      v-for="(HashTag, index) in HashTags"
      :key="HashTag.id"
      :name="HashTag.name"
      @remove="HashTags.splice(index, 1)"
    ></HashTag>
  </ul>
  <div>
    <q-btn label="Submit" type="submit" color="primary"/>
    <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
  </div>
</template>

<script>
import { ref,defineComponent } from 'vue'
import HashTag from 'components/HashTag.vue';


export default defineComponent({
  name:"LabStation",
  components: {HashTag},
  data(){
    return {
      newHashTag: '',
      HashTags: [],
      nextHashTagId: 1
    }
  },
  methods: {
    addNewHashTags() {
      this.HashTags.push({
        id: this.nextHashTagId++,
        name: this.newHashTag
      })
      this.newHashTag = ''
    },
    onSubmit (evt) {
      console.log('@submit - do something here', evt)
      evt.target.submit()
    }

  },
  setup () {
    const url = ref('https://placeimg.com/500/300/nature')

    return {
      url,
      refresh () {
        url.value = 'https://placeimg.com/500/300/nature?t=' + Math.random()
      }
    }
  }
})
</script>
