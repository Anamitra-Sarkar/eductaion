import React from 'react';
import Image from 'next/image';

const Testimonials = () => {
  return (
    <section className="mx-auto max-w-2xl py-40 px-4 sm:px-6 lg:max-w-7xl lg:px-8 overflow-hidden" id="reviews">
      <div className="bg-image-what relative">
        {/* Section Heading */}
        <div className="text-center mb-16">
          <h3 className="text-navyblue text-center text-4xl lg:text-6xl font-semibold leading-tight">
            What say clients about us.
          </h3>
          <h4 className="text-lg font-normal text-darkgray text-center mt-4 max-w-2xl mx-auto">
            Prep Master is a platform that helps to connect with interviewor around the world
          </h4>
        </div>

        {/* Circular Avatar Layout */}
        <div className="relative flex flex-col items-center justify-center min-h-[600px] lg:min-h-[733px]">
          {/* Background Decorative Elements - Orbit Lines & Blobs (SVG-like lines inferred from layout) */}
          <div className="absolute inset-0 pointer-events-none hidden lg:block">
             <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] border border-gray-100 rounded-full opacity-50"></div>
             <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[450px] h-[450px] border border-gray-100 rounded-full opacity-30"></div>
          </div>

          {/* Scattered Colored Bubbles (Aurora style) */}
          <div className="absolute top-10 left-[20%] w-4 h-4 rounded-full bg-orange-400 opacity-80 hidden lg:block"></div>
          <div className="absolute bottom-[20%] left-[10%] w-2 h-2 rounded-full bg-cyan-400 opacity-60 hidden lg:block"></div>
          <div className="absolute top-0 right-[40%] w-3 h-3 rounded-full bg-cyan-300 opacity-70 hidden lg:block"></div>
          <div className="absolute bottom-[10%] right-[20%] w-3 h-3 rounded-full bg-green-400 opacity-80 hidden lg:block"></div>
          <div className="absolute top-[20%] right-[15%] w-6 h-10 rounded-full bg-blue-300 transform rotate-45 opacity-60 hidden lg:block"></div>

          {/* Desktop/Tablet Master Image Path (Contains all avatars in orbit) */}
          <div className="relative w-full max-w-[1061px] hidden lg:block">
            <Image
              alt="avatar-image"
              width={1061}
              height={733}
              className="mx-auto"
              src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/images/images_7.png"
            />
          </div>

          {/* Central Featured Testimonial Card */}
          <div className="lg:absolute lg:top-1/2 lg:left-1/2 lg:-translate-x-1/2 lg:-translate-y-1/2 z-10 w-full max-w-lg">
            <div className="flex flex-col items-center">
              {/* Central User Avatar */}
              <div className="relative mb-8 lg:mb-0 lg:-mt-10">
                <Image
                  alt="user-image"
                  width={168}
                  height={168}
                  className="mx-auto rounded-full border-4 border-white shadow-lg"
                  src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/images/images_6.png"
                />
              </div>

              {/* Review Content Card */}
              <div className="bg-white rounded-2xl p-8 lg:p-10 shadow-soft border border-gray-50 text-center max-w-md mx-auto mt-4">
                <p className="text-base lg:text-lg font-normal text-darkgray leading-relaxed mb-6">
                  I am very happy with the service provided by Prep Master.
                  <br className="hidden md:block" />
                  It is very easy to use and the support team
                  <br className="hidden md:block" />
                  is always available to help me with any issues.
                </p>
                <h3 className="text-2xl font-semibold text-navyblue py-1">
                  Jony Scotty
                </h3>
                <h4 className="text-sm font-medium text-gray-500 uppercase tracking-wider">
                  UI Designer
                </h4>
              </div>
            </div>
          </div>

          {/* Mobile Fallback Avatars (If needed, but using the main assets provided) */}
          <div className="flex flex-wrap justify-center gap-4 mt-12 lg:hidden">
             {/* Small avatars for mobile as replacements for the orbit image */}
             <div className="w-12 h-12 rounded-full border-2 border-primary/20 overflow-hidden bg-gray-100"></div>
             <div className="w-12 h-12 rounded-full border-2 border-primary/40 overflow-hidden bg-gray-200"></div>
             <div className="w-12 h-12 rounded-full border-2 border-blue-400 overflow-hidden bg-gray-300"></div>
             <div className="w-12 h-12 rounded-full border-2 border-green-400 overflow-hidden bg-gray-200"></div>
          </div>
        </div>
      </div>

      <style jsx>{`
        .bg-image-what {
          background-size: contain;
          background-position: center;
          background-repeat: no-repeat;
        }
        .text-navyblue {
          color: #001529;
        }
        .text-darkgray {
           color: #4b5563;
        }
        .shadow-soft {
          box-shadow: 0px 10px 15px -3px rgba(0, 0, 0, 0.05), 0px 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
      `}</style>
    </section>
  );
};

export default Testimonials;