const express = require('express');
const axios = require('axios');

//import express from 'express'
//import axios from 'axios'

const app = express();
const port = process.env.PORT || 8888;

// Endpoint to exchange the authorization code for an access token
app.post('/api/linkedin/access_token', (req, res) => {
  const params = new URLSearchParams({
    grant_type: 'authorization_code',
    code: req.body.code,
    redirect_uri: 'http://localhost:9000',
      client_id: '78sme225fsy5by',
        client_secret: 'J3xg14qRTV87viVq'
          });

          axios.post('https://www.linkedin.com/oauth/v2/accessToken', params)
          .then(response => {
          res.send(response.data);
        })
          .catch(error => {
          console.error(error);
          res.status(500).send('Error exchanging authorization code for access token');
        });
          });

          // Start the server
          app.listen(port, () => {
          console.log(`Server listening on port ${port}`);
        });
