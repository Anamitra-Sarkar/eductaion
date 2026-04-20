import React from 'react';
import Image from 'next/image';

const ServiceCard = ({ 
  icon, 
  title, 
  className = "" 
}: { 
  icon: string; 
  title: string; 
  className?: string;
}) => {
  return (
    <div className={`bg-white rounded-[24px] p-6 shadow-soft flex flex-col items-start min-h-[180px] ${className}`}>
      <div className="mb-5 flex items-center justify-center">
        <Image 
          src={icon} 
          alt={title} 
          width={64} 
          height={64} 
          className="object-contain"
        />
      </div>
      <h4 className="text-[24px] font-semibold text-[#001529] leading-tight">
        {title}
      </h4>
    </div>
  );
};

const ServicesSection = () => {
  return (
    <section id="services" className="w-full bg-white py-16 sm:py-24 overflow-hidden">
      <div className="container mx-auto max-w-7xl px-4 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          {/* Left Content Side */}
          <div className="lg:col-span-6 flex flex-col justify-center text-center lg:text-left">
            <h2 className="text-[40px] lg:text-[64px] font-semibold text-[#001529] leading-[1.1] mb-6">
              Everything your campus needs.
            </h2>
            <p className="text-[18px] font-normal text-[#4B5563] leading-[1.6] mb-8 max-w-2xl mx-auto lg:mx-0">
              AttendX connects administration, faculty, and students with real-time attendance, activities, learning content, internships, and verification tools backed by the database.
            </p>
              <a 
                href="/" 
                className="inline-flex items-center gap-2 text-[20px] font-medium text-[#2563EB] hover:opacity-80 transition-opacity mx-auto lg:mx-0"
              >
              Explore portal
                <Image 
                  src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/svgs/arrow-6.svg" 
                  alt="arrow" 
                width={20} 
                height={20} 
              />
            </a>
          </div>

          {/* Right Cards Side with Staggered Grid */}
          <div className="lg:col-span-6 relative">
            {/* Soft Blue Background Shape */}
            <div className="absolute inset-0 bg-[#E0F2FE] rounded-[32px] -z-10 transform translate-x-4 translate-y-4 sm:translate-x-10 sm:translate-y-10 lg:translate-x-20 lg:-mr-20"></div>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 p-6 sm:p-10 lg:pl-10 lg:pr-0">
              <div className="flex flex-col gap-6 lg:-ml-12">
                <ServiceCard 
                  icon="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/svgs/marketing-7.svg" 
                  title="Attendance Analytics" 
                />
                <ServiceCard 
                  icon="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/svgs/heaking-9.svg" 
                  title="Role-Based Editing" 
                />
              </div>
              
              <div className="flex flex-col gap-6 pt-0 sm:pt-12 lg:-ml-12">
                <ServiceCard 
                  icon="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/svgs/graphic-8.svg" 
                  title="Learning & Internships" 
                />
                <ServiceCard 
                  icon="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/svgs/uidesign-10.svg" 
                  title="Secure Documents" 
                />
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
};

export default ServicesSection;
