export function loadFBSDK(appId, version) {
  return new Promise(resolve => {
    window.fbAsyncInit = function () {
      FB.init({
        appId:"645161304039045",
        xfbml: false,
        version:"v16.0",
        cookie: true
      });
      FB.AppEvents.logPageView();
      resolve('SDK Loaded!');
    };
    (function (d, s, id) {
      const fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) { return; }
      const js = d.createElement(s); js.id = id;
      js.src = '//connect.facebook.net/en_UK/sdk.js';
      fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));
  });
}

export function getFBLoginStatus() {
  return new Promise(resolve => {
    window.FB.getLoginStatus(responseStatus => {
      resolve(responseStatus);
    });
  });
}

export function FBLogin(options) {
  return new Promise(resolve => {
    window.FB.login(response => resolve(response), options);
  });
}
export function FBLogout() {
  return new Promise(resolve => {
    window.FB.logout(response => resolve(response));
  });
}
