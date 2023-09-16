import $ from "jquery";
import { API_URL } from "./config";

export function registerUser(email, password) {
  return $.ajax({
    type: 'POST',
    url: `${API_URL}/auth/register`,
    data: JSON.stringify({ email, password }),
    contentType: 'application/json',
    headers: {
      'from-frontend' : true
    }
  });
}

export function verifyEmail(verificationToken) {
  return $.ajax({
    type: 'GET',
    url: `${API_URL}/auth/verify_email/${verificationToken}`,
  });
}

export function loginUser(email, password) {
  return $.ajax({
    type: 'POST',
    url: `${API_URL}/auth/login`,
    data: JSON.stringify({ email, password }),
    contentType: 'application/json'
  });
}

export function getRecommenders() {
  return $.ajax({
    type: 'GET',
    url: `${API_URL}/list-recommenders`,
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    },
  });
}

export function getRecommendation(generator, amount) {
  return $.ajax({
    type: 'POST',
    url: `${API_URL}/recommend`,
    data: JSON.stringify({
      generator,
      amount,
    }),
    contentType: 'application/json',
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    },
  });
}

export async function checkToken() {
  return $.ajax({
      type: 'GET',
      url: `${API_URL}/auth/check-token`,
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
    });
}

export async function refreshToken() {
  try {
    const response = await $.ajax({
      type: 'POST',
      url: `${API_URL}/auth/refresh-token`,
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('refresh_token')}`,
        'Content-Type': 'application/json',
      },
    });
    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('access_token', data.access_token);
      return true;
    }
    return false;
  } catch (error) {
    return false;
  }
}

export function logout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  console.log("Logged out successfully.")
}

export async function isAuth() {
  // Check if an access token exists in localStorage
  const accessToken = localStorage.getItem('access_token');
  if (!accessToken) {
    return false;
  }

  // Check if the access token is still valid
  const tokenValid = await checkToken();
  if (tokenValid) {
    return true;
  }

  // If the access token has expired, attempt to refresh it using the refresh token
  const refreshSuccess = await refreshToken();
  if (refreshSuccess) {
    return true;
  }

  // If all the checks fail, log the user out
  logout();
  return false;
}

export function subscribe(recommender, frequency, numRecommendations) {
  const subscriptionData = {
    recommender,
    frequency,
    num_recommendations: numRecommendations,
  };

  console.log(JSON.stringify(subscriptionData))

  return $.ajax({
    type: 'POST',
    url: `${API_URL}/subscribe`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      'Content-Type': 'application/json',
    },
    data: JSON.stringify(subscriptionData),
  });
}

export function editSubscription(recommender, frequency, numRecommendations) {
  const subscriptionData = {
    recommender,
    frequency,
    num_recommendations: numRecommendations,
  };

  return $.ajax({
    type: 'PUT',
    url: `${API_URL}/edit-subscription`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      'Content-Type': 'application/json',
    },
    data: JSON.stringify(subscriptionData),
  });
}

export function viewSubscription() {
  return $.ajax({
    type: 'GET',
    url: `${API_URL}/view-subscription`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    },
  });
}

export function deleteSubscription() {
  return $.ajax({
    type: 'DELETE',
    url: `${API_URL}/delete-subscription`,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    },
  });
}
