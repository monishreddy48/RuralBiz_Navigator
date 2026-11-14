/**
 * Translates Firebase Authentication error codes into warm, clear, 
 * and accessible guidance for rural entrepreneurs and users.
 */
export function getFriendlyAuthErrorMessage(errorCode: string): string {
  switch (errorCode) {
    case "auth/invalid-credential":
    case "auth/user-not-found":
    case "auth/wrong-password":
      return "The email or password you entered does not match our records. Please double-check and try again.";
    
    case "auth/email-already-in-use":
      return "An account is already registered with this email address. Please sign in or use 'Forgot Password'.";
    
    case "auth/weak-password":
      return "Password is too short. Please choose a password with at least 6 characters for security.";
    
    case "auth/invalid-email":
      return "Please enter a valid email address (e.g., yourname@domain.com).";
    
    case "auth/popup-closed-by-user":
      return "Google sign-in popup was closed before completing. Please click Google Sign-In again.";
    
    case "auth/popup-blocked":
      return "Google sign-in window was blocked by your browser. Please allow popups for this site.";
    
    case "auth/unauthorized-domain":
      return "Firebase configuration note: 'localhost' is not yet added to Authorized Domains in your Firebase Console (Authentication > Settings > Authorized Domains).";
    
    case "auth/too-many-requests":
      return "Too many unsuccessful attempts. Access has been temporarily paused for security. Please try again in a few minutes or reset your password.";
    
    case "auth/network-request-failed":
      return "Unable to connect to the authentication server. Please check your internet connection.";
    
    case "auth/expired-action-code":
      return "This password reset link has expired. Please request a new password reset email.";
    
    case "auth/invalid-action-code":
      return "This password reset link is invalid or has already been used. Please request a new reset email.";

    case "auth/user-disabled":
      return "This account has been disabled. Please contact the RuralBiz support team.";

    case "auth/requires-recent-login":
      return "For your security, please log out and log back in before making this sensitive change.";

    case "auth/missing-credentials":
      return "Firebase credentials not configured. Please add your credentials to frontend/.env.local.";

    default:
      return "An unexpected authentication error occurred. Please try again.";
  }
}

