"use client";

import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";

export default function NotFoundPage() {
  return (
    <div className="min-h-[70vh] flex items-center justify-center p-4 text-center select-none">
      <Card className="max-w-md w-full p-8 bg-[#182830] border-2 border-[#1cb0f6] space-y-6 shadow-2xl">
        <div className="w-20 h-20 rounded-full bg-[#1cb0f6]/20 border-4 border-[#1cb0f6] text-[#1cb0f6] flex items-center justify-center text-4xl mx-auto">
          🔍
        </div>

        <div>
          <h1 className="text-3xl font-black text-white">404 - Page Not Found</h1>
          <p className="text-xs text-gray-400 font-medium mt-2">
            The page or resource you are looking for does not exist on your learning path.
          </p>
        </div>

        <Link href="/learn" className="block">
          <Button variant="primary" size="lg" className="w-full">
            RETURN TO LEARNING PATH →
          </Button>
        </Link>
      </Card>
    </div>
  );
}
