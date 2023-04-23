import firebase from "firebase/compat/app"
import { getAuth } from "firebase/auth"

const firebaseConfig = {
    apiKey: "AIzaSyAhLly_xBcWA2FTfeKe726EGCJmQD7mGHo",
    authDomain: "socialmediacontentgenerator.firebaseapp.com",
    projectId: "socialmediacontentgenerator",
    storageBucket: "socialmediacontentgenerator.appspot.com",
    messagingSenderId: "205591394295",
    appId: "1:205591394295:web:474e8be42ce7a64edde0f2"
  };
firebase.initializeApp(firebaseConfig);

export const auth = getAuth()
