<template >

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
            <q-icon name="close" @click="text = ''" class="cursor-pointer" />
      </template>
      <template v-slot:after>
            <q-icon name="send" @click="addNewTweet" color="primary" class="cursor-pointer" :disable="!text" />
      </template>
    </q-input>
  </div>
  <div>
    <!--<q-page class="flex q-pa-md">
      Welcome Home
    <q-space />
    <div>
      <q-btn
        class="flex flex-center q-px-lg q-py-sm q-mb-md"
        size="md"
        label="Logout"
        @click="logout"
        color="primary"
      />
    </div>
    </q-page>-->
    <q-list bordered padding separator>
    <q-item v-for="tweet in tweets" :key="tweet.date">
        <q-item-section>
          <q-item-label overline>NEW TWEET</q-item-label>
          <q-item-label caption>{{ tweet.content }}</q-item-label>
        </q-item-section>

        <q-item-section side top>
          {{  tweet.date }}
        </q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import AuthComponent from '../components/AuthComponent.vue'

// const TwitterApi = require('twitter-api-v2').default()

// import TwitterApi from 'twitter-api-v2';

/*var T = new Twit({
        consumer_key: AuthComponent.data().apiKey,
        consumer_secret: AuthComponent.data().apiSecret,
        access_token: AuthComponent.data().token,
        access_token_secret: AuthComponent.data().secret
})*/

/*var T = new Twit({
        appKey: AuthComponent.data().apiKey,
        appSecret: AuthComponent.data().apiSecret,
        accessToken: AuthComponent.data().token,
        accessSecret: AuthComponent.data().secret
}) */

export default defineComponent({
  name: 'HomePage',
  data() {
    return {
      text: '',
      tweets: [
        {
          content: 'Secondary line text. Lorem ipsum dolor sit amet, consectetur adipiscit elit. Secondary line text. Lorem ipsum dolor sit amet, consectetur adipiscit elit.',
          date: "1675016437899"
        },
        {
          content: 'Secondary line text. Lorem ipsum dolor sit amet, consectetur adipiscit elit.',
          date: "1675018774223"
        }
      ]
    }
  },
  methods: {
    relativeDate(value) {
      return formatDistance(value, new Date())
    },
    async addNewTweet() {
      console.log(AuthComponent.data())
      let tweet = this.text
      const url = `http://localhost:5000/tweet?status=${encodeURIComponent(tweet)}&consumer_key=${encodeURIComponent(AuthComponent.data().apiKey)}&consumer_secret=${encodeURIComponent(AuthComponent.data().apiSecret)}&access_token=${encodeURIComponent(AuthComponent.data().token)}&access_token_secret=${encodeURIComponent(AuthComponent.data().secret)}`
      const response = await fetch(url)
      const data = await response.json()
      console.log(data)

      let newTweet = {
        content: this.text,
        date: Date.now()
      }
      this.tweets.unshift(newTweet)
      this.text = ''
    },
    logout() {
      console.log('logged out')
    },
  }
})
</script>



