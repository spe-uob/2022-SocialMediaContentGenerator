import firebase from "firebase/compat/app"

const firebaseConfig = {
    apiKey: "AIzaSyAhLly_xBcWA2FTfeKe726EGCJmQD7mGHo",
    authDomain: "socialmediacontentgenerator.firebaseapp.com",
    projectId: "socialmediacontentgenerator",
    storageBucket: "socialmediacontentgenerator.appspot.com",
    messagingSenderId: "205591394295",
    appId: "1:205591394295:web:474e8be42ce7a64edde0f2"
  };
firebase.initializeApp(firebaseConfig);
firebase.getCurrentUser = () => {
  return new Promise((resolve, reject) => {
    const unsubscribe = firebase.auth().onAuthStateChanged(user => {
      unsubscribe();
      resolve(user);
    }, reject);
  })
  }
export default firebase
