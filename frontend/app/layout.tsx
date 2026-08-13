import type { Metadata } from "next";
import { AppShell } from "@/components/layout/AppShell";
import "./globals.css";

export const metadata: Metadata = {
  title: "Duolingo Clone - Language Learning Platform",
  description: "Scalable full-stack language-learning platform built with Next.js and FastAPI",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased bg-[#131f24] text-white selection:bg-[#58cc02] selection:text-black">
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
