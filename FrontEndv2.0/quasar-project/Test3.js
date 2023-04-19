//const axios = require('axios');
//const crypto = require('crypto');
//const { URLSearchParams } = require('url');
import axios from 'axios';
import crypto from "crypto";
import { URLSearchParams } from 'url'

const clientId = '78sme225fsy5by';
const clientSecret = 'J3xg14qRTV87viVq';
const redirectUri = 'http://localhost:9000';
const scope = 'r_liteprofile r_emailaddress w_member_social';

export function authorize(){
  const responseType = 'code';
  const authorizeUrl = `https://www.linkedin.com/oauth/v2/authorization?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=${responseType}&scope=${scope}`;
  console.log(`Open this URL in your web browser and follow the instructions:\n${authorizeUrl}`);
  window.location.href = authorizeUrl;
}

export function handleResponse(){
  console.log("HHHHHHEEEEEEERRRRR")
  const url = new URL(window.location.href);
  const code = url .searchParams.get('code');
  console.log("HHHEEEERRRREEEE")
  console.log(code)

  if(code){

    axios.post('localhost:8888/api/linkedin/access_token', {
      code: code,
    }).then(response => {
              console.log("YOOOOOOOOOO")
              console.log(response.data.access_token);
              const accessToken = response.data.access_token;

      // Add the appropriate headers to the API request
              const config = {
                headers: {
                  'Authorization': `Bearer ${accessToken}`,
                  /*'Access-Control-Allow-Origin': '*',
                  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
                  'Access-Control-Allow-Headers': 'Content-Type, Authorization',*/
                  'cache-control': 'no-cache',
                  'X-Restli-Protocol-Version': '2.0.0'
                },
                params: {
                  'projection': '(id,firstName,lastName,profilePicture(displayImage~:playableStreams))'
                }
              };

              // Send a GET request to the LinkedIn API to get the user's profile
              axios.get('https://api.linkedin.com/v2/me', config)
                .then(response => {
                  console.log(response.data);
                })
                .catch(error => {
                  console.error(error);
                });
          }).catch(error => {
            console.log("NNNNNNAAAAAAHHHHHHH")
            console.error(error);
          });
            } else {
            // The user has not authorized your app yet, or there was an error
            // Redirect the user to the authorization URL to start the authorization process
            authorize();
          }
}
