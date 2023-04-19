import axios from 'axios'
//import http from 'http'

const clientId = '78sme225fsy5by';
const clientSecret = 'J3xg14qRTV87viVq';
const redirectUri = 'http://localhost:9000';
let url = ' ';
//const http = require('http');

const axiosInstance = axios.create({
  baseURL: 'https://www.linkedin.com/oauth/v2',
  params: {
    client_id: '78sme225fsy5by',
    client_secret: 'J3xg14qRTV87viVq',
    redirect_uri: 'http://localhost:9000',
    scope: 'r_emailaddress r_liteprofile w_member_social',
    grant_type: 'authorization_code'
  }
});



export async function  login() {
  const responseType = 'code';
  const scope = 'r_emailaddress r_liteprofile w_member_social';
  url = `https://www.linkedin.com/oauth/v2/authorization?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=${responseType}&scope=${scope}`;
  /*axios.post(url).then(response => {
    const accessToken = response.data.access_token;
    console.log(accessToken);
  })
    .catch(error => {
      console.error(error);
    });*/
  console.log(`Open this URL in your web browser and follow the instructions:\n${url}`);
}

export const getToken = async (code) => {
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
      console.log(response.data.access_token)
      return response.data.access_token;
      //getUserInfo(accessToken);
    })
    .catch(error => {
      console.error(error);
    });
}

const getAccessToken = async (code) => {
  const response = await axiosInstance.post('/accessToken', null, {
    params: {
      code,
      grant_type: 'authorization_code',
      redirect_uri: redirectUri,
    }
  });
  return response.data.access_token;
};

export const  getUserInfo = async (accessToken) =>{
  axios.get('https://api.linkedin.com/v2/me', {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })
    .then(response => {
      console.log(response.data);
      return response.data;

    })
    .catch(error => {
      console.error(error);
    });
};

const handleRedirect = async (RedirectUrl) => {
  const params = new URLSearchParams(new URL(RedirectUrl).search);
  console.log(params)
  const code = params.get('code');
  console.log(code)
  const accessToken = await getAccessToken(code);
  console.log(accessToken)
  console.log("hhhhhheeeerrrrreeeeee")
  //const accessToken = await getToken(code);
  const userProfile = await getUserInfo(accessToken);
  console.log("finish")

  console.log(userProfile);
};

/*const server = http.createServer((req, res) => {
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
  console.log('Server listening on port 9010');
  login();
});*/


async function run() {
  console.log("start")
  await login()

  console.log("middle")
  setTimeout(() => {handleRedirect(url)}, 20000);
  console.log("finish")
  //getToken()
}

run()

