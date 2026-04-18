import React from 'react';
import Image from 'next/image';

const Footer = () => {
  return (
    <footer className="bg-[#000319] w-full text-white">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Main Footer Content */}
        <div className="pt-48 pb-12 grid grid-cols-1 gap-y-10 gap-x-16 sm:grid-cols-2 lg:grid-cols-12">
          
          {/* Brand Identity Section */}
          <div className="lg:col-span-4">
            <div className="flex items-center gap-2 mb-6">
              <Image 
                src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/icons/logo-white-1200x1200-1.png"
                alt="PrepMaster Logo"
                width={40}
                height={40}
                className="object-contain"
              />
              <span className="text-2xl font-bold tracking-tight">PrepMaster</span>
            </div>
          </div>

          {/* Spacer for layout matching */}
          <div className="hidden lg:block lg:col-span-2"></div>

          {/* Quick Links Column */}
          <div className="lg:col-span-2">
            <ul className="space-y-4">
              <li>
                <a href="/" className="text-sm font-medium text-gray-300 hover:text-white transition-colors">
                  Home
                </a>
              </li>
              <li>
                <a href="#popular" className="text-sm font-medium text-gray-300 hover:text-white transition-colors">
                  Popular
                </a>
              </li>
              <li>
                <a href="#about" className="text-sm font-medium text-gray-300 hover:text-white transition-colors">
                  About
                </a>
              </li>
              <li>
                <a href="#contact" className="text-sm font-medium text-gray-300 hover:text-white transition-colors">
                  Contact
                </a>
              </li>
            </ul>
          </div>

          {/* Contact Information Column */}
          <div className="lg:col-span-4">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center p-2 rounded-lg">
                <Image 
                  src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/svgs/email-15.svg"
                  alt="Email Icon"
                  width={20}
                  height={20}
                />
              </div>
              <a 
                href="mailto:projectsportfolio75@gmail.com" 
                className="text-sm font-medium text-gray-300 hover:text-white transition-colors"
              >
                projectsportfolio75@gmail.com
              </a>
            </div>
          </div>
        </div>

        {/* Bottom Legal Row */}
        <div className="border-t border-gray-800 py-10 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-sm text-gray-400">
            @2025 PrepMaster. All Rights Reserved
          </p>
          <div className="flex items-center gap-6">
            <a href="/privacy-policy" className="text-sm text-gray-400 hover:text-white transition-colors">
              Privacy policy
            </a>
            <div className="h-4 w-[1px] bg-gray-700 hidden md:block"></div>
            <a href="/terms-and-conditions" className="text-sm text-gray-400 hover:text-white transition-colors">
              Terms & conditions
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;