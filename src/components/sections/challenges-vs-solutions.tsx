import React from 'react';
import { AlertCircle, Bot, Zap, Users, ShieldAlert, FileText, Send, Database, Globe } from 'lucide-react';

const ChallengesVsSolutions = () => {
  const challenges = [
    {
      title: "Information Latency",
      description: "Critical updates delayed across departments",
      impact: "Impact: 4-6 hour delays",
      icon: <Zap className="w-5 h-5" />,
    },
    {
      title: "Department Silos",
      description: "Isolated workflows creating inefficiencies",
      impact: "Impact: Duplicated efforts",
      icon: <Users className="w-5 h-5" />,
    },
    {
      title: "Compliance Risks",
      description: "Manual tracking of regulatory requirements",
      impact: "Impact: Safety concerns",
      icon: <ShieldAlert className="w-5 h-5" />,
    },
    {
      title: "Manual Processing",
      description: "Time-intensive document handling",
      impact: "Impact: 80% manual effort",
      icon: <FileText className="w-5 h-5" />,
    },
  ];

  const solutions = [
    {
      title: "AI Summarization",
      description: "Intelligent, role-based document processing",
      result: "Result: 95% time reduction",
      icon: <Bot className="w-5 h-5" />,
    },
    {
      title: "Smart Routing",
      description: "Automated department distribution",
      result: "Result: Real-time delivery",
      icon: <Send className="w-5 h-5" />,
    },
    {
      title: "Knowledge Management",
      description: "Centralized, searchable repository",
      result: "Result: Universal access",
      icon: <Database className="w-5 h-5" />,
    },
    {
      title: "Multilingual AI",
      description: "English, Malayalam, Hindi processing",
      result: "Result: Inclusive operation",
      icon: <Globe className="w-5 h-5" />,
    },
  ];

  return (
    <section className="py-20 px-6 bg-slate-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center rounded-full border border-slate-200 bg-slate-100 px-4 py-2 text-xs font-semibold text-slate-700 mb-6 transition-colors shadow-sm">
            <AlertCircle className="w-4 h-4 mr-2" />
            Operational Transformation
          </div>
          <h2 className="text-4xl font-bold text-slate-900 mb-6 tracking-tight">
            From Operational Challenges to AI Excellence
          </h2>
          <p className="text-xl text-slate-600 max-w-3xl mx-auto leading-relaxed">
            Discover how intelligent automation transforms traditional metro operations into a streamlined, efficient enterprise
          </p>
        </div>

        {/* Comparison Grid */}
        <div className="grid lg:grid-cols-2 gap-12">
          {/* Challenges Column */}
          <div className="rounded-3xl border-0 shadow-xl overflow-hidden bg-gradient-to-br from-[#FEF2F2] to-[#FEE2E2]/50 group transition-all duration-500 hover:shadow-2xl">
            <div className="p-8 pb-4">
              <div className="flex items-center gap-4 mb-6">
                <div className="bg-[#EF4444] text-white p-3 rounded-2xl shadow-lg ring-4 ring-red-500/10">
                  <AlertCircle className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-[#B91C1C] tracking-tight">
                    Current Operational Challenges
                  </h3>
                </div>
              </div>
              <p className="text-[#DC2626] text-lg font-medium opacity-90">
                Critical operational bottlenecks impacting metro efficiency and safety protocols
              </p>
            </div>

            <div className="p-8 pt-2 space-y-4">
              {challenges.map((item, idx) => (
                <div 
                  key={idx} 
                  className="flex items-start gap-5 p-5 bg-white/60 hover:bg-white/80 rounded-2xl border border-red-100 transition-all duration-300 transform hover:-translate-y-1"
                >
                  <div className="bg-red-50 p-3 rounded-xl text-red-500 shadow-sm">
                    {item.icon}
                  </div>
                  <div className="flex-1">
                    <h4 className="font-bold text-red-900 mb-1 text-base">{item.title}</h4>
                    <p className="text-red-700 text-sm mb-3 font-medium opacity-80">{item.description}</p>
                    <div className="inline-block px-3 py-1 bg-red-50 text-red-600 text-xs font-bold rounded-full border border-red-100">
                      {item.impact}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Solutions Column */}
          <div className="rounded-3xl border-0 shadow-xl overflow-hidden bg-gradient-to-br from-[#ECFEFF] to-[#CFFAFE]/50 group transition-all duration-500 hover:shadow-2xl">
            <div className="p-8 pb-4">
              <div className="flex items-center gap-4 mb-6">
                <div className="bg-[#06B6D4] text-white p-3 rounded-2xl shadow-lg ring-4 ring-cyan-500/10">
                  <Bot className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-[#0E7490] tracking-tight">
                    AI-Powered Solutions
                  </h3>
                </div>
              </div>
              <p className="text-[#0891B2] text-lg font-medium opacity-90">
                Intelligent automation transforming metro operations with enterprise-grade AI
              </p>
            </div>

            <div className="p-8 pt-2 space-y-4">
              {solutions.map((item, idx) => (
                <div 
                  key={idx} 
                  className="flex items-start gap-5 p-5 bg-white/60 hover:bg-white/80 rounded-2xl border border-cyan-100 transition-all duration-300 transform hover:-translate-y-1"
                >
                  <div className="bg-cyan-50 p-3 rounded-xl text-cyan-500 shadow-sm">
                    {item.icon}
                  </div>
                  <div className="flex-1">
                    <h4 className="font-bold text-cyan-900 mb-1 text-base">{item.title}</h4>
                    <p className="text-cyan-700 text-sm mb-3 font-medium opacity-80">{item.description}</p>
                    <div className="inline-block px-3 py-1 bg-cyan-50 text-cyan-600 text-xs font-bold rounded-full border border-cyan-100">
                      {item.result}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ChallengesVsSolutions;