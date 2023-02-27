<template>
  <div>
    <vue-linkedin-login
      :client-id="clientId"
      :redirect-uri="redirectUri"
      :scope="scope"
      @success="onSuccess"
      @error="onError"
    >
      Login with LinkedIn
    </vue-linkedin-login>
  </div>
</template>

<script>
//import VueLinkedinLogin from 'vue-linkedin-login'

export default {
  name: 'AuthComponentLinkedIn',
  components: {
    VueLinkedinLogin
  },
  data () {
    return {
      clientId: 'your-client-id',
      redirectUri: 'http://localhost:8080/linkedin/callback',
      scope: 'r_liteprofile'
    }
  },
  methods: {
    onSuccess (data) {
      // handle successful login
      console.log(data)
    },
    onError (error) {
      // handle login error
      console.log(error)
    }
  }
}
</script>


<style scoped>

</style>
