import React from "react";
import { 
  Upload, 
  Cpu, 
  GitPullRequest, 
  BarChart3, 
  Archive,
  MousePointer2 
} from "lucide-react";

const EnterpriseAutomationProcess = () => {
  const steps = [
    {
      icon: <Upload className="w-6 h-6" />,
      title: "Document Ingestion",
      description: "Automated multi-source document capture with intelligent preprocessing"
    },
    {
      icon: <Cpu className="w-6 h-6" />,
      title: "AI Processing",
      description: "Advanced NLP analysis with context-aware summarization"
    },
    {
      icon: <GitPullRequest className="w-6 h-6" />,
      title: "Smart Distribution",
      description: "Intelligent routing to relevant departments with priority classification"
    },
    {
      icon: <BarChart3 className="w-6 h-6" />,
      title: "Executive Dashboard",
      description: "Real-time insights with comprehensive analytics and reporting"
    },
    {
      icon: <Archive className="w-6 h-6" />,
      title: "Knowledge Archive",
      description: "Secure archival with compliance logging and audit trails"
    }
  ];

  return (
    <section id="workflow" className="py-20 px-6 bg-white overflow-hidden relative">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <div className="inline-flex items-center rounded-full border border-slate-200 bg-slate-50 text-slate-700 text-xs font-semibold px-4 py-2 mb-6 shadow-sm">
            <MousePointer2 className="w-3.5 h-3.5 mr-2 text-cyan-600" />
            Intelligent Workflow
          </div>
          <h2 className="text-4xl font-bold text-slate-900 mb-6 tracking-tight">
            Enterprise Automation Process
          </h2>
          <p className="text-xl text-slate-600 max-w-3xl mx-auto leading-relaxed">
            Streamlined 5-stage intelligent workflow transforming operational chaos into strategic clarity
          </p>
        </div>

        {/* Workflow Steps Grid */}
        <div className="relative grid grid-cols-1 md:grid-cols-5 gap-8 mb-20">
          {/* Connecting Line (Desktop) */}
          <div className="hidden md:block absolute top-[44px] left-[10%] right-[10%] h-0.5 bg-slate-100 -z-0" />
          
          {steps.map((step, idx) => (
            <div key={idx} className="relative z-10 flex flex-col items-center group">
              {/* Step Number Badge */}
              <div className="absolute -top-1 right-[25%] md:right-[20%] lg:right-[30%] bg-emerald-500 text-white w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold shadow-md border-2 border-white">
                {idx + 1}
              </div>
              
              {/* Icon Container */}
              <div className="w-20 h-20 bg-cyan-500 text-white rounded-2xl flex items-center justify-center shadow-lg group-hover:scale-110 group-hover:shadow-2xl transition-all duration-300 mb-6">
                {step.icon}
              </div>

              {/* Text Content */}
              <div className="text-center px-2">
                <h3 className="text-lg font-bold text-slate-900 mb-2 leading-tight">
                  {step.title}
                </h3>
                <p className="text-sm text-slate-500 leading-relaxed">
                  {step.description}
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* Average Processing Card */}
        <div className="max-w-2xl mx-auto">
          <div className="bg-[#f0f9ff]/50 backdrop-blur-md rounded-3xl p-8 border border-white shadow-xl text-center relative overflow-hidden group">
            {/* Subtle internal gradient pulse */}
            <div className="absolute inset-0 bg-gradient-to-tr from-cyan-50/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700" />
            
            <div className="relative z-10 flex flex-col items-center">
              <div className="flex items-center gap-2 mb-4">
                <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
                <span className="text-sm font-semibold text-slate-700 tracking-wide uppercase">
                  Average Processing Time
                </span>
              </div>
              
              <div className="text-5xl md:text-6xl font-black text-cyan-600 mb-3 tracking-tighter">
                2.3 seconds
              </div>
              
              <div className="text-slate-500 font-medium">
                From upload to intelligent distribution
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default EnterpriseAutomationProcess;