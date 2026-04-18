import React from 'react';
import { 
  Zap, 
  Users, 
  ShieldCheck, 
  BookOpen, 
  DollarSign, 
  BarChart3, 
  Rocket 
} from 'lucide-react';

const TransformativeImpact = () => {
  const benefits = [
    {
      icon: <Zap className="w-6 h-6" />,
      title: "Lightning-Fast Decisions",
      description: "Reduce operational downtime by 95% with instant AI-powered insights and real-time decision support"
    },
    {
      icon: <Users className="w-6 h-6" />,
      title: "Unified Collaboration",
      description: "Break down departmental silos with seamless information sharing and cross-functional workflows"
    },
    {
      icon: <ShieldCheck className="w-6 h-6" />,
      title: "Regulatory Excellence",
      description: "Never miss critical compliance deadlines with automated monitoring and intelligent alerts"
    },
    {
      icon: <BookOpen className="w-6 h-6" />,
      title: "Knowledge Preservation",
      description: "Accelerate onboarding and training with intelligent knowledge management and instant access"
    },
    {
      icon: <DollarSign className="w-6 h-6" />,
      title: "Cost Optimization",
      description: "Eliminate redundant processes and achieve significant operational cost savings through automation"
    },
    {
      icon: <BarChart3 className="w-6 h-6" />,
      title: "Operational Excellence",
      description: "Drive data-driven decision making with comprehensive analytics and performance insights"
    }
  ];

  return (
    <section className="bg-[#0891b2] py-20 px-6 relative overflow-hidden">
      {/* Visual background accents */}
      <div className="absolute inset-0 opacity-10 pointer-events-none">
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-white rounded-full blur-[120px] -translate-y-1/2 translate-x-1/4"></div>
        <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-cyan-300 rounded-full blur-[120px] translate-y-1/2 -translate-x-1/4"></div>
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        <div className="flex flex-col items-center text-center mb-16">
          {/* Floating Navigation Pill */}
          <div className="inline-flex items-center gap-2 px-4 py-2 mb-8 bg-white/10 backdrop-blur-md border border-white/20 rounded-full shadow-lg">
            <Rocket className="w-4 h-4 text-white" />
            <span className="text-xs font-semibold uppercase tracking-wider text-white">Operational Impact</span>
          </div>

          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-6 tracking-tight max-w-4xl text-balance">
            Transformative Impact for the modern organisations
          </h2>
          
          <p className="text-lg md:text-xl text-cyan-50/90 max-w-3xl leading-relaxed">
            Measurable improvements across all operational dimensions with enterprise-grade performance
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 lg:gap-12">
          {benefits.map((benefit, index) => (
            <div 
              key={index} 
              className="flex flex-col items-center text-center group cursor-default"
            >
              {/* Icon Container */}
              <div className="mb-6 w-16 h-16 bg-white/15 backdrop-blur-sm rounded-2xl flex items-center justify-center text-white border border-white/20 shadow-xl group-hover:scale-110 group-hover:bg-white group-hover:text-[#0891b2] transition-all duration-300">
                {benefit.icon}
              </div>

              {/* Text Content */}
              <h3 className="text-xl font-bold text-white mb-4 tracking-tight">
                {benefit.title}
              </h3>
              
              <p className="text-white/80 leading-relaxed text-sm md:text-base max-w-[280px]">
                {benefit.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default TransformativeImpact;