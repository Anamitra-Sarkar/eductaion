import React from 'react';
import Image from 'next/image';

const statsData = [
  {
    icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/svgs/ourbuyers-2.svg",
    value: "80",
    unit: "k",
    title: "Our buyers",
    description: "Follow a hashtag growth total posts, videos and images.",
  },
  {
    icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/svgs/projectcompleted-3.svg",
    value: "90",
    unit: "k",
    title: "Project completed",
    description: "Follow a hashtag growth total posts, videos and images.",
  },
  {
    icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/svgs/happybuyers-4.svg",
    value: "80",
    unit: "k",
    title: "Happy buyers",
    description: "Follow a hashtag growth total posts, videos and images.",
  },
  {
    icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/svgs/teammembers-5.svg",
    value: "50",
    unit: "k",
    title: "Team members",
    description: "Follow a hashtag growth total posts, videos and images.",
  },
];

const StatsSection = () => {
  return (
    <section className="bg-white py-16 px-6 sm:px-8 lg:px-12 w-full">
      <div className="mx-auto max-w-7xl">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-y-20 gap-x-5">
          {statsData.map((stat, index) => (
            <div 
              key={index} 
              className="flex flex-col justify-center items-center group"
            >
              {/* Icon Container */}
              <div className="flex justify-center border border-[#e5e7eb] p-2 w-10 h-10 rounded-lg bg-white mb-5 transition-colors duration-300">
                <Image
                  src={stat.icon}
                  alt={stat.title}
                  width={30}
                  height={30}
                  className="object-contain"
                />
              </div>

              {/* Numerical Value */}
              <h2 className="text-[40px] lg:text-[60px] text-black font-semibold text-center leading-tight">
                <span>{stat.value}</span>{stat.unit}
              </h2>

              {/* Title */}
              <h3 className="text-2xl text-black font-semibold text-center mt-4 lg:mt-6 mb-2">
                {stat.title}
              </h3>

              {/* Description */}
              <p className="text-lg font-normal text-black text-center text-opacity-50 max-w-[280px]">
                {stat.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default StatsSection;