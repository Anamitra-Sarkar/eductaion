"use client";

import React from "react";
import { House, FileText, Target, Sparkles, User } from "lucide-react";
import { cn } from "@/lib/utils";

interface NavItemProps {
  href: string;
  icon: React.ElementType;
  label: string;
  isActive?: boolean;
}

const NavItem = ({ href, icon: Icon, label, isActive }: NavItemProps) => {
  return (
    <a href={href} className="block group">
      <div
        className={cn(
          "relative flex flex-col items-center gap-1 px-3 py-2 rounded-xl transition-all duration-200",
          isActive
            ? "text-[#4f46e5]"
            : "text-gray-600 hover:text-[#6366f1]"
        )}
      >
        {isActive && (
          <div 
            className="absolute inset-0 bg-[#eef2ff] rounded-xl" 
            style={{ backgroundColor: "oklch(0.962 0.018 272.314)" }}
          />
        )}
        <Icon
          className={cn(
            "h-5 w-5 relative z-10 transition-colors duration-200",
            isActive ? "text-[#4f46e5]" : "text-gray-500 group-hover:text-[#6366f1]"
          )}
        />
        <span
          className={cn(
            "text-xs font-medium relative z-10 transition-colors duration-200",
            isActive ? "text-[#4f46e5]" : "text-gray-600 group-hover:text-[#6366f1]"
          )}
        >
          {label}
        </span>
      </div>
    </a>
  );
};

const MobileNav = () => {
  // Navigation items definition
  const navItems = [
    { href: "/", icon: House, label: "Home", isActive: true },
    { href: "/resume-analyzer", icon: FileText, label: "Resume" },
    { href: "/company-target", icon: Target, label: "Jobs" },
    { href: "/askGroq", icon: Sparkles, label: "AI Chat" },
    { href: "/auth", icon: User, label: "Profile" },
  ];

  return (
    <div className="fixed bottom-4 left-4 right-4 z-50 md:hidden">
      <div 
        className="bg-white/90 backdrop-blur-xl border border-gray-200/50 rounded-2xl shadow-xl shadow-black/10 px-2 py-3"
        style={{
          boxShadow: "rgba(0, 0, 0, 0.1) 0px 20px 25px -5px, rgba(0, 0, 0, 0.1) 0px 8px 10px -6px",
          backgroundColor: "rgba(255, 255, 255, 0.9)",
          borderRadius: "16px"
        }}
      >
        <div className="flex items-center justify-around">
          {navItems.map((item) => (
            <NavItem
              key={item.label}
              href={item.href}
              icon={item.icon}
              label={item.label}
              isActive={item.isActive}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default MobileNav;