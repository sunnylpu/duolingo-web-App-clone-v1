import React from "react";
import { Button } from "@/components/ui/Button";

interface ExitConfirmationModalProps {
  isOpen: boolean;
  onStay: () => void;
  onLeave: () => void;
}

export const ExitConfirmationModal: React.FC<ExitConfirmationModalProps> = ({
  isOpen,
  onStay,
  onLeave,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fadeIn">
      <div className="duo-card w-full max-w-sm p-6 bg-[#182830] border-2 border-[#ff4b4b] text-center space-y-4 shadow-2xl">
        <div className="w-14 h-14 rounded-full bg-[#ff4b4b]/20 text-[#ff4b4b] flex items-center justify-center text-2xl mx-auto border-2 border-[#ff4b4b]">
          ⚠️
        </div>
        <div>
          <h3 className="text-xl font-black text-white">Leave lesson?</h3>
          <p className="text-xs text-gray-400 mt-1">
            Your session progress may be lost if you leave now.
          </p>
        </div>
        <div className="flex gap-3 pt-2">
          <Button variant="outline" className="flex-1" onClick={onStay}>
            STAY
          </Button>
          <Button variant="danger" className="flex-1" onClick={onLeave}>
            LEAVE
          </Button>
        </div>
      </div>
    </div>
  );
};
