import axios from 'axios'
import http from 'http'

const clientId = '78sme225fsy5by';
const clientSecret = 'J3xg14qRTV87viVq';
const redirectUri = 'http://localhost:9000';

//const http = require('http');



function login() {
  const responseType = 'code';
  const scope = 'r_emailaddress r_liteprofile w_member_social';
  const url = `https://www.linkedin.com/oauth/v2/authorization?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=${responseType}&scope=${scope}`;

  console.log(`Open this URL in your web browser and follow the instructions:\n${url}`);
}

function getToken(code) {
  axios.post('https://www.linkedin.com/oauth/v2/accessToken', null, {
    params: {
      grant_type: 'authorization_code',
      code,
      redirect_uri: redirectUri,
      client_id: clientId,
      client_secret: clientSecret,
    },
  })
    .then(response => {
      const accessToken = response.data.access_token;
      getUserInfo(accessToken);
    })
    .catch(error => {
      console.error(error);
    });
}

function getUserInfo(accessToken) {
  axios.get('https://api.linkedin.com/v2/me', {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })
    .then(response => {
      console.log(response.data);
    })
    .catch(error => {
      console.error(error);
    });
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const code = url.searchParams.get('code');
  if (code) {
    getToken(code);
    res.end('Authorization successful! You may now close this window.');
  } else {
    res.end('Authorization failed! Please try again.');
  }
});

server.listen(9010, () => {
  console.log('Server listening on port 8080');
  login();
});


function run(){
  login()
}

run()

