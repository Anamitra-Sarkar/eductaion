import React from 'react';
import Image from 'next/image';

export default function HowItWorks() {
  return (
    <section className="py-20 bg-[#f9fafb]">
      <div className="container mx-auto px-4">
        {/* Decorative Header */}
        <div className="flex flex-col items-center mb-12 text-center">
          <div className="relative inline-block mb-3">
            <h2 className="text-3xl md:text-[32px] font-bold text-[#111827] tracking-tight">
              An Ov
            </h2>
            <div className="absolute -bottom-1 left-0 w-full h-[3px] bg-gradient-to-r from-[#6366F1] to-[#A855F7]"></div>
          </div>
          <p className="text-[#6B7280] text-xs font-medium uppercase tracking-[0.1em]">
            See how Career Path Navigator works
          </p>
        </div>

        {/* Main Content Container */}
        <div className="max-w-[1100px] mx-auto bg-white border border-[#E5E7EB]/50 rounded-[2rem] shadow-xl shadow-black/5 overflow-hidden">
          {/* Internal Header */}
          <div className="pt-16 pb-12 px-8 text-center border-b border-[#E5E7EB]/30">
            <div className="flex items-center justify-center gap-2 mb-6">
              <div className="w-4 h-4 rounded-full bg-gradient-to-br from-[#6366F1] to-[#A855F7]"></div>
              <span className="font-bold text-lg text-[#111827]">Career Compass</span>
            </div>
            <h3 className="text-[56px] font-bold text-[#334155] leading-none mb-6 tracking-tight">
              How it all Works
            </h3>
            <p className="text-[#6B7280] text-lg max-w-2xl mx-auto leading-relaxed">
              From AI-driven analysis to personalized roadmaps, explore how our
              platform empowers your career growth.
            </p>
          </div>

          {/* Dashboard Preview Container */}
          <div className="p-8 md:p-12 bg-white">
            <div className="relative rounded-3xl border-[3px] border-[#A5B4FC]/40 overflow-hidden bg-white shadow-inner">
              {/* This represents the large screenshot area from the design */}
              <div className="relative aspect-[16/11] w-full overflow-hidden">
                <Image
                  src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-careercompass-v2-vercel-app/assets/images/resume-2.jpg"
                  alt="AI Driven Analysis Dashboard Roadmap"
                  fill
                  className="object-contain p-4 md:p-8"
                  priority
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}