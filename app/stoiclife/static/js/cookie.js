// Function to check if the cookie_consent cookie exists and its value
function checkCookieConsent() {
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith('stoic_cookie_consent=')) {
      return cookie.substring('stoic_cookie_consent='.length);
    }
  }
  return null;
}

// Function to hide the cookie consent bar
function hideCookieConsentBar() {
  const consent_bar = document.getElementById('cookie-consent-bar').style.display = 'none';
}

// Check cookie consent status on page load
document.addEventListener('DOMContentLoaded', function () {
  const consentStatus = checkCookieConsent();
  const consentBar = document.getElementById('cookie-consent-bar');
  if (consentStatus === 'accepted' || consentStatus === 'rejected') {
    // If user has already accepted or rejected cookies, hide the cookie consent bar
    hideCookieConsentBar();
  } else {
    consentBar.classList.remove('d-none')
  }
});

const accept_cookies = document.getElementById('accept-cookies');


document.getElementById('accept-cookies').addEventListener('click', function () {
  document.cookie = 'stoic_cookie_consent=accepted; expires=Fri, 31 Dec 9999 23:59:59 GMT; path=/';
  hideCookieConsentBar();
});


const reject_cookies = document.getElementById('reject-cookies');


document.getElementById('reject-cookies').addEventListener('click', function () {
  document.cookie = 'stoic_cookie_consent=rejected; expires=Fri, 31 Dec 9999 23:59:59 GMT; path=/';
  window.show_cookie_consent = false;
  hideCookieConsentBar();
});


