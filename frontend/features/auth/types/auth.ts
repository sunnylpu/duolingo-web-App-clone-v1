import { User } from "@/types";

export interface AuthState {
  user: User | null;
  loading: boolean;
  error: string | null;
}
