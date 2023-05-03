<template>
  <div>
    <a
      :href="`https://www.linkedin.com/oauth/v2/authorization?client_id=${client_id}&redirect_uri=${redirect_uri}&response_type=code&scope=r_emailaddress r_liteprofile w_member_social`">

      <q-btn class="flex justify-center full-width" color="blue-8" icon="fa-brands fa-linkedin" rounded style="min-height:50px; min-width:270px">
        <span class="q-pl-xs">
          Sign in with LinkedIn
        </span>
      </q-btn>
    </a>
  </div>

</template>

<script>
import axios from 'axios'

const scope = 'r_liteprofile r_emailaddress w_member_social'
export default {
  name: "LinkedinAuth",
  data() {
    return {
      debug: false,
      base_url: '',
      client_id: '',
      redirect_uri: new URL(window.location.href).origin + '/index.html',
      // redirect_uri: window.location.href,
    }
  },
  methods: {
    getUrl(path) {
      return this.base_url + path;
    },
    getCode() {
      const code = new URL(location.href).searchParams.get('code')
      console.log(code)
      if (code) {
        axios.post(this.getUrl("/api/v1/Login"), {platform: 'linkedin', code: code, url: new URL(window.location.href).origin + '/index.html'})
      }
    },
    async get_id() {
      let response = await fetch(this.getUrl("/api/v1/key"))
      let data = await response.json()
      this.client_id = data['linkedin_auth']['application_key']
    },
  },
  mounted() {
    console.log("debug type:", this.$DEBUG)
    this.debug = this.$DEBUG;
    this.base_url = this.$BASEURL;
    this.get_id();
    this.getCode();
  },
}
</script>

<style scoped>

</style>
