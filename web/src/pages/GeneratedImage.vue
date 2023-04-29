<template>
  <div class="row q-pa-md">
    <q-intersection v-for="(image_path, index) in image_path_list" :key="index" once transition="scale"
                    :style="`width: ${image_info_list[index].width}px; height: ${image_info_list[index].height}px;`">
      <q-card flat bordered class="q-ma-sm">
        <img :src="getUrl(`/api/v1/cached_image?path=${image_path}`)">
        <q-card-section>
          <div class="text-h6">Image {{ image_path.replace(/^.*\//, "") }}</div>
          <div class="text-subtitle2"> Width: {{ image_info_list[index].raw_width }}, Height: {{ image_info_list[index].raw_height }}</div>
        </q-card-section>
      </q-card>
    </q-intersection>
  </div>
</template>

<script>
import {defineComponent} from "vue";

export default defineComponent({
  name: "GeneratedImage",
  data() {
    return {
      item_width: 512,
      item_height: 512,
      debug: false,
      image_path_list: [],
      image_info_list: [],
      max_size: 500,
      bottom_size: 86,
    };
  },
  methods: {
    getUrl(path) {
      return this.debug ? "http://localhost:8888" + path : path;
    },
    async load_image_list() {
      let response = await fetch(this.getUrl("/api/v1/image_list"));
      this.image_path_list = await response.json();
      for (let i = 0; i < this.image_path_list.length; i++)
        this.image_info_list.push({"width": this.max_size, "height": this.max_size + this.bottom_size});
      let tasks = []
      for (let i = 0; i < this.image_path_list.length; i++) {
        tasks.push((async (index) => {
          let image_path = this.image_path_list[index];
          let response = await fetch(this.getUrl(`/api/v1/image_info?path=${image_path}`));
          let size = await response.json();
          let scale = Math.min(this.max_size / size.width, (this.max_size + this.bottom_size) / size.height);
          this.image_info_list[index] = {
            "width": size.width * scale,
            "height": (size.height * scale) + this.bottom_size,
            "raw_width": size.width,
            "raw_height": size.height,
          }
        })(i))
      }
      await Promise.all(tasks)
    }
  },
  mounted() {
    console.log("debug type:", this.$DEBUG)
    this.debug = this.$DEBUG;
    this.load_image_list()
  }
});
</script>

<style lang="sass" scoped>
.example-item
  height: 512px
  width: 512px
</style>
