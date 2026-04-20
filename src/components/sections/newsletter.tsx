import React from 'react';
import Image from 'next/image';

  /**
   * NewsletterSection Component
   * Campus updates and announcements signup block for AttendX.
   */
const NewsletterSection: React.FC = () => {
  // Asset URLs from provided data
  const assets = {
    mailboxIllustration: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/images/images_8.png",
    leaf: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/svgs/leaf-12.svg",
    circle: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/svgs/circel-13.svg",
    plane: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/svgs/plane-14.svg"
  };

  return (
    <section 
      id="contact" 
      className="-mt-32 relative z-10 px-6 sm:px-8"
    >
      <div className="mx-auto max-w-7xl bg-[#3B82F6] rounded-[2rem] overflow-hidden">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-y-10 lg:gap-x-8">
          
          {/* Left Side: Illustrations (Hidden on mobile) */}
          <div className="hidden lg:block relative h-full min-h-[400px]">
            <div className="absolute inset-0 flex items-end justify-center pointer-events-none">
              {/* Main Mailbox/Plant Illustration */}
              <div className="relative w-[588px] h-[334px] translate-y-4">
                <Image
                  src={assets.mailboxIllustration}
                alt="AttendX announcement illustration"
                  width={588}
                  height={334}
                  className="object-contain"
                  priority
                />
                
                {/* Floating Leaf Decoration */}
                <div className="absolute -top-12 right-12 animate-bounce-slow">
                  <Image
                    src={assets.leaf}
                    alt="Floating leaf"
                    width={81}
                    height={81}
                  />
                </div>
                
                {/* Floating Circle Decoration */}
                <div className="absolute bottom-16 left-8">
                  <Image
                    src={assets.circle}
                    alt="Floating circle"
                    width={30}
                    height={30}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Right Side: Form Content */}
          <div className="p-8 md:p-12 lg:p-20 flex flex-col justify-center">
            <h3 className="text-4xl md:text-5xl font-semibold mb-4 text-white tracking-tight">
              Stay updated with campus alerts.
            </h3>
            
            <p className="text-base md:text-lg font-normal mb-8 text-blue-50/90 max-w-md leading-relaxed">
              Get important notices about attendance, events, internships, and learning updates in one place.
            </p>

            <form 
              className="flex w-full max-w-md"
              onSubmit={(e) => e.preventDefault()}
            >
              <input
                type="email"
                placeholder="Enter your email address"
                className="flex-1 py-4 px-6 text-sm text-[#001529] bg-white rounded-l-xl focus:outline-none placeholder:text-gray-400"
                required
              />
              <button
                type="submit"
                className="bg-[#001529] hover:bg-[#002a52] transition-colors duration-200 text-white flex items-center justify-center w-14 rounded-r-xl"
                aria-label="Subscribe"
              >
                <Image
                  src={assets.plane}
                  alt="Send"
                  width={20}
                  height={20}
                  className="shrink-0"
                />
              </button>
            </form>
          </div>
        </div>
      </div>
      
      {/* Spacer to handle the negative margin overlap with next section */}
      <div className="h-40 pointer-events-none"></div>

      <style jsx global>{`
        @keyframes bounce-slow {
          0%, 100% {
            transform: translateY(-5%);
            animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
          }
          50% {
            transform: translateY(0);
            animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
          }
        }
        .animate-bounce-slow {
          animation: bounce-slow 3s infinite;
        }
      `}</style>
    </section>
  );
};

export default NewsletterSection;
