"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "../hooks/useAuth";

export function RegisterForm() {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [password, setPassword] = useState("");
  const [formError, setFormError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const { register } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !username || !password) {
      setFormError("Please fill in all required fields.");
      return;
    }
    setSubmitting(true);
    setFormError(null);
    try {
      await register({
        email,
        username,
        password,
        display_name: displayName || undefined,
      });
      router.push("/learn");
    } catch (err: any) {
      setFormError(err.message || "Failed to create account.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ maxWidth: 440, margin: "40px auto", padding: 24, borderRadius: 16, border: "2px solid #e5e7eb", background: "#ffffff" }}>
      <h2 style={{ fontSize: 24, fontWeight: 700, textAlign: "center", marginBottom: 8, color: "#4b4b4b" }}>
        Create Your Profile
      </h2>
      <p style={{ textAlign: "center", color: "#777", marginBottom: 24, fontSize: 14 }}>
        Join millions of learners around the world.
      </p>

      {formError && (
        <div style={{ padding: "10px 14px", borderRadius: 8, background: "#fee2e2", border: "1px solid #fca5a5", color: "#991b1b", fontSize: 14, marginBottom: 16 }}>
          {formError}
        </div>
      )}

      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 14 }}>
        <div>
          <label style={{ display: "block", fontSize: 13, fontWeight: 600, color: "#666", marginBottom: 4 }}>
            Email Address
          </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="name@example.com"
            style={{ width: "100%", padding: "12px 14px", borderRadius: 10, border: "2px solid #e5e7eb", fontSize: 15, outline: "none" }}
            required
          />
        </div>

        <div>
          <label style={{ display: "block", fontSize: 13, fontWeight: 600, color: "#666", marginBottom: 4 }}>
            Username
          </label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="polyglot_learner"
            style={{ width: "100%", padding: "12px 14px", borderRadius: 10, border: "2px solid #e5e7eb", fontSize: 15, outline: "none" }}
            required
          />
        </div>

        <div>
          <label style={{ display: "block", fontSize: 13, fontWeight: 600, color: "#666", marginBottom: 4 }}>
            Display Name (Optional)
          </label>
          <input
            type="text"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            placeholder="Alex Johnson"
            style={{ width: "100%", padding: "12px 14px", borderRadius: 10, border: "2px solid #e5e7eb", fontSize: 15, outline: "none" }}
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
            placeholder="Min 6 characters"
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
            background: "#1cb0f6",
            color: "#ffffff",
            fontWeight: 700,
            fontSize: 16,
            border: "none",
            boxShadow: "0 4px 0 #1899d6",
            cursor: submitting ? "not-allowed" : "pointer",
            opacity: submitting ? 0.7 : 1,
          }}
        >
          {submitting ? "Creating Account..." : "CREATE ACCOUNT"}
        </button>
      </form>

      <div style={{ marginTop: 24, textAlign: "center", fontSize: 14, color: "#777" }}>
        Already have an account?{" "}
        <Link href="/login" style={{ color: "#58cc02", fontWeight: 700, textDecoration: "none" }}>
          Log in
        </Link>
      </div>
    </div>
  );
}
