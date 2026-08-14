"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "../hooks/useAuth";

export function LoginForm() {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [formError, setFormError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const { login } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!identifier || !password) {
      setFormError("Please enter both email/username and password.");
      return;
    }
    setSubmitting(true);
    setFormError(null);
    try {
      await login({ email_or_username: identifier, password });
      router.push("/learn");
    } catch (err: any) {
      setFormError(err.message || "Invalid credentials.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ maxWidth: 420, margin: "40px auto", padding: 24, borderRadius: 16, border: "2px solid #e5e7eb", background: "#ffffff" }}>
      <h2 style={{ fontSize: 24, fontWeight: 700, textAlign: "center", marginBottom: 8, color: "#4b4b4b" }}>
        Log in to Duolingo
      </h2>
      <p style={{ textAlign: "center", color: "#777", marginBottom: 24, fontSize: 14 }}>
        Enter your credentials to access your course progress.
      </p>

      {formError && (
        <div style={{ padding: "10px 14px", borderRadius: 8, background: "#fee2e2", border: "1px solid #fca5a5", color: "#991b1b", fontSize: 14, marginBottom: 16 }}>
          {formError}
        </div>
      )}

      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 16 }}>
        <div>
          <label style={{ display: "block", fontSize: 13, fontWeight: 600, color: "#666", marginBottom: 4 }}>
            Email or Username
          </label>
          <input
            type="text"
            value={identifier}
            onChange={(e) => setIdentifier(e.target.value)}
            placeholder="demo@duolingo.clone"
            style={{ width: "100%", padding: "12px 14px", borderRadius: 10, border: "2px solid #e5e7eb", fontSize: 15, outline: "none" }}
            required
          />
        </div>

        <div>
          <label style={{ display: "block", fontSize: 13, fontWeight: 600, color: "#666", marginBottom: 4 }}>
            Password
          </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            style={{ width: "100%", padding: "12px 14px", borderRadius: 10, border: "2px solid #e5e7eb", fontSize: 15, outline: "none" }}
            required
          />
        </div>

        <button
          type="submit"
          disabled={submitting}
          style={{
            marginTop: 8,
            padding: 14,
            borderRadius: 12,
            background: "#58cc02",
            color: "#ffffff",
            fontWeight: 700,
            fontSize: 16,
            border: "none",
            boxShadow: "0 4px 0 #46a302",
            cursor: submitting ? "not-allowed" : "pointer",
            opacity: submitting ? 0.7 : 1,
          }}
        >
          {submitting ? "Logging in..." : "LOG IN"}
        </button>
      </form>

      <div style={{ marginTop: 24, textAlign: "center", fontSize: 14, color: "#777" }}>
        Don't have an account?{" "}
        <Link href="/register" style={{ color: "#1cb0f6", fontWeight: 700, textDecoration: "none" }}>
          Create one
        </Link>
      </div>
    </div>
  );
}
