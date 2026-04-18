import React from 'react';

/**
 * CTAFooter Section
 * Features:
 * - Soft purple-to-white gradient background.
 * - Stylized "level up" headline with color-gradient spans.
 * - Centered copyright footer.
 * - Responsive layout matching the design guidelines.
 */
const CTAFooter: React.FC = () => {
  return (
    <footer className="w-full">
      {/* CTA Section */}
      <div className="relative w-full bg-gradient-to-br from-[#F5F3FF] via-white to-[#F5F3FF] py-24 px-4 overflow-hidden">
        {/* Subtle glow effect background elements as per high-level design */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-purple-200/20 blur-[100px] rounded-full -z-10" />
        
        <div className="container mx-auto max-w-4xl text-center">
          <h2 className="text-[2.5rem] md:text-[3.5rem] font-extrabold text-[#111827] tracking-tight leading-tight mb-6">
            Ready to{' '}
            <span className="inline-flex">
              <span className="text-[#A5B4FC]">l</span>
              <span className="text-[#C084FC]">e</span>
              <span className="text-[#2DD4BF]">v</span>
              <span className="text-[#38BDF8]">e</span>
              <span className="text-[#818CF8]">l</span>
              <span className="inline-block w-3" />
              <span className="text-[#6366F1]">u</span>
              <span className="text-[#A855F7]">p</span>
            </span>{' '}
            your career?
          </h2>
          
          <p className="text-lg md:text-xl text-[#6B7280] font-normal leading-relaxed max-w-2xl mx-auto mb-12">
            Join thousands of professionals who found their dream career path with our AI-powered platform.
          </p>

          <a 
            href="/auth"
            className="inline-flex items-center justify-center px-8 py-4 bg-[#111827] text-white rounded-full font-semibold transition-all hover:scale-105 active:scale-95 shadow-lg"
          >
            Get Started Now
          </a>
        </div>
      </div>

      {/* Footer Branding Section */}
      <div className="w-full bg-white py-12 border-t border-gray-100">
        <div className="container mx-auto px-4 flex flex-col items-center">
          <div className="flex flex-col items-center gap-2 mb-6 text-center">
            <div className="font-bold text-lg bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
              Career Compass
            </div>
            <div className="text-xs text-gray-500 font-medium">
              Navigate Your Future with AI
            </div>
          </div>
          
          <div className="text-sm text-gray-400 font-medium">
            © 2025 Career Compass. All rights reserved.
          </div>
        </div>
      </div>
    </footer>
  );
};

export default CTAFooter;