import axios from 'axios'
import qs from 'qs'

const client_id = '78sme225fsy5by'
const client_secret = 'J3xg14qRTV87viVq'
const redirect_uri = 'http://localhost:9000'
const scope = 'r_liteprofile r_emailaddress w_member_social'
const state = Math.random().toString(36).substring(7)
const linkedinAuthUrl = `https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=${client_id}&redirect_uri=${encodeURIComponent(redirect_uri)}&state=${state}&scope=${scope}`

function getAccessToken(code) {
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

  return axios.post('https://www.linkedin.com/oauth/v2/accessToken', qs.stringify(data), { headers })
    .then(response => response.data.access_token)
}

export { linkedinAuthUrl, getAccessToken }
