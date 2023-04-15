import axios from 'axios'
import qs from 'qs'

const client_id = '78sme225fsy5by'
const client_secret = 'J3xg14qRTV87viVq'
const redirect_uri = 'http://localhost:9000'
const scope = 'r_liteprofile r_emailaddress w_member_social'
const state = Math.random().toString(36).substring(7)
const linkedinAuthUrl = `https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=${client_id}&redirect_uri=${encodeURIComponent(redirect_uri)}&state=${state}&scope=${scope}`
//let accessToken = 'AQVgVkduTETUtblERvunIpMxrw2jDeJfFldADa68vEZHjdUOfiRgSKhle6chBxOjclV8gHyYlFCTc-aWLrOV5QfuvMNw8qbFl5FFVMhpHFY8vbMU86nw9Ws4XrYKyh9jPaQ7ptqZ_cOKT5DD3qp4T6wWs5H9Lmnrx22vK--YxrHJ35RzlHJfinUi57zwBfr4S3x_f-7yiHpglEtpWDE9FyFKE2T83AYsl0N2oRCY_vNTgK78-CC31nY3lfhMHejVKTM7ozLmfIvD2Myjtqr9V4fBLRK4BdvKpU_loHxjAEYn-GoFzYxzBJRNr-pw9iImVk6kiWCW15ak-HGerLoJwoBYIsyKXg'
let accessToken = 'AQWXwufriO-kI6UGBhte4ZT9z9DHP4dpKkEmmRZUJkOew5apwGY1t_nuyoONACRYYX8Uh3d2i13zZYFEv7OO99KEbnlrrnoECIig25Q6SQVpELK0B3DB6kbL3NiD2kRD7749qx0MiKw9cjoc0f9d1ctn4nkUuuj9kNxqUBbRPilk_eabV0F7ikEfha4JDpYqMPBC1LBlqKZa2KiblpQ7n0Lw3lCl8y0_LgCWpLaUyrUYVY1QIFZTPMyGhhAUp3lpY-JUiEvDECEOx8Xa7iPMnOYfzmb4eQgpUYKax4isOBbz7JG1BpJFJ-kDwFTQy5oVTuIAyZl2wljQWHbiV3-Sz07xcjARyQ'
let userId = ''

/*async function checkAccessToken() {
  const headers = {
    'Authorization': `Bearer ${accessToken}`,
    'cache-control': 'no-cache',
    'X-Restli-Protocol-Version': '2.0.0'
  }

  try {
    let response = await axios.get('https://api.linkedin.com/v2/me', {headers})
    userId = response.data.id;
    console.log(`Access token is still valid. User ID: ${userId}`);
  } catch (error) {
    console.log(`Access token is invalid or has expired. Error: ${error}`);
  }
}*/

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
  try {
    let response = await axios.get('https://api.linkedin.com/v2/me', {headers})
    userId = response.data.id;
    console.log(`User ID: ${userId}`);
    console.log(`User ID: ${userId}`);
  } catch (error) {
    console.log(`Error getting user ID: ${error}`);
    console.log(`Response: ${error.response}`);
    console.log(`Status: ${error.response.status}`);
    console.log(`Data: ${error.response.data}`);
  }
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
  try {
    let response = await axios.post(`https://api.linkedin.com/v2/ugcPosts`, {
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
            "text": "114514!" // replace with your desired post text
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
    })
    console.log('Post created:', response.data);
  } catch (error) {
    console.log('Error creating post:', error.response.data);
  }
}

async function run() {
  console.log("start")
  //await checkAccessToken()
  await retrieveAccessToken()
  console.log("second")
  await postToLinkedIn()
  console.log("finished")
}

run()
//await postToLinkedIn();

/*export {
  retrieveAccessToken,
  postToLinkedIn
}*/
