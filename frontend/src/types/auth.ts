export interface User {
  id: number;
  full_name: string;
  email: string;
  created_at: string;
}

export interface RegisterCredentials {
  full_name: string;
  email: string;
  password: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}
