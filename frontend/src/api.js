// api.js

import $ from "jquery";
import { API_URL } from "./config";

export function registerUser(email, password) {
  return $.ajax({
    type: 'POST',
    url: `${API_URL}/api/auth/register`,
    data: JSON.stringify({ email, password }),
    contentType: 'application/json'
  });
}

export function loginUser(email, password) {
  return $.ajax({
    type: 'POST',
    url: `${API_URL}/api/auth/login`,
    data: JSON.stringify({ email, password }),
    contentType: 'application/json'
  });
}
