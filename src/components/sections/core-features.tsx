import React from 'react';
import { 
  FileText, 
  Cpu, 
  Search, 
  Bell, 
  ShieldCheck, 
  Archive,
  Sparkles 
} from 'lucide-react';

const features = [
  {
    title: "Multi-Source Ingestion",
    description: "Seamless integration with emails, PDFs, scanned documents, and SharePoint with real-time synchronization capabilities",
    icon: <FileText className="w-6 h-6" />,
    iconBg: "bg-cyan-500",
  },
  {
    title: "AI Summarization Engine",
    description: "Advanced role-based, multilingual document processing with 99.7% accuracy and contextual understanding",
    icon: <Cpu className="w-6 h-6" />,
    iconBg: "bg-green-500",
  },
  {
    title: "Intelligent Search",
    description: "Elasticsearch-powered semantic search with advanced traceability and content discovery algorithms",
    icon: <Search className="w-6 h-6" />,
    iconBg: "bg-blue-600",
  },
  {
    title: "Compliance Monitoring",
    description: "Proactive safety notices and automated regulatory deadline management with intelligent alerting",
    icon: <Bell className="w-6 h-6" />,
    iconBg: "bg-[#f97316]", // Orange 500
  },
  {
    title: "Enterprise Security",
    description: "Military-grade role-based access control with comprehensive audit logging and end-to-end encryption",
    icon: <ShieldCheck className="w-6 h-6" />,
    iconBg: "bg-[#a855f7]", // Purple 500
  },
  {
    title: "Knowledge Management",
    description: "Intelligent archival system with automated knowledge preservation and institutional memory retention",
    icon: <Archive className="w-6 h-6" />,
    iconBg: "bg-[#4f46e5]", // Indigo 600
  }
];

export default function CoreFeatures() {
  return (
    <section id="features" className="py-20 px-6 bg-white overflow-hidden">
      <div className="max-w-7xl mx-auto">
        {/* Header Section */}
        <div className="text-center mb-16 relative">
          <div className="inline-flex items-center rounded-full border border-cyan-200 bg-cyan-50 text-cyan-700 text-xs font-semibold px-4 py-2 mb-6">
            <Sparkles className="w-3.5 h-3.5 mr-2" />
            Enterprise Features
          </div>
          
          <h2 className="text-[2.25rem] font-bold text-[#0f172a] mb-6 tracking-tight leading-[1.2]">
            Comprehensive AI-Powered Platform
          </h2>
          
          <p className="text-[1.25rem] text-[#475569] max-w-3xl mx-auto leading-relaxed font-medium">
            Enterprise-grade document intelligence designed specifically for metro operations with military-grade security and scalable performance architecture
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div 
              key={index}
              className="group p-8 bg-white rounded-[1.5rem] border border-slate-100 shadow-[0_10px_15px_-3px_rgba(0,0,0,0.05)] hover:shadow-[0_20px_25px_-5px_rgba(0,0,0,0.1)] transition-all duration-300 hover:-translate-y-1"
            >
              {/* Icon Container */}
              <div className={`w-14 h-14 ${feature.iconBg} text-white rounded-[1rem] flex items-center justify-center mb-6 shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                {feature.icon}
              </div>

              {/* Text Content */}
              <h3 className="text-[1.5rem] font-semibold text-[#0f172a] mb-3">
                {feature.title}
              </h3>
              
              <p className="text-[1rem] text-[#475569] leading-[1.6]">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}