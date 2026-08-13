import React from "react";
import { Header } from "./Header";
import { MobileNavigation } from "./MobileNavigation";

interface AppShellProps {
  children: React.ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-[#131f24] text-white flex flex-col font-sans">
      <Header />
      <main className="flex-1 pb-20 md:pb-8 max-w-6xl w-full mx-auto p-4 md:p-8">
        {children}
      </main>
      <MobileNavigation />
    </div>
  );
};
