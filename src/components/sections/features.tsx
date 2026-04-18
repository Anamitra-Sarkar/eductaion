import React from 'react';
import Image from 'next/image';

const features = [
  {
    title: 'AI-Driven Efficiency',
    description: 'Simplifies and enhances every interview step.',
    icon: 'https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/svgs/check-11.svg',
  },
  {
    title: 'Customizable and Shareable',
    description: 'Access tips, mock interviews, and expert insights.',
    icon: 'https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/svgs/check-11.svg',
  },
  {
    title: 'Professional Resumes',
    description: 'Create standout resumes that impress and pass ATS.',
    icon: 'https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/svgs/check-11.svg',
  },
  {
    title: 'Collaborative Community',
    description: 'Share resources and feedback with fellow interviewers.',
    icon: 'https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/svgs/check-11.svg',
  },
  {
    title: 'Top LinkedIn Jobs',
    description: 'Interviewers can check the top LinkedIn interviews as well in our platform',
    icon: 'https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/svgs/check-11.svg',
  },
];

const Features = () => {
  return (
    <section id="about" className="overflow-hidden bg-white">
      <div className="mx-auto max-w-7xl px-4 py-20 sm:py-28 lg:px-8">
        <div className="grid grid-cols-1 items-center gap-x-12 lg:grid-cols-2">
          {/* Left Side: iPad Mockup */}
          <div className="relative -ml-20 lg:-ml-64 flex justify-center lg:justify-start">
            <Image
              src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/images/images_5.png"
              alt="iPad-image"
              width={1600}
              height={900}
              className="max-w-[140%] lg:max-w-[160%] h-auto"
              priority
            />
          </div>

          {/* Right Side: Copy and Features */}
          <div className="mt-12 lg:mt-0">
            <div className="max-w-xl mx-auto lg:mx-0">
              <h3 className="text-4xl font-semibold tracking-tight text-[#001529] sm:text-5xl lg:text-5xl text-center lg:text-start">
                Why we best?
              </h3>
              <p className="mt-6 text-lg leading-relaxed text-[#4b5563] text-center lg:text-start">
                Dont waste time on search manual tasks. Let Automation do it for you. Simplify workflows, reduce errors, and save time.
              </p>

              <div className="mt-12 space-y-8">
                {features.map((feature, index) => (
                  <div key={index} className="flex items-start">
                    <div className="flex-shrink-0">
                      <div className="flex h-11 w-11 items-center justify-center rounded-full bg-[#E0F2FE]/50">
                        <Image
                          src={feature.icon}
                          alt="check-image"
                          width={24}
                          height={24}
                        />
                      </div>
                    </div>
                    <div className="ml-5">
                      <h4 className="text-2xl font-semibold text-[#001529]">
                        {feature.title}
                      </h4>
                      <p className="mt-2 text-lg text-[#4b5563] font-normal leading-tight">
                        {feature.description}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Features;