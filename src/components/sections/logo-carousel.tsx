"use client";

import React from "react";
import Image from "next/image";

const logos = [
  {
    src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/svgs/google-1.svg",
    alt: "Google",
    width: 150,
    height: 150,
  },
  {
    src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/images/images_2.png",
    alt: "Garnier",
    width: 150,
    height: 150,
  },
  {
    src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/images/images_3.png",
    alt: "Slack",
    width: 150,
    height: 150,
  },
  {
    src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/6cbd6322-6dcc-49f2-a60d-432431f809da-prep-master-v2-vercel-app/assets/images/images_4.png",
    alt: "Udemy",
    width: 150,
    height: 150,
  },
];

/**
 * LogoCarousel Component
 * An infinite horizontal scrolling carousel of partner logos.
 * Uses a CSS-based animation for smooth infinite scrolling.
 */
const LogoCarousel = () => {
  // Triple the logos to ensure seamless infinite scroll across all screen widths
  const extendedLogos = [...logos, ...logos, ...logos, ...logos];

  return (
    <section className="w-full bg-white text-center">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:max-w-7xl lg:px-8">
        <div className="py-14">
          <div className="relative overflow-hidden">
            {/* 
              Animation container:
              We use a CSS animation 'scroll' which translates the div horizontally.
              The 'animate-scroll' class needs to be defined in tailwind/globals or 
              inlined via a style tag for precise control over the keyframes.
            */}
            <div className="flex animate-infinite-scroll items-center gap-12 sm:gap-24">
              {extendedLogos.map((logo, index) => (
                <div
                  key={`${logo.alt}-${index}`}
                  className="flex-shrink-0 grayscale transition-all duration-300 hover:grayscale-0"
                >
                  <Image
                    src={logo.src}
                    alt={logo.alt}
                    width={logo.width}
                    height={logo.height}
                    className="h-10 w-auto object-contain sm:h-12 md:h-16"
                  />
                </div>
              ))}
            </div>

            {/* Gradient overlays for smooth fade edges */}
            <div className="pointer-events-none absolute inset-y-0 left-0 w-20 bg-gradient-to-r from-white to-transparent z-10" />
            <div className="pointer-events-none absolute inset-y-0 right-0 w-20 bg-gradient-to-l from-white to-transparent z-10" />
          </div>
        </div>
        <hr className="border-border opacity-50" />
      </div>

      <style jsx global>{`
        @keyframes infiniteScroll {
          from {
            transform: translateX(0);
          }
          to {
            transform: translateX(-50%);
          }
        }
        .animate-infinite-scroll {
          display: flex;
          width: max-content;
          animation: infiniteScroll 40s linear infinite;
        }
        .animate-infinite-scroll:hover {
          animation-play-state: paused;
        }
      `}</style>
    </section>
  );
};

export default LogoCarousel;