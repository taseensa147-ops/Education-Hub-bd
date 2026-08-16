// Helper to decode the JWT payload returned by Google
function parseJwt(token) {
  const base64Url = token.split('.')[1];
  const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  const jsonPayload = decodeURIComponent(
    atob(base64)
      .split('')
      .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
      .join('')
  );
  return JSON.parse(jsonPayload);
}

// Global Callback handler invoked by Google's library
function handleCredentialResponse(response) {
  // response.credential contains the Google ID Token (JWT)
  const responsePayload = parseJwt(response.credential);

  console.log("User Google Account Data:");
  console.log("ID: " + responsePayload.sub);
  console.log("Full Name: " + responsePayload.name);
  console.log("Given Name: " + responsePayload.given_name);
  console.log("Family Name: " + responsePayload.family_name);
  console.log("Image URL: " + responsePayload.picture);
  console.log("Email: " + responsePayload.email);

  // In production, send `response.credential` to your backend server 
  // to create an account in your database or issue a session cookie.
  alert(`Welcome, ${responsePayload.name}! Signed in successfully.`);
}

document.addEventListener('DOMContentLoaded', () => {
  const customBtn = document.getElementById('google-signin-btn');
  
  if (customBtn) {
    customBtn.addEventListener('click', () => {
      // Trigger Google Prompt Programmatically
      google.accounts.id.prompt();
    });
  }
});