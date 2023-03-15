import axios from 'axios'
import qs from 'qs'

const client_id = '78sme225fsy5by'
const client_secret = 'J3xg14qRTV87viVq'
const redirect_uri = 'http://localhost:9000'
const scope = 'r_liteprofile r_emailaddress w_member_social'
const state = Math.random().toString(36).substring(7)
const linkedinAuthUrl = `https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=${client_id}&redirect_uri=${encodeURIComponent(redirect_uri)}&state=${state}&scope=${scope}`
let accessToken = 'AQVgVkduTETUtblERvunIpMxrw2jDeJfFldADa68vEZHjdUOfiRgSKhle6chBxOjclV8gHyYlFCTc-aWLrOV5QfuvMNw8qbFl5FFVMhpHFY8vbMU86nw9Ws4XrYKyh9jPaQ7ptqZ_cOKT5DD3qp4T6wWs5H9Lmnrx22vK--YxrHJ35RzlHJfinUi57zwBfr4S3x_f-7yiHpglEtpWDE9FyFKE2T83AYsl0N2oRCY_vNTgK78-CC31nY3lfhMHejVKTM7ozLmfIvD2Myjtqr9V4fBLRK4BdvKpU_loHxjAEYn-GoFzYxzBJRNr-pw9iImVk6kiWCW15ak-HGerLoJwoBYIsyKXg'
let userId = ''
    async function retrieveAccessToken() {
     /* const code = new URLSearchParams(linkedinAuthUrl).get('code')
      if (code) {
        const data = {
          grant_type: 'authorization_code',
          code,
          redirect_uri,
          client_id,
          client_secret,
        }*/

        const headers = {
          //'Content-Type': 'application/x-www-form-urlencoded',
          'Authorization': `Bearer ${accessToken}`,
          'cache-control': 'no-cache',
          'X-Restli-Protocol-Version': '2.0.0'
        }
        //https://www.linkedin.com/oauth/v2/accessToken
        /*axios.post('https://www.linkedin.com/oauth/v2/me', qs.stringify(data), { headers })
          .then(response => {
            this.authorized = true
            //accessToken = response.data.access_token
            userId = response.data.id // set the userId property to the user's LinkedIn ID
            //this.firstName = response.data.localizedFirstName
            //this.email = response.data.emailAddress
            console.log("herere")
            console.log(userId)
          })
          .catch(error => console.error(error))
      }*/
        axios.get('https://api.linkedin.com/v2/me', {headers})
          .then(response => {
            userId = response.data.id;
            console.log(`User ID: ${userId}`);
            console.log(`User ID: ${userId}`);
          })
          .catch(error => {
            console.log(`Error getting user ID: ${error}`);
            console.log(`Response: ${error.response}`);
            console.log(`Status: ${error.response.status}`);
            console.log(`Data: ${error.response.data}`);
          });
      //}
    }

const userID = userId; // replace with the user's LinkedIn ID
if (!userID) {
  console.error('Error: User ID is not defined or is incorrect.');
}

    async function postToLinkedIn() {
      const message = 'Hello, world!'; // the message to post
      const visibility = {
        'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC' // the visibility of the post
      };
      //`https://api.linkedin.com/v2/ugcPosts?oauth2_access_token=".${this.access_token}`,
      //https://api.linkedin.com/v2/ugcPosts
      // https://api.linkedin.com/v2/posts
      axios.post(`https://api.linkedin.com/v2/ugcPosts`, {
       // author: `urn:li:person:${userId}`,

        /*lifecycleState: 'PUBLISHED',
        specificContent: {
          'com.linkedin.ugc.ShareContent': {
            shareCommentary: {
              text: message
            },
            shareMediaCategory: 'NONE'
          }
        },*/
        "author": `urn:li:person:${userId}`, // replace userId with the user's LinkedIn ID
        "lifecycleState": "PUBLISHED",
        "specificContent": {
          "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
              "text": "Hello, world!" // replace with your desired post text
            },
            "shareMediaCategory": "NONE"
          }
        },
        visibility: visibility
      }, {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
          'X-Restli-Protocol-Version': '2.0.0'
        }
      }).then(response => {
        console.log('Post created:', response.data);
      })
        .catch(error => {
          console.log('Error creating post:', error.response.data);
        });
  }

  await retrieveAccessToken().then( await postToLinkedIn);
  //await postToLinkedIn();
