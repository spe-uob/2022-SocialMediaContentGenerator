
//const axios = require('axios');
import axios from 'axios'

// Set up the LinkedIn API endpoint and access token
const endpoint = 'https://api.linkedin.com/v2/me';
const accessToken = 'AQWXwufriO-kI6UGBhte4ZT9z9DHP4dpKkEmmRZUJkOew5apwGY1t_nuyoONACRYYX8Uh3d2i13zZYFEv7OO99KEbnlrrnoECIig25Q6SQVpELK0B3DB6kbL3NiD2kRD7749qx0MiKw9cjoc0f9d1ctn4nkUuuj9kNxqUBbRPilk_eabV0F7ikEfha4JDpYqMPBC1LBlqKZa2KiblpQ7n0Lw3lCl8y0_LgCWpLaUyrUYVY1QIFZTPMyGhhAUp3lpY-JUiEvDECEOx8Xa7iPMnOYfzmb4eQgpUYKax4isOBbz7JG1BpJFJ-kDwFTQy5oVTuIAyZl2wljQWHbiV3-Sz07xcjARyQ';
let UID = ' ';
export async function retrieveAccessToken() {
// Set up the headers for the API request
  const headers = {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
    'X-Restli-Protocol-Version': '2.0.0'
  };

// Make the API request using Axios
  await axios.get(endpoint, {headers})
    .then(response => {
      const userId = response.data.id;
      UID = userId;
      console.log(`User ID: ${userId}`);
    })
    .catch(error => {
      console.log(`Error getting user ID: ${error}`);
      console.log(`Response: ${error.response}`);
      //console.log(`Status: ${error.response.status}`);
      //console.log(`Data: ${error.response.data}`);
    });
}

export async function postToLinkedIn(){
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
      "author": `urn:li:person:${UID}`, // replace userId with the user's LinkedIn ID
      "lifecycleState": "PUBLISHED",
      "specificContent": {
        "com.linkedin.ugc.ShareContent": {
          "shareCommentary": {
            "text": "114514!5" // replace with your desired post text
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

export async function run(){
  console.log("start");
  await retrieveAccessToken();
  console.log("middle");
  await postToLinkedIn();
  console.log("finish")
}

run();

export const myData = {
  endpoint,
  accessToken,
  UID
}






