import React from "react";
import Image from "next/image";

/**
 * CollaborationSection
 * 
 * Clones the collaboration section which displays a stack of overlapping circular team member avatars
 * followed by a centered heading "Collaborate With Teams", a brief description, and a "Start Now" call-to-action button.
 * 
 * Theme: Light
 * Priority: Pixel perfect accuracy based on HTML structure and computed styles.
 */

const avatars = [
  {
    name: "John Doe",
    src: "https://images.unsplash.com/photo-1599566150163-29194dcaad36?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3387&q=80",
  },
  {
    name: "Robert Johnson",
    src: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8YXZhdGFyfGVufDB8fDB8fHww&auto=format&fit=crop&w=800&q=60",
  },
  {
    name: "Jane Smith",
    src: "https://images.unsplash.com/photo-1580489944761-15a19d654956?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8YXZhdGFyfGVufDB8fDB8fHww&auto=format&fit=crop&w=800&q=60",
  },
  {
    name: "Emily Davis",
    src: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGF2YXRhcnxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60",
  },
  {
    name: "Tyler Durden",
    src: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3540&q=80",
  },
  {
    name: "Dora",
    src: "https://images.unsplash.com/photo-1544725176-7c40e5a71c5e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3534&q=80",
  },
];

export default function CollaborationSection() {
  return (
    <section className="bg-background">
      <div className="mx-auto max-w-screen-xl px-6 py-8 sm:px-6 sm:py-12 lg:px-8 lg:py-12">
        <div className="flex flex-col items-center justify-center text-center">
          {/* Avatar Stack Container */}
          <div className="flex flex-row items-center justify-center my-10 w-full">
            {avatars.map((avatar, index) => (
              <div
                key={index}
                className="-mr-4 relative group"
                style={{ zIndex: avatars.length - index }}
              >
                <Image
                  alt={avatar.name}
                  width={100}
                  height={100}
                  className="object-cover !m-0 !p-0 object-top rounded-full h-14 w-14 border-2 border-white relative transition duration-500 group-hover:scale-105 group-hover:z-50 shadow-sm"
                  src={avatar.src}
                />
              </div>
            ))}
          </div>

          {/* Text Content */}
          <div className="lg:py-12 space-y-4 max-w-2xl">
            <h2 className="text-3xl font-bold sm:text-4xl text-foreground tracking-tight">
              Collaborate With Teams
            </h2>
            <p className="mt-4 text-muted-foreground text-lg leading-relaxed">
              Create beautiful flowcharts and diagrams and share effortlessly with your whole team!!
            </p>
            
            {/* CTA Button */}
            <div className="pt-4">
              <a
                href="/dashboard"
                className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 active:scale-95 transition-all bg-[#f97316] text-white hover:bg-[#f97316]/90 h-10 px-6 py-2 shadow-sm"
              >
                Start Now
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}