<template>
  <q-page class="flex flex-center">
    <div class="col-12">
      <div class="row q-pb-sm">
        <div class="text-h6 vertical-middle q-ma-md">Blog preview:</div>
      </div>
      <div class="row q-pb-sm">
        <iframe :src="blog_url" v-if="blog_url !== ''" style="height: 80vh; width: 80vw" id="iframe"></iframe>
      </div>
    </div>
  </q-page>
</template>

<script>

export default {
  name: "BlogPreview",
  data() {
    return {
      blog_url: '',
      raw_blog_url: '',
      base_url: '',
      url_history: [],
    }
  },
  methods: {
    getUrl(path) {
      return this.base_url + path;
    },
    async load_blog_address() {
      let blog_url = (await (await fetch(this.getUrl('/api/v1/blog_server_url'))).json())['content']
      this.raw_blog_url = blog_url
      this.blog_url = blog_url
    },
  },
  mounted() {
    this.debug = this.$DEBUG;
    this.base_url = this.$BASEURL;
    this.load_blog_address()
  },
  watch: {
    'blog_url': function (newVal, oldVal) {
      this.url_history.push(oldVal)
    }
  }
}
</script>

<style scoped>

</style>
