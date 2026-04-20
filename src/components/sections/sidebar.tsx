"use client";

import React from "react";
import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  House,
  FileText,
  Lightbulb,
  Compass,
  Map,
  Target,
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
         description: "Landing page",
         active: true,
       },
     ],
   },
   {
     category: "Campus",
     items: [
       {
         icon: FileText,
         label: "Services",
         href: "#services",
         description: "Portal highlights",
       },
       {
         icon: Lightbulb,
         label: "About",
         href: "#about",
         description: "What AttendX does",
       },
       {
         icon: Compass,
         label: "How It Works",
         href: "#reviews",
         description: "User feedback",
       },
       {
         icon: Map,
         label: "Contact",
         href: "#contact",
         description: "Stay connected",
       },
     ],
   },
   {
     category: "Portal",
     items: [
       {
         icon: Target,
         label: "Dashboard",
         href: "/attendx.html",
         description: "Open the portal",
       },
       {
         icon: Sparkles,
         label: "Login",
         href: "/attendx.html#login",
         description: "Access account",
       },
       {
         icon: Settings,
         label: "Settings",
         href: "/attendx.html#settings",
         description: "Manage account",
       },
     ],
   },
   {
     category: "Support",
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
               { icon: FileText, label: "Services", href: "#services" },
               { icon: Target, label: "Portal", href: "/attendx.html" },
               { icon: Sparkles, label: "About", href: "#about" },
               { icon: User, label: "Contact", href: "#contact" },
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
                   alt="AttendX"
                  width={48}
                  height={48}
                  className="rounded-2xl shadow-lg group-hover:shadow-xl transition-all duration-300"
                  src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-careercompass-v2-vercel-app/assets/icons/logo-1.png"
                />
                <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-2xl opacity-0 group-hover:opacity-20 transition-opacity duration-300 blur" />
              </div>
              <div className="flex flex-col">
                <div className="font-bold text-lg bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
                   AttendX
                </div>
                <div className="text-[12px] text-gray-500 font-medium">
                   Smart attendance and activity intelligence
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
                 © 2025 AttendX
              </div>
               <div className="text-[12px] text-gray-500">Manage campus operations with confidence</div>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
