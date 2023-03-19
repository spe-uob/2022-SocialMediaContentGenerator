<template>
  <div>
    <div class="flex flex-center">
      <q-btn class="text-center full-width" color="blue" icon="fa-brands fa-facebook" label="sign in with facebook" type="submit" @click="loginWithFacebook" rounded></q-btn>
    </div>
  </div>
</template>

<script>
import { getAuth, signInWithPopup, FacebookAuthProvider } from 'firebase/auth'
import { defineComponent } from 'vue'
const provider = new FacebookAuthProvider()
export default defineComponent({
  name: 'FaceBook',
  methods: {
    async loginWithFacebook () {
      try {
        const auth = getAuth()
        const result = await signInWithPopup(auth, provider)
        const user = result.user
        const credential = provider.credentialFromResult(result)
        this.$emit('login', user)
        this.$emit('access', credential)
      } catch (error) {
        // Handle error
      }
    }
  }
})

</script>

<style scoped>

</style>
