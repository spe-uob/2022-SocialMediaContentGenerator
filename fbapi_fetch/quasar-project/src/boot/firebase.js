import firebase from 'firebase/compat/app'
const firebaseConfig = {
  apiKey: 'AIzaSyBDwO_OvSwRkQJ66A_OFo4cOR51DdnLHsY',
  authDomain: 'test-b64fd.firebaseapp.com',
  projectId: 'test-b64fd',
  storageBucket: 'test-b64fd.appspot.com',
  messagingSenderId: '888879762179',
  appId: '1:888879762179:web:575028c2a264d7c8efb736',
  measurementId: 'G-JS1VSJ2JEH'
}

firebase.initializeApp(firebaseConfig)
firebase.getCurrentUser = () => {
  return new Promise((resolve, reject) => {
    const unsubscribe = firebase.auth().onAuthStateChanged(user => {
      unsubscribe()
      resolve(user)
    }, reject)
  })
}

window.fbAsyncInit = function () {
  // eslint-disable-next-line no-undef
  FB.init({
    appId: '645161304039045',
    xfbml: false,
    version: 'v16.0',
    cookie: true
  })
};
(function (d, s, id) {
  const fjs = d.getElementsByTagName(s)[0]
  if (d.getElementById(id)) { return }
  const js = d.createElement(s); js.id = id
  js.src = '//connect.facebook.net/en_US/sdk.js'
  fjs.parentNode.insertBefore(js, fjs)
}(document, 'script', 'facebook-jssdk'))
export default firebase
