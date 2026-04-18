"use client";

import React, { useState } from "react";
import Image from "next/image";
import { Menu } from "lucide-react";

/**
 * Header Section component based on the PrepMaster light theme.
 * Features: Sticky navigation, glassmorphism effect, logo, menu links, and CTA buttons.
 */
export default function Header() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navLinks = [
    { name: "Home", href: "/" },
    { name: "Services", href: "#services" },
    { name: "About", href: "#about" },
    { name: "Reviews", href: "#reviews" },
    { name: "Contact", href: "#contact" },
  ];

  return (
    <header className="sticky top-0 z-[99] w-full border-b border-border bg-white/40 backdrop-blur-md">
      <div className="mx-auto max-w-screen-xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo Area */}
          <div className="md:flex md:items-center md:gap-12">
            <a className="flex items-center justify-center gap-2 font-semibold text-primary" href="/">
              <Image
                alt="PrepMaster Logo"
                width={40}
                height={50}
                src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/icons/favicon-2.ico"
                className="h-auto w-10 object-contain"
              />
              <span className="text-xl tracking-tight text-brand-navy">PrepMaster</span>
            </a>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:block">
            <nav aria-label="Global">
              <ul className="flex items-center gap-6 text-[14px] font-medium">
                {navLinks.map((link) => (
                  <li key={link.name}>
                    <a
                      className="text-foreground transition hover:text-primary"
                      href={link.href}
                    >
                      {link.name}
                    </a>
                  </li>
                ))}
              </ul>
            </nav>
          </div>

          {/* Actions: Login, Sign Up, Mobile Menu */}
          <div className="flex items-center gap-4">
            <div className="flex gap-4">
              <a
                className="inline-flex h-11 items-center justify-center whitespace-nowrap rounded-md bg-primary px-8 text-sm font-medium text-primary-foreground transition-all duration-300 active:scale-95 hover:bg-primary/90"
                href="/sign-in"
              >
                Login
              </a>
              <div className="hidden sm:flex">
                <a
                  className="inline-flex h-11 items-center justify-center whitespace-nowrap rounded-md bg-secondary px-8 text-sm font-medium text-secondary-foreground transition-all duration-300 active:scale-95 hover:bg-secondary/80"
                  href="/sign-up"
                >
                  Sign Up
                </a>
              </div>
            </div>

            {/* Mobile Menu Button */}
            <div className="block md:hidden">
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="inline-flex h-10 items-center justify-center whitespace-nowrap rounded-md bg-secondary p-2 text-sm font-medium text-secondary-foreground transition-all duration-300 active:scale-95 hover:bg-secondary/80 hover:text-accent-foreground"
                aria-expanded={isMobileMenuOpen}
              >
                <Menu className="h-6 w-6" />
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Navigation Dropdown */}
        {isMobileMenuOpen && (
          <div className="md:hidden border-t border-border py-4 animate-in fade-in slide-in-from-top-1 duration-200">
            <nav>
              <ul className="flex flex-col gap-4 text-sm font-medium">
                {navLinks.map((link) => (
                  <li key={link.name}>
                    <a
                      className="block px-2 py-1 text-foreground transition hover:text-primary"
                      href={link.href}
                      onClick={() => setIsMobileMenuOpen(false)}
                    >
                      {link.name}
                    </a>
                  </li>
                ))}
                <li className="sm:hidden">
                  <a
                    className="block px-2 py-1 text-primary font-bold"
                    href="/sign-up"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    Sign Up
                  </a>
                </li>
              </ul>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
}