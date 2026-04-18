"use client";

import React from "react";
import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  House,
  FileText,
  Code,
  Lightbulb,
  Compass,
  Map,
  Target,
  MessageSquare,
  TriangleAlert,
  Sparkles,
  Settings,
  LogIn,
  ChevronRight,
  User,
} from "lucide-react";

const menuItems = [
  {
    category: "Overview",
    items: [
      {
        icon: House,
        label: "Home",
        href: "/",
        description: "Dashboard overview",
        active: true,
      },
    ],
  },
  {
    category: "Career Development",
    items: [
      {
        icon: FileText,
        label: "Resume Analyzer",
        href: "/resume-analyzer",
        description: "AI-powered analysis",
      },
      {
        icon: Code,
        label: "GitGaze",
        href: "/portfolioranker",
        description: "AI-powered analysis",
      },
      {
        icon: Lightbulb,
        label: "Career Counselor",
        href: "/counselor",
        description: "Expert guidance",
      },
      {
        icon: Compass,
        label: "Career Path",
        href: "/path",
        description: "Plan your journey",
      },
      {
        icon: Map,
        label: "Roadmap",
        href: "/roadmap",
        description: "Visual progress",
      },
    ],
  },
  {
    category: "Job Search",
    items: [
      {
        icon: Target,
        label: "Company Target",
        href: "/company-target",
        description: "Find your match",
      },
      {
        icon: MessageSquare,
        label: "Interview Prep",
        href: "/interview-questions",
        description: "Practice questions",
      },
      {
        icon: TriangleAlert,
        label: "Failure Analysis",
        href: "/failureAnalyser",
        description: "Learn & improve",
      },
    ],
  },
  {
    category: "AI Tools",
    items: [
      {
        icon: Sparkles,
        label: "Ask Gen AI",
        href: "/askGroq",
        description: "AI assistant",
      },
      {
        icon: Settings,
        label: "Workflow Manager",
        href: "/WorkflowManager",
        description: "Organize tasks",
      },
    ],
  },
  {
    category: "Account",
    items: [
      {
        icon: LogIn,
        label: "Sign In",
        href: "/auth",
        description: "Access your account",
      },
    ],
  },
];

const Sidebar = () => {
  const pathname = usePathname();

  return (
    <>
      {/* Mobile Navigation (Floating Bottom Bar) */}
      <div className="fixed bottom-4 left-4 right-4 z-50 md:hidden">
        <div className="bg-white/90 backdrop-blur-xl border border-gray-200/50 rounded-2xl shadow-xl shadow-black/10 px-2 py-3">
          <div className="flex items-center justify-around">
            {[
              { icon: House, label: "Home", href: "/" },
              { icon: FileText, label: "Resume", href: "/resume-analyzer" },
              { icon: Target, label: "Jobs", href: "/company-target" },
              { icon: Sparkles, label: "AI Chat", href: "/askGroq" },
              { icon: User, label: "Profile", href: "/auth" },
            ].map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link key={item.label} href={item.href}>
                  <div
                    className={`relative flex flex-col items-center gap-1 px-3 py-2 rounded-xl transition-all duration-200 ${
                      isActive ? "text-indigo-600" : "text-gray-600 hover:text-indigo-500"
                    }`}
                  >
                    {isActive && (
                      <div className="absolute inset-0 bg-indigo-50 rounded-xl" />
                    )}
                    <item.icon
                      size={20}
                      className={`relative z-10 ${isActive ? "text-indigo-600" : ""}`}
                    />
                    <span
                      className={`text-[12px] font-medium relative z-10 ${
                        isActive ? "text-indigo-600" : ""
                      }`}
                    >
                      {item.label}
                    </span>
                  </div>
                </Link>
              );
            })}
          </div>
        </div>
      </div>

      {/* Desktop Sidebar */}
      <aside className="group peer text-sidebar-foreground hidden md:block" data-state="expanded">
        <div className="relative w-[280px] bg-transparent transition-[width] duration-200 ease-linear" />
        <div className="fixed inset-y-0 z-10 h-screen w-[280px] ease-linear left-0 p-2 border-r-0 bg-white/80 backdrop-blur-xl transition-all duration-300 flex flex-col glass-sidebar">
          {/* Header / Logo */}
          <div className="flex flex-col gap-2 p-6 border-b border-gray-100/50">
            <Link className="flex items-center gap-3 group" href="/">
              <div className="relative">
                <Image
                  alt="Career Path Navigator"
                  width={48}
                  height={48}
                  className="rounded-2xl shadow-lg group-hover:shadow-xl transition-all duration-300"
                  src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-careercompass-v2-vercel-app/assets/icons/logo-1.png"
                />
                <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-2xl opacity-0 group-hover:opacity-20 transition-opacity duration-300 blur" />
              </div>
              <div className="flex flex-col">
                <div className="font-bold text-lg bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
                  Career Compass
                </div>
                <div className="text-[12px] text-gray-500 font-medium">
                  AI-Powered Career Growth
                </div>
              </div>
            </Link>
          </div>

          {/* Navigation Content */}
          <div className="flex-1 flex flex-col gap-2 overflow-y-auto px-4 py-6 scrollbar-hide">
            {menuItems.map((section) => (
              <div key={section.category} className="mb-6 last:mb-0">
                <h3 className="mb-3 px-3 text-[12px] font-semibold text-gray-500 uppercase tracking-wider">
                  {section.category}
                </h3>
                <div className="space-y-1">
                  {section.items.map((item) => {
                    const isActive = item.active || pathname === item.href;
                    return (
                      <Link key={item.label} href={item.href}>
                        <div
                          className={`group flex items-center gap-3 rounded-xl px-3 py-3 transition-all duration-200 ${
                            isActive
                              ? "bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg shadow-indigo-500/25"
                              : "hover:bg-gray-50 text-gray-700 hover:text-indigo-600"
                          }`}
                        >
                          <item.icon
                            size={20}
                            className={`transition-all duration-200 ${
                              isActive ? "text-white" : "text-gray-500 group-hover:text-indigo-500"
                            }`}
                          />
                          <div className="flex-1 min-w-0">
                            <div className={`font-medium text-sm ${isActive ? "text-white" : ""}`}>
                              {item.label}
                            </div>
                            <div
                              className={`text-[12px] opacity-75 ${
                                isActive ? "text-white/80" : "text-gray-500"
                              }`}
                            >
                              {item.description}
                            </div>
                          </div>
                          {isActive && (
                            <ChevronRight size={16} className="text-white/80" />
                          )}
                        </div>
                      </Link>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>

          {/* Footer */}
          <div className="flex flex-col gap-2 p-6 border-t border-gray-100/50">
            <div className="text-center space-y-2">
              <div className="bg-gradient-to-r from-indigo-600/80 to-purple-600/80 bg-clip-text text-[12px] font-semibold text-transparent">
                © 2025 Career Compass
              </div>
              <div className="text-[12px] text-gray-500">Navigate Your Future with AI</div>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;