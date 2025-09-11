import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

// TODO: Replace these with your Firebase config from step 4
const firebaseConfig = {
 apiKey: "AIzaSyACqdEe-jaV5fNrJYzsP4q0YrpBgLPagCg",
  authDomain: "fitness-app-test-31e86.firebaseapp.com",
  projectId: "fitness-app-test-31e86",
  storageBucket: "fitness-app-test-31e86.firebasestorage.app",
  messagingSenderId: "628832599085",
  appId: "1:628832599085:web:f78ab6871640b89b984ca4"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const db = getFirestore(app);
