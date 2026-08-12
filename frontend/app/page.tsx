"use client";

import { useEffect, useState } from "react";
import { checkBackendHealth } from "@/lib/api-client";
import { apiService } from "@/services/api";

export default function HomePage() {
  const [backendStatus, setBackendStatus] = useState<{
    online: boolean;
    statusText: string;
    loading: boolean;
  }>({
    online: false,
    statusText: "Checking...",
    loading: true,
  });

  const [coursesCount, setCoursesCount] = useState<number | null>(null);

  const apiUrl =
    process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

  const verifyBackend = async () => {
    setBackendStatus((prev) => ({ ...prev, loading: true }));
    const health = await checkBackendHealth();
    setBackendStatus({
      online: health.online,
      statusText: health.statusText,
      loading: false,
    });

    if (health.online) {
      const coursesRes = await apiService.getCourses();
      if (coursesRes.data && Array.isArray(coursesRes.data)) {
        setCoursesCount(coursesRes.data.length);
      }
    }
  };

  useEffect(() => {
    verifyBackend();
  }, []);

  const domains = [
    { name: "User Domain", path: "/api/v1/users", status: "Ready" },
    { name: "Course Domain", path: "/api/v1/courses", status: "Ready" },
    { name: "Lesson Domain", path: "/api/v1/lessons", status: "Ready" },
    { name: "Progress Domain", path: "/api/v1/progress", status: "Ready" },
    { name: "Gamification Domain", path: "/api/v1/gamification", status: "Ready" },
    { name: "Leaderboard Domain", path: "/api/v1/leaderboard", status: "Ready" },
  ];

  return (
    <main className="min-h-screen p-6 md:p-12 max-w-5xl mx-auto flex flex-col justify-between">
      {/* Header */}
      <header className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-8 border-b border-[#37464f]">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-[#58cc02] flex items-center justify-center text-black font-extrabold text-2xl shadow-[0_4px_0_#46a302]">
            D
          </div>
          <div>
            <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight">
              Duolingo Clone
            </h1>
            <p className="text-sm text-gray-400 font-medium">
              Phase 01 Architectural Foundation
            </p>
          </div>
        </div>

        {/* Backend Status Card */}
        <div className="duo-card px-4 py-3 flex items-center gap-3">
          <span className="text-xs uppercase font-bold text-gray-400">
            Backend API:
          </span>
          <div className="flex items-center gap-2">
            <span
              className={`w-3 h-3 rounded-full ${
                backendStatus.loading
                  ? "bg-yellow-400 animate-pulse"
                  : backendStatus.online
                  ? "bg-[#58cc02] shadow-[0_0_8px_#58cc02]"
                  : "bg-[#ff4b4b]"
              }`}
            />
            <span className="font-bold text-sm">
              {backendStatus.loading
                ? "Connecting..."
                : backendStatus.online
                ? "Online (HTTP 200)"
                : `Disconnected (${backendStatus.statusText})`}
            </span>
          </div>
        </div>
      </header>

      {/* Main Content Body */}
      <section className="my-10 space-y-8">
        <div className="duo-card p-6 md:p-8 border-2 border-[#37464f] relative overflow-hidden">
          <div className="absolute top-0 right-0 p-8 opacity-10 text-9xl font-black select-none pointer-events-none text-white">
            01
          </div>
          <h2 className="text-xl md:text-2xl font-bold mb-3 text-[#58cc02]">
            Phase 01 Foundation Verified
          </h2>
          <p className="text-gray-300 max-w-2xl text-sm md:text-base leading-relaxed">
            Infrastructure, containerization readiness, SQLAlchemy SQLite persistence,
            Pydantic Settings, centralized CORS, logging, error handling, and 6 domain
            modules have been successfully initialized.
          </p>

          <div className="mt-6 pt-6 border-t border-[#37464f] flex flex-wrap gap-4 text-xs font-mono text-gray-400">
            <div>
              <span className="text-gray-500">API Prefix:</span>{" "}
              <code className="text-[#1cb0f6]">{apiUrl}</code>
            </div>
            {coursesCount !== null && (
              <div>
                <span className="text-gray-500">Sample Course Data:</span>{" "}
                <span className="text-green-400 font-bold">{coursesCount} courses returned</span>
              </div>
            )}
          </div>
        </div>

        {/* Domain Scaffolding Grid */}
        <div>
          <h3 className="text-lg font-bold mb-4 text-gray-200">
            Domain Boundary Scaffolding (6 Modules)
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {domains.map((domain) => (
              <div
                key={domain.name}
                className="duo-card p-4 hover:border-[#1cb0f6] transition-colors"
              >
                <div className="flex justify-between items-start mb-2">
                  <h4 className="font-bold text-base text-white">{domain.name}</h4>
                  <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-[#131f24] text-[#58cc02] border border-[#37464f]">
                    {domain.status}
                  </span>
                </div>
                <code className="text-xs text-gray-400 block font-mono">
                  {domain.path}
                </code>
                <p className="text-xs text-gray-500 mt-2">
                  Router → Service → Repository → Model
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="pt-6 border-t border-[#37464f] flex flex-col sm:flex-row justify-between items-center text-xs text-gray-500 gap-4">
        <div>Next.js 14 App Router + Python FastAPI Modular Monolith</div>
        <button
          onClick={verifyBackend}
          className="duo-button-green px-4 py-2 text-black font-bold rounded-xl text-xs"
        >
          Re-test API Connection
        </button>
      </footer>
    </main>
  );
}
