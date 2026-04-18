import React from 'react';
import Image from 'next/image';
import { Sparkles, Map, MessageSquare, Zap } from 'lucide-react';

const AboutUs = () => {
  return (
    <section className="py-20 bg-white overflow-hidden">
      <div className="container mx-auto px-4 md:px-6">
        {/* Centered Heading with floating star decorations */}
        <div className="text-center mb-16 relative">
          <div className="inline-block relative">
            <h2 className="text-[48px] font-bold tracking-tight text-[#111827] mb-4">
              About US
            </h2>
            {/* Floating Star Decorations */}
            <div className="absolute -top-4 -right-10 flex space-x-1 animate-pulse">
              <Sparkles className="w-6 h-6 text-[#A855F7] opacity-60" />
              <div className="w-2 h-2 rounded-full bg-[#A5B4FC] mt-4" />
            </div>
          </div>
          <p className="text-[#6B7280] text-lg max-w-2xl mx-auto">
            Discover the best career paths that match your skills and interests
          </p>
          <div className="mt-4 flex justify-center">
             <div className="w-12 h-1 bg-gray-100 rounded-full" />
          </div>
        </div>

        {/* Tab-style Navigation */}
        <div className="flex flex-wrap justify-center gap-4 mb-16">
          <button className="flex items-center gap-2 px-6 py-3 rounded-full bg-[#f3f4f6] text-[#111827] text-sm font-medium transition-all hover:bg-white hover:shadow-lg border border-transparent hover:border-gray-100">
            <Zap className="w-4 h-4 text-indigo-500" />
            Get Career Insights
          </button>
          <button className="flex items-center gap-2 px-6 py-3 rounded-full bg-transparent text-[#6B7280] text-sm font-medium transition-all hover:text-[#111827]">
            <Map className="w-4 h-4" />
            View Your Roadmap
          </button>
          <button className="flex items-center gap-2 px-6 py-3 rounded-full bg-transparent text-[#6B7280] text-sm font-medium transition-all hover:text-[#111827]">
            <MessageSquare className="w-4 h-4" />
            Chat With Groq
          </button>
        </div>

        {/* Feature Card: Resume & Skill Analysis */}
        <div className="max-w-6xl mx-auto">
          <div className="relative bg-[#a5b4fc]/40 rounded-[2rem] border border-white/20 overflow-hidden shadow-2xl shadow-indigo-100/50">
            <div className="grid grid-cols-1 lg:grid-cols-2">
              {/* Text Side */}
              <div className="p-8 md:p-14 lg:p-16 flex flex-col justify-center">
                <div className="inline-flex items-center px-3 py-1 rounded-full bg-[#2dd4bf] text-white text-[10px] font-bold uppercase tracking-wider mb-6 w-fit">
                  Features
                </div>
                <h3 className="text-[42px] font-bold leading-tight text-[#111827] mb-6">
                  Resume & Skill Analysis
                </h3>
                <p className="text-[#6B7280] text-lg leading-relaxed mb-8">
                  Upload your resume and let our AI deeply analyze your skills, strengths, and experience. 
                  It then recommends the most suitable career paths, detects any missing skills, and 
                  generates an improvement plan to help you bridge the gap and grow faster.
                </p>
                <div className="flex items-center">
                   <div className="w-10 h-10 rounded-xl bg-[#111827] flex items-center justify-center">
                      <Zap className="w-5 h-5 text-white" />
                   </div>
                </div>
              </div>

              {/* Illustration Side */}
              <div className="relative p-8 lg:p-0 flex items-center justify-center bg-white/10 backdrop-blur-sm">
                <div className="relative w-full h-[400px] lg:h-full min-h-[450px]">
                  <Image
                    src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-careercompass-v2-vercel-app/assets/images/pic-3.jpg"
                    alt="Resume & Skill Analysis Illustration"
                    fill
                    className="object-contain p-4 lg:p-8 transform hover:scale-105 transition-transform duration-700"
                    priority
                  />
                  {/* Decorative blur elements for depth */}
                  <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-indigo-400 opacity-20 blur-[100px] -z-10" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AboutUs;