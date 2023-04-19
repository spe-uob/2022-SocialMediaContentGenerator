import axios from 'axios'
import crypto from 'crypto'

const CLIENT_ID = '78sme225fsy5by';
const CLIENT_SECRET = 'J3xg14qRTV87viVq';
const REDIRECT_URI = 'http://localhost:9000';
const STATE = crypto.randomBytes(16).toString('hex');;
const SCOPE = 'r_liteprofile r_emailaddress w_member_social';

const axiosInstance = axios.create({
  baseURL: 'https://www.linkedin.com/oauth/v2',
  params: {
    client_id: CLIENT_ID,
    client_secret: CLIENT_SECRET,
    redirect_uri: REDIRECT_URI,
    scope: SCOPE,
    grant_type: 'authorization_code'
  }
});

const authorizeUrl = `https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&state=${STATE}`;

const getAccessToken = async (code) => {
  const response = await axiosInstance.post('/accessToken', null, {
    params: {
      code,
      grant_type: 'authorization_code',
      redirect_uri: REDIRECT_URI,
    }
  });
  return response.data.access_token;
};

const getUserProfile = async (accessToken) => {
  const response = await axios.get('https://api.linkedin.com/v2/me', {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
  return response.data;
};

const authorizeUser = () => {
  window.location.href = authorizeUrl;
};

// In a real app, you would likely handle the redirect with a server-side endpoint
// that can securely store the access token and perform authenticated requests to
// the LinkedIn API on behalf of the user.

const handleRedirect = async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get('code');
  const accessToken = await getAccessToken(code);
  const userProfile = await getUserProfile(accessToken);
  console.log(userProfile);
};

// Example usage:
authorizeUser();

// After the user authorizes your app, they will be redirected back to your redirect URI
// with an authorization code as a query parameter. You can handle the redirect and
// exchange the authorization code for an access token by calling `handleRedirect`.
