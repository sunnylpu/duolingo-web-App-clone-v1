"use client";

import { useEffect } from "react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";

export default function GlobalErrorPage({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log unexpected frontend error to console
    console.error("Global Next.js Error Boundary caught error:", error);
  }, [error]);

  return (
    <div className="min-h-[70vh] flex items-center justify-center p-4 text-center select-none">
      <Card className="max-w-md w-full p-8 bg-[#182830] border-2 border-[#ff4b4b] space-y-6 shadow-2xl">
        <div className="w-20 h-20 rounded-full bg-[#ff4b4b]/20 border-4 border-[#ff4b4b] text-[#ff4b4b] flex items-center justify-center text-4xl mx-auto">
          ⚠️
        </div>

        <div>
          <h1 className="text-2xl font-black text-white">Something went wrong!</h1>
          <p className="text-xs text-gray-400 font-medium mt-2">
            An unexpected application error occurred while loading this page.
          </p>
        </div>

        {error.digest && (
          <div className="text-[10px] text-gray-500 font-mono bg-[#131f24] p-2 rounded-lg border border-[#37464f]">
            Digest ID: {error.digest}
          </div>
        )}

        <div className="flex gap-3">
          <Button
            variant="outline"
            className="w-1/2"
            onClick={() => (window.location.href = "/learn")}
          >
            Go Home
          </Button>
          <Button variant="primary" className="w-1/2" onClick={() => reset()}>
            TRY AGAIN 🔄
          </Button>
        </div>
      </Card>
    </div>
  );
}
