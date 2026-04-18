import React from 'react';
import Image from 'next/image';

const AnalyticsPatterns = () => {
  return (
    <section className="flex flex-col items-center justify-center py-20 px-6 bg-white overflow-hidden">
      <div className="max-w-[1280px] w-full flex flex-col lg:flex-row items-center justify-between gap-12 lg:gap-8">
        
        {/* Left Card: Database Design */}
        <div className="w-full max-w-[320px] lg:w-80 transition-all duration-300">
          <div className="relative overflow-hidden h-full rounded-2xl transition duration-200 group bg-white hover:shadow-xl border border-gray-200">
            {/* Image Container with Hover Zoom */}
            <div className="w-full aspect-[16/10] bg-[#f3f4f6] rounded-t-2xl overflow-hidden relative min-h-[160px]">
              <Image
                src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-aivis-liart-vercel-app/assets/images/images_9.png"
                alt="Database Design thumbnail"
                fill
                className="group-hover:scale-95 group-hover:rounded-2xl transform object-cover transition duration-500 ease-in-out"
              />
            </div>
            
            {/* Card Content */}
            <div className="p-4 flex flex-col h-full">
              <h3 className="font-bold my-4 text-lg text-[#111827] leading-tight">
                Database Design with Prisma and Postgres
              </h3>
              <p className="font-normal text-sm text-[#6b7280] leading-relaxed mb-6">
                How to create database design with Prisma and Postgres. In this article, we will learn how to create database design with Prisma and Postgres.
              </p>
              
              <div className="mt-auto pt-4 flex flex-row justify-between items-center border-t border-transparent">
                <span className="text-xs text-[#6b7280] font-medium">28th March, 2024</span>
                <button className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 active:scale-95 transition-all bg-[#f97316] text-white hover:bg-[#f97316]/90 h-10 px-4 py-2 shadow-sm">
                  Read More
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Center Text Block */}
        <div className="flex flex-col gap-6 text-center text-balance py-8 order-first lg:order-none max-w-sm">
          <h2 className="text-[2.25rem] font-bold leading-[1.2] text-[#111827] tracking-tight">
            For All types of <br /> Flowcharts
          </h2>
          <p className="text-[1rem] text-[#6b7280] leading-relaxed max-w-[320px] mx-auto">
            From simple flowcharts to complex diagrams, we have got you covered. From wireframes to mind maps to algorithms, we have got you covered too!!
          </p>
        </div>

        {/* Right Card: Serverless Functions */}
        <div className="w-full max-w-[320px] lg:w-80 transition-all duration-300">
          <div className="relative overflow-hidden h-full rounded-2xl transition duration-200 group bg-white hover:shadow-xl border border-gray-200">
            {/* Image Container with Hover Zoom */}
            <div className="w-full aspect-[16/10] bg-[#f3f4f6] rounded-t-2xl overflow-hidden relative min-h-[160px]">
              <Image
                src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-aivis-liart-vercel-app/assets/images/images_10.png"
                alt="Serverless Functions thumbnail"
                fill
                className="group-hover:scale-95 group-hover:rounded-2xl transform object-cover transition duration-500 ease-in-out"
              />
            </div>
            
            {/* Card Content */}
            <div className="p-4 flex flex-col h-full">
              <h3 className="font-bold my-4 text-lg text-[#111827] leading-tight">
                Serverless Functions with Next.js and Firebase
              </h3>
              <p className="font-normal text-sm text-[#6b7280] leading-relaxed mb-6">
                How to create serverless functions with Next.js and Firebase. In this article, we will learn how to create serverless functions with Next.js and Firebase.
              </p>
              
              <div className="mt-auto pt-4 flex flex-row justify-between items-center border-t border-transparent">
                <span className="text-xs text-[#6b7280] font-medium">28th March, 2024</span>
                <button className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 active:scale-95 transition-all bg-[#f97316] text-white hover:bg-[#f97316]/90 h-10 px-4 py-2 shadow-sm">
                  Read More
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </section>
  );
};

export default AnalyticsPatterns;