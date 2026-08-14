import { apiClient } from "@/lib/api-client";
import { User } from "@/types";

export interface RegisterPayload {
  email: string;
  username: string;
  password: string;
  display_name?: string;
}

export interface LoginPayload {
  email_or_username: string;
  password: string;
}

export interface AuthResponse {
  user: User;
  status: string;
  message?: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in_minutes: number;
}

export const authService = {
  register: (payload: RegisterPayload): Promise<AuthResponse> => {
    return apiClient.post<AuthResponse>("/auth/register", payload);
  },

  login: (payload: LoginPayload): Promise<AuthResponse> => {
    return apiClient.post<AuthResponse>("/auth/login", payload);
  },

  logout: (): Promise<{ status: string; message: string }> => {
    return apiClient.post<{ status: string; message: string }>("/auth/logout");
  },

  getMe: (): Promise<User> => {
    return apiClient.get<User>("/auth/me");
  },
};
