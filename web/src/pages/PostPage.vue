<template>
  <q-page>
    <div class="column q-pt-md">
      <div class="col flex justify-center">
        <div class="row" style="width: 90%;  ">
          <div class="col-8 q-pa-sm">
            <div class="text-h6 q-mb-sm">Poster</div>
            <q-input class="q-mb-sm" v-if="blog_mode" v-model="title" label="Title"></q-input>
            <q-input class="q-mb-sm" filled type="textarea" v-model="post_content" label="Post content" ref="input_box"/>
            <div class="text-h6" style="background-color: #00acc1">
              <q-menu anchor="bottom left" :no-focus="true" self="top left" ref="input_menu" @show="event_menu_show" @before-hide="menu_hide($event)">
                <q-item ref="input_menu_anchor"></q-item>
                <q-item clickable v-for="(image, index) in filtered_images" :key="index" @click="post_content = complete_string(post_content,`<${image}>`)">
                  <q-item-section thumbnail>
                    <img :src="getUrl(`/api/v1/cached_image?path=${image}`)" alt="">
                  </q-item-section>
                  <q-item-section>{{ image }}</q-item-section>
                </q-item>
              </q-menu>
            </div>
            <div class="row q-pa-md">
              <q-intersection v-for="(image_path, index) in selected_images" :key="index" once transition="scale"
                              :style="`width: ${image_info_list[image_path].width}px; height: ${image_info_list[image_path].height}px;`">
                <q-card flat bordered class="q-ma-sm">
                  <img :src="getUrl(`/api/v1/cached_image?path=${image_path}`)">
                  <q-card-section>
                    <div class="text-h6">Image {{ image_path.replace(/^.*\//, "") }}</div>
                    <div class="text-subtitle2"> Width: {{ image_info_list[image_path].raw_width }}, Height: {{ image_info_list[image_path].raw_height }}</div>
                  </q-card-section>
                </q-card>
              </q-intersection>
            </div>
            <div class=" q-gutter-sm">
              <q-btn label="Post" color="primary" class="q-pr-md" @click="post"/>
              <q-btn label="Save to blog" color="primary" class="q-pr-md" @click="blog"/>
              <q-toggle v-model="blog_mode">Enable blog mode</q-toggle>
            </div>

          </div>
          <div class="col-4 q-pa-sm">
            <div class="text-h6 q-mb-sm">Information Board</div>
            <q-card class="q-mb-md">
              <q-card-section>
                <q-title> Select Accounts</q-title>
              </q-card-section>
              <q-card-section>
                <q-option-group
                  v-model="selected_accounts"
                  :options="account_options"
                  type="checkbox"
                  colour="primary">
                  <template v-slot:label="opt">
                    <q-item>
                      <div class="row items-center">
                        <q-item-section>
                          <q-avatar size="2rem" :class="opt.avatar"/>
                          <span class="text-teal">{{ opt.label }}</span>
                        </q-item-section>
                        <q-item-section side>
                          <q-btn icon="delete" @click="deleteOptions(opt.name, opt.platform)"/>
                        </q-item-section>
                      </div>
                    </q-item>
                  </template>
                </q-option-group>
              </q-card-section>
            </q-card>
            <q-card class="q-mb-md">
              <q-card-section>
                <div class="">
                  <q-title class="vertical-middle q-ma-md">Current Blogs</q-title>
                  <q-btn label="goto blog page" color="secondary" @click="goto_blog" :disable="blog_url==='' || blog_url ===null || blog_url===undefined"/>
                </div>
                <q-item clickable v-for="(blog_name, index) in blog_list" :key="index" @click="load_blog(blog_name)">
                  <div class="flex flex-center">{{ index + 1 }}.{{ blog_name }}</div>
                  <q-tooltip>click to edit</q-tooltip>
                </q-item>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import {defineComponent, ref} from "vue";
import Convert from 'ansi-to-html';


export default defineComponent({
  name: "PostPage",
  data() {
    return {
      selected_accounts: [],
      logged_accounts: [],
      post_content: '',
      base_url: "",
      title: "",
      blog_url: "",
      blog_mode: false,
      blog_list: [],
      images: [],
      max_size: 250,
      bottom_size: 86,
      menu_visible: false,
      image_info_list: {},
      filtered_images: [],
      selected_images: [],
      account_options: [],
    };
  },
  methods: {
    getUrl(path) {
      return this.base_url + path;
    },
    deleteOptions(name, platform) {
      const response = fetch(this.getUrl("/api/v1/Delete"), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          platform: platform,
          name: name
        }),
        mode: 'cors',
      })
      this.account_options = this.account_options.filter(
        (option) => option.name !== name
      );
    },
    async load_image_list() {
      let response = await fetch(this.getUrl("/api/v1/image_list"));
      this.images = await response.json();
      let tasks = []
      for (let i = 0; i < this.images.length; i++) {
        tasks.push((async (index) => {
          let image_path = this.images[index];
          let response = await fetch(this.getUrl(`/api/v1/image_info?path=${image_path}`));
          let size = await response.json();
          let scale = Math.min(this.max_size / size.width, (this.max_size + this.bottom_size) / size.height);
          this.image_info_list[image_path] = {
            "width": size.width * scale,
            "height": (size.height * scale) + this.bottom_size,
            "raw_width": size.width,
            "raw_height": size.height,
          }
        })(i))
      }
      await Promise.all(tasks)
    },
    extraction_picture() {
      // get all image from text between < and > to array
      let result = [];
      let text = this.post_content;
      let start = 0;
      while (true) {
        let index = text.indexOf('<', start);
        if (index < 0)
          break;
        let end = text.indexOf('>', index);
        if (end < 0)
          break;
        result.push(text.substring(index + 1, end));
        start = end + 1;
      }
      this.selected_images = result;
    },
    complete_string(content, target) {
      this.$refs.input_menu.hide();
      let textarea = this.$refs.input_box.$el.querySelector("textarea");
      let cursorPosition = textarea.selectionStart;
      let workspace = content.substring(0, cursorPosition);
      workspace = workspace.replace(/<[^<]*$/, target)
      let suffix = content.substring(cursorPosition);
      return workspace + suffix;
    },
    event_input(value) {
      let textarea = this.$refs.input_box.$el.querySelector("textarea");
      let cursorPosition = textarea.selectionStart;
      if (value[cursorPosition - 1] !== '<')
        value = value.substring(0, cursorPosition);
      let filtered = this.filter_option_images(value);
      if (filtered.length > 0 || value.replaceAll(/<.*>/g, '').indexOf('<') >= 0) {
        this.filtered_images = filtered;
        if (!this.menu_visible)
          this.$refs.input_menu.show();
        else
          this.event_menu_show()
        this.menu_visible = true;
      } else {
        this.$refs.input_menu.hide();
      }
      this.extraction_picture();
    },
    filter_option_images(text) {
      let result = [];
      let target = /<.*$/.exec(text.replaceAll(/<.*>/g, ''));
      if (target && target.length > 0)
        target = target[0].substring(1);
      else
        return []
      for (let i = 0; i < this.images.length; i++) {
        let image_path = this.images[i];
        if (image_path.indexOf(target) >= 0) {// && !this.selected_images.includes(image_path)
          result.push(image_path);
        }
      }
      return result;
    },
    menu_hide(event) {
      this.menu_visible = false;
    },
    event_menu_show() {
      let textarea = this.$refs.input_box.$el.querySelector("textarea");
      let cursorPosition = textarea.selectionStart;
      let cursorCoordinates = this.getCaretCoordinates(textarea, cursorPosition);
      let X = textarea.getBoundingClientRect().left + document.documentElement.scrollLeft;
      let Y = textarea.getBoundingClientRect().top + document.documentElement.scrollTop;
      let menu = this.$refs.input_menu_anchor.$el.parentNode;
      menu.style.position = "absolute";
      menu.style.top = (cursorCoordinates.top + Y + 20) + "px";
      menu.style.left = (cursorCoordinates.left + X + 20) + "px";
      // this.$refs.input_box.focus()
    },
    getCaretCoordinates(element, position) {
      // 初始化
      var div = document.createElement("div");
      div.id = "calculationDiv";
      div.style.position = "absolute";
      div.style.visibility = "hidden";
      div.style.whiteSpace = "pre-wrap";
      div.style.wordWrap = "break-word";
      document.body.appendChild(div);

      // 获取文本
      var textContent = this.post_content.substr(0, position);

      // 获取计算div的样式
      var style = window.getComputedStyle(element);
      var fontSize = style.getPropertyValue("font-size");
      var fontFamily = style.getPropertyValue("font-family");

      // 设置计算div的样式
      div.style.fontSize = fontSize;
      div.style.fontFamily = fontFamily;
      div.textContent = textContent;

      // 计算光标位置
      var span = document.createElement("span");
      span.textContent = this.post_content.substr(position) || ".";
      div.appendChild(document.createTextNode("."));
      div.appendChild(span);

      var coordinates = {
        top: span.offsetTop + parseInt(fontSize),
        left: span.offsetLeft
      };

      // 删除计算div
      document.body.removeChild(div);

      return coordinates;
    },
    goto_blog() {
      window.open(this.blog_url)
    },
    async load_logged_account() {
      function get_avatar(platform) {
        if (platform === "twitter")
          return 'fa-brands fa-twitter text-light-blue'
        if (platform === "facebook")
          return 'fa-brands fa-facebook text-blue'
        if (platform === "linkedin")
          return 'fa-brands fa-linkedin text-blue-2'
      }

      this.logged_accounts = await (await fetch(this.getUrl('/api/v1/account_status'))).json()
      for (let i = 0; i < this.logged_accounts.length; i++) {
        this.account_options.push({
          value: this.logged_accounts[i],
          label: "username: " + this.logged_accounts[i].name,
          name: this.logged_accounts[i].name,
          avatar: get_avatar(this.logged_accounts[i].platform),
          platform: this.logged_accounts[i].platform
        })
      }
      console.log(this.logged_accounts)
    },
    async load_blog_list() {
      this.blog_list = (await (await fetch(this.getUrl('/api/v1/blog_list'))).json())['content']
    },
    async load_blog_address() {
      this.blog_url = (await (await fetch(this.getUrl('/api/v1/blog_server_url'))).json())['content']
    },
    async load_blog(blog_name) {
      let title = blog_name.replace(/\.md$/, '')
      let response = await fetch(this.getUrl(`/api/v1/load_blog?filename=${blog_name}`), {method: 'GET', mode: 'cors'})
      let result = await response.json()
      this.title = title
      this.post_content = result.content;
      this.blog_mode = true;
    },
    async blog() {
      if (this.title === '' || this.title === undefined || this.title === null) {
        this.$q.notify({message: 'Title is empty', color: 'warning', position: 'top',})
        return;
      }
      let response = await fetch(this.getUrl('/api/v1/save_to_blog'), {
        method: 'POST', mode: 'cors', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({"content": this.post_content, "title": this.title,}),
      })
      let result = await response.json()
      let output = result.output;
      output = output.replaceAll('\n', '<br />')
      const convert = new Convert();
      output = convert.toHtml(output)
      this.$q.notify({message: `build blog complete: <br/ >${output}`, html: true, position: 'top',})
    },
    async post() {
      this.$q.loading.show();
      let request_body = {
        text: this.post_content.replaceAll(/<.*>/g, ''),
        images: this.selected_images,
        accounts: this.selected_accounts,
      }
      console.log(request_body)
      let result = await fetch(this.getUrl('/api/v1/post'), {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(request_body),
      })
      this.$q.loading.hide();
    }
  },
  mounted() {
    console.log("debug type:", this.$DEBUG)
    this.debug = this.$DEBUG;
    this.base_url = this.$BASEURL;
    this.load_image_list()
    this.load_logged_account()
    this.load_blog_list()
    this.load_blog_address()
  },
  watch: {
    post_content: function (val) {
      this.event_input(val);
    },
  },
});
</script>

<style scoped>
.login_card {
  padding: 20px;
  width: 400px;
  height: 400px;
}
</style>
