import React from "react";
import { Button } from "@/components/ui/Button";

interface OutOfHeartsModalProps {
  isOpen: boolean;
  onExit: () => void;
}

export const OutOfHeartsModal: React.FC<OutOfHeartsModalProps> = ({
  isOpen,
  onExit,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fadeIn">
      <div className="duo-card w-full max-w-sm p-6 bg-[#182830] border-2 border-[#ff4b4b] text-center space-y-5 shadow-2xl">
        <div className="w-20 h-20 rounded-full bg-[#ff4b4b]/20 border-2 border-[#ff4b4b] text-[#ff4b4b] flex items-center justify-center text-4xl mx-auto animate-bounce">
          💔
        </div>

        <div>
          <h3 className="text-2xl font-black text-white">Out of Hearts</h3>
          <p className="text-xs text-gray-300 mt-2 font-medium">
            You made 5 mistakes in this session.
          </p>
          <div className="mt-3 text-lg font-black text-[#ff4b4b]">
            ❤️ 0 remaining
          </div>
        </div>

        <div className="p-3 bg-[#131f24] rounded-xl border border-[#37464f] text-xs text-gray-400">
          <p className="font-bold text-white mb-1">Practice to regain hearts</p>
          <span className="text-[10px] text-gray-500 uppercase tracking-widest font-mono">
            COMING SOON
          </span>
        </div>

        <div className="flex gap-3 pt-2">
          <Button variant="outline" className="flex-1 text-xs" disabled>
            PRACTICE
          </Button>
          <Button variant="danger" className="flex-1 text-xs font-bold" onClick={onExit}>
            EXIT TO PATH
          </Button>
        </div>
      </div>
    </div>
  );
};
