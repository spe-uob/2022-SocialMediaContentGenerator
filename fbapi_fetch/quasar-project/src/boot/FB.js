import firebase from 'boot/firebase'
import { FacebookAuthProvider } from 'firebase/auth'
export default {
  methods: {
    async loginWithFacebook () {
      const provider = new firebase.auth.FacebookAuthProvider()
      try {
        const result = await firebase.auth().signInWithPopup(provider)
        const user = result.user
        const displayName = user.displayName
        const credential = FacebookAuthProvider.credentialFromResult(result)
        const accessToken = credential.accessToken
        return [displayName, accessToken]
        // User is signed in
      } catch (error) {
        // Handle error
      }
    }
  }
}
