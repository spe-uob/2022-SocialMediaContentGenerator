<template>
  <div>
    <h1>LinkedIn API Authorization</h1>
    <div v-if="!authorized">
      <p>Click the button to authorize this app to access your LinkedIn profile:</p>
      <q-btn label="Authorize" @click="authorize" />
    </div>
    <div v-else>
      <p>You are authorized to access the LinkedIn API.</p>
      <p>Your access token is: {{ access_token }}</p>
    </div>
  </div>
  <div>
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
        <q-icon name="send" @click="postToLinkedIn" color="primary" class="cursor-pointer" :disable="!text"/>
      </template>
    </q-input>
    <q-img :src="image" style="max-width: 40vw"></q-img>
    <q-file color="purple-12" @update:model-value="uploadImage($event)" label="Add images">
      <template v-slot:prepend>
        <q-icon name="attach_file"/>
      </template>
    </q-file>
  </div>
</template>

<script>
import axios from 'axios'
import qs from 'qs'

const client_id = '78sme225fsy5by'
const client_secret = 'J3xg14qRTV87viVq'
const redirect_uri = 'http://localhost:9000'
const scope = 'r_liteprofile r_emailaddress'
export default {
  name: "linkedInA",
  data() {
    return {
      authorized: false,
      access_token: '',
    }
  },
  methods: {
    authorize() {
      const state = Math.random().toString(36).substring(7)
      const linkedinAuthUrl = `https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=${client_id}&redirect_uri=${encodeURIComponent(redirect_uri)}&state=${state}&scope=${scope}`
      window.location.href = linkedinAuthUrl
    },
    retrieveAccessToken() {
      const code = new URLSearchParams(window.location.search).get('code')
      if (code) {
        const data = {
          grant_type: 'authorization_code',
          code,
          redirect_uri,
          client_id,
          client_secret,
        }

        const headers = {
          'Content-Type': 'application/x-www-form-urlencoded',
        }

        axios.post('https://www.linkedin.com/oauth/v2/accessToken', qs.stringify(data), { headers })
          .then(response => {
            this.authorized = true
            this.access_token = response.data.access_token
            this.userId = response.data.id // set the userId property to the user's LinkedIn ID
            //this.firstName = response.data.localizedFirstName
            //this.email = response.data.emailAddress
          })
          .catch(error => console.error(error))
      }
    },

    postToLinkedIn() {
      const message = 'Hello, world!'; // the message to post
      const visibility = {
        'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC' // the visibility of the post
      };
      //`https://api.linkedin.com/v2/ugcPosts?oauth2_access_token=".${this.access_token}`,
      //https://api.linkedin.com/v2/ugcPosts
      axios.post(`https://api.linkedin.com/v2/ugcPosts`, {
        author: `urn:li:person:${this.userId}`,
        lifecycleState: 'PUBLISHED',
        specificContent: {
          'com.linkedin.ugc.ShareContent': {
            shareCommentary: {
              text: message
            },
            shareMediaCategory: 'NONE'
          }
        },
        visibility: visibility
      }, {
        headers: {
          'Authorization': `Bearer ${this.access_token}`,
          'Content-Type': 'application/json'
        }
      })
        .then(response => {
          console.log('Post was successful!');
        })
        .catch(error => {
          console.log('Error posting to LinkedIn:', error);
          console.log(this.access_token)
        });
    }
  },
  mounted() {
    this.retrieveAccessToken()
  },
}
</script>

<style scoped>

</style>
