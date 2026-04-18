"use client";

import React from "react";
import Image from "next/image";

/**
 * Navbar component for the InnovaDocs landing page.
 * Features a sticky header with glassmorphism effects, a logo with an online status indicator,
 * a central pill-shaped navigation menu, and a "Sign In" CTA.
 */
export default function Navbar() {
  return (
    <header className="bg-white border-b border-slate-200/60 sticky top-0 z-50 shadow-sm w-full transition-all duration-300">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between px-6 py-4 lg:h-[94px]">
          {/* Logo Section */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-3">
              <div className="relative group">
                {/* Logo Image Container with Border and Shadow */}
                <div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center shadow-lg group-hover:shadow-xl transition-all duration-300 overflow-hidden border border-cyan-200">
                  <Image
                    alt="Logo"
                    className="object-contain w-10 h-10"
                    src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-innova-docs-vercel-app/assets/icons/logo-1.jpg"
                    width={40}
                    height={40}
                  />
                </div>
                {/* Green "Online" Status Indicator */}
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-white flex items-center justify-center">
                  <div className="w-2 h-2 bg-white rounded-full"></div>
                </div>
              </div>

              {/* Brand Name and Subtitle */}
              <div className="flex flex-col">
                <span className="text-xl font-bold text-slate-900 tracking-tight leading-7">
                  InnovaDocs
                </span>
                <span className="text-xs text-slate-500 font-medium uppercase tracking-wide leading-4">
                  Document AI
                </span>
              </div>
            </div>
          </div>

          {/* Desktop Navigation - Pill Shaped Menu */}
          <div className="hidden lg:flex items-center">
            <nav className="flex items-center bg-gradient-to-r from-slate-100 to-slate-50 rounded-full p-2 space-x-2 shadow-md border border-slate-200">
              <a
                href="#features"
                className="px-8 py-3 text-sm font-semibold text-slate-800 hover:text-cyan-600 hover:bg-white rounded-full transition-all duration-200 shadow-sm hover:shadow-lg transform hover:scale-105"
              >
                Features
              </a>
              <a
                href="#workflow"
                className="px-8 py-3 text-sm font-semibold text-slate-800 hover:text-cyan-600 hover:bg-white rounded-full transition-all duration-200 shadow-sm hover:shadow-lg transform hover:scale-105"
              >
                Workflow
              </a>
              <a
                href="#dashboard"
                className="px-8 py-3 text-sm font-semibold text-slate-800 hover:text-cyan-600 hover:bg-white rounded-full transition-all duration-200 shadow-sm hover:shadow-lg transform hover:scale-105"
              >
                Dashboard
              </a>
              <a
                href="/onboarding"
                className="px-8 py-3 text-sm font-semibold text-slate-800 hover:text-cyan-600 hover:bg-white rounded-full transition-all duration-200 shadow-sm hover:shadow-lg transform hover:scale-105"
              >
                Onboarding
              </a>
            </nav>
          </div>

          {/* Call to Action - Sign In Button */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-3">
              <a href="/signin">
                <button 
                  className="inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm bg-cyan-600 text-white hover:bg-cyan-700 font-bold px-6 py-3 h-11 rounded-xl shadow-lg hover:shadow-xl transition-all duration-200 border border-cyan-600 hover:border-cyan-700 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                >
                  Sign In
                </button>
              </a>
            </div>
          </div>
        </div>

        {/* Mobile Navigation Links */}
        <div className="lg:hidden px-6 pb-4">
          <div className="flex items-center justify-center space-x-6">
            <a
              href="#features"
              className="text-sm font-medium text-slate-600 hover:text-cyan-600 transition-colors duration-200"
            >
              Features
            </a>
            <a
              href="#workflow"
              className="text-sm font-medium text-slate-600 hover:text-cyan-600 transition-colors duration-200"
            >
              Workflow
            </a>
            <a
              href="#dashboard"
              className="text-sm font-medium text-slate-600 hover:text-cyan-600 transition-colors duration-200"
            >
              Dashboard
            </a>
            <a
              href="/onboarding"
              className="text-sm font-medium text-slate-600 hover:text-cyan-600 transition-colors duration-200"
            >
              Onboarding
            </a>
          </div>
        </div>
      </div>
    </header>
  );
}