import React from 'react';
import Image from 'next/image';

/**
 * FeaturesCreateSection Component
 * 
 * A pixel-perfect clone of the "Start Creating Now" feature section.
 * Features a two-column grid layout:
 * - Left column: Title, descriptive text, and primary orange CTA button.
 * - Right column: Framed interface image showcasing a flowchart/schematic.
 */
const FeaturesCreateSection: React.FC = () => {
  // Asset URL from the provided section-specific assets
  const featureImage = "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-aivis-liart-vercel-app/assets/images/images_12.png";

  return (
    <section className="bg-white">
      <div className="mx-auto max-w-screen-xl px-6 py-8 sm:px-6 sm:py-12 lg:px-8 lg:py-16">
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-2 lg:gap-16 items-center">
          {/* Right Column (Image) - Ordered last on desktop using lg:order-last */}
          <div className="relative h-64 overflow-hidden rounded-xl sm:h-80 lg:order-last lg:h-[450px]">
            <Image
              src={featureImage}
              alt="Aivis Flowchart Interface"
              width={2500}
              height={1677}
              className="absolute inset-0 h-full w-full object-cover rounded-xl shadow-lg border border-gray-100"
              priority
            />
          </div>

          {/* Left Column (Content) */}
          <div className="lg:py-24 space-y-6">
            <h2 className="text-3xl font-bold tracking-tight text-[#111827] sm:text-4xl lg:text-[2.25rem] leading-tight">
              Start Creating Now
            </h2>
            
            <p className="text-[#6b7280] text-base leading-relaxed max-w-xl">
              With best in class tools and features, you can start creating flowcharts and diagrams in minutes. 
              Also powered with a rich text editor to create beautiful documentation. Save and Share your thoughts!
            </p>

            <div className="pt-2">
              <a
                href="/dashboard"
                className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-all active:scale-95 bg-[#f97316] text-white hover:bg-[#f97316]/90 h-10 px-6 py-2 shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#f97316] focus-visible:ring-offset-2"
              >
                Start Now
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default FeaturesCreateSection;