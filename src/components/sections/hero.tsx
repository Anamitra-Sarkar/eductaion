import React from 'react';
import Image from 'next/image';

/**
 * Hero component for AttendX.
 * Features animated background blurs, gradient typography, and shimmer CTA button.
 */
const HeroSection = () => {
  return (
    <section className="relative w-full overflow-hidden bg-white">
      {/* Animated Background Blur Circles */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden select-none">
        <div 
          className="duration-1000 transition-all min-h-24 min-w-24 rounded-full blur-3xl absolute bg-purple-500/30 top-12 left-10 animate-pulse" 
          style={{ width: '200px', height: '200px' }}
        />
        <div 
          className="duration-1000 transition-all min-h-24 min-w-24 rounded-full blur-3xl absolute bg-yellow-300/30 bottom-20 left-40 animate-pulse delay-700" 
          style={{ width: '250px', height: '250px' }}
        />
        <div 
          className="duration-1000 transition-all min-h-24 min-w-24 rounded-full blur-3xl absolute bg-green-400/30 top-12 right-10 animate-pulse delay-1000" 
          style={{ width: '180px', height: '180px' }}
        />
        <div 
          className="duration-1000 transition-all min-h-24 min-w-24 rounded-full blur-3xl absolute bg-cyan-500/30 bottom-3 right-52 animate-pulse delay-300" 
          style={{ width: '220px', height: '220px' }}
        />
        
        {/* Decorative Leaf Shapes (Absolute UI elements from screenshot) */}
        <div className="absolute top-[10%] left-[10%] opacity-80">
          <Image src="/assets/newsletter/leaf.svg" alt="" width={60} height={60} className="text-orange-400 rotate-12" />
        </div>
        <div className="absolute top-[12%] right-[10%] opacity-80">
          <Image src="/assets/newsletter/leaf.svg" alt="" width={60} height={60} className="text-sky-400 -rotate-45" />
        </div>
      </div>

      <div className="container relative z-10 pt-20 sm:pt-28 pb-16">
        <div className="max-w-7xl mx-auto flex flex-col items-center">
          {/* Headline Container */}
          <div className="text-center max-w-4xl mx-auto">
            <h1 className="text-4xl sm:text-5xl lg:text-7xl font-bold tracking-tight text-[#001529] leading-[1.1]">
              Power campus operations with{' '}
              <span className="relative inline-block">
                <span className="bg-gradient-to-r from-[#13c4f9] to-[#2563eb] bg-clip-text text-transparent">
                   AttendX
                </span>
                {/* Sparkle replacements (using text-shadow and gradient effect style) */}
                <span className="absolute -top-2 -right-6 text-xl">✨</span>
              </span>{' '}
              AI
            </h1>
            
            <p className="mt-8 text-lg md:text-xl text-[#4B5563] max-w-2xl mx-auto leading-relaxed">
               Track attendance, manage activities, publish learning content, and keep internships connected in one secure portal.
            </p>
          </div>

          {/* Shimmer CTA Button */}
          <div className="mt-10 mb-16 text-center">
            <button className="group relative inline-flex items-center justify-center p-0.5 mb-2 mr-2 overflow-hidden text-sm font-medium text-gray-900 rounded-tr-2xl rounded-bl-2xl rounded-br-2xl group bg-gradient-to-br from-[#13c4f9] via-[#f3f4f6] to-[#13c4f9] focus:ring-4 focus:outline-none focus:ring-sky-300">
              <span className="relative px-10 py-5 transition-all ease-in duration-75 bg-[#139ef4] rounded-tr-2xl rounded-bl-2xl rounded-br-2xl group-hover:bg-opacity-0">
                <a 
                  href="/sign-in" 
                  className="text-white text-2xl sm:text-3xl font-semibold no-underline"
                >
                  Get Started
                </a>
              </span>
              {/* Shimmer overlay effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent -translate-x-full group-hover:animate-[shimmer_2s_infinite] pointer-events-none" />
            </button>
          </div>

          {/* Dashboard Preview Image */}
          <div className="relative w-full max-w-6xl mx-auto">
            <div className="relative rounded-2xl border border-cyan-800/10 shadow-2xl overflow-hidden bg-white">
              <Image 
                src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/images/images_9.png"
                alt="AttendX Dashboard"
                width={1200}
                height={675}
                layout="responsive"
                priority
                className="w-full h-auto object-cover"
              />
            </div>
            
            {/* Soft decorative spheres for depth around image */}
            <div className="absolute -bottom-10 -left-10 w-24 h-24 bg-green-400 rounded-full blur-2xl opacity-40 z-[-1]" />
            <div className="absolute -top-10 -right-10 w-32 h-32 bg-sky-400 rounded-full blur-2xl opacity-30 z-[-1]" />
          </div>
        </div>
      </div>
      
      <style jsx global>{`
        @keyframes shimmer {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(100%); }
        }
      `}</style>
    </section>
  );
};

export default HeroSection;
