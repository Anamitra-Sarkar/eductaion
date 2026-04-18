import React from 'react';
import { AlertCircle, Timer, BarChart3, Globe2 } from 'lucide-react';

const IntelligenceDashboard = () => {
  const metrics = [
    {
      title: "Actionable Insights / Alerts",
      description: "Documents with high-priority content (compliance deadlines, approvals required, safety issues).",
      icon: <AlertCircle className="w-8 h-8" />,
      color: "cyan",
      gradient: "from-cyan-500 to-cyan-600",
      bgGradient: "from-white via-cyan-50/30 to-white",
      textClass: "text-cyan-600 group-hover:text-cyan-700",
      glowColor: "from-cyan-500/5",
      isMetric: false
    },
    {
      title: "Avg Processing Time",
      metric: "2.3s",
      subtext: "98.7% faster",
      icon: <Timer className="w-8 h-8" />,
      color: "green",
      gradient: "from-green-500 to-green-600",
      bgGradient: "from-white via-green-50/30 to-white",
      textClass: "text-green-600 group-hover:text-green-700",
      glowColor: "from-green-500/5",
      badgeClass: "text-green-600 bg-green-50 border-green-200",
      isMetric: true
    },
    {
      title: "Efficiency & Performance Metrics",
      description: "Throughput: Documents processed per hour/day",
      badge: "8 departments",
      icon: <BarChart3 className="w-8 h-8" />,
      color: "orange",
      gradient: "from-orange-500 to-orange-600",
      bgGradient: "from-white via-orange-50/30 to-white",
      textClass: "text-orange-600 group-hover:text-orange-700",
      glowColor: "from-orange-500/5",
      badgeClass: "text-blue-600 bg-blue-50 border-blue-200",
      isMetric: false
    },
    {
      title: "Languages Supported",
      metric: "50+",
      subtext: "EN, ML, HI",
      icon: <Globe2 className="w-8 h-8" />,
      color: "purple",
      gradient: "from-purple-500 to-purple-600",
      bgGradient: "from-white via-purple-50/30 to-white",
      textClass: "text-purple-600 group-hover:text-purple-700",
      glowColor: "from-purple-500/5",
      badgeClass: "text-slate-600 bg-slate-100 border-slate-200",
      isMetric: true
    }
  ];

  return (
    <section id="dashboard" className="py-20 px-6 bg-gradient-to-br from-slate-50 via-white to-cyan-50/50 relative overflow-hidden">
      {/* Decorative Blur Background Elements */}
      <div className="absolute inset-0 opacity-30 pointer-events-none">
        <div className="absolute top-10 right-10 w-32 h-32 bg-cyan-200 rounded-full blur-3xl"></div>
        <div className="absolute bottom-10 left-10 w-24 h-24 bg-blue-200 rounded-full blur-2xl"></div>
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        {/* Header Container */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center border text-[12px] font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 bg-gradient-to-r from-cyan-100 to-blue-100 text-cyan-700 border-cyan-200 mb-6 px-6 py-3 rounded-full shadow-lg">
            <BarChart3 className="mr-2 w-4 h-4" />
            Live Performance Metrics
          </div>
          <h2 className="text-[36px] font-bold text-slate-900 mb-6 tracking-tight">
            Enterprise Intelligence Dashboard
          </h2>
          <p className="text-[20px] text-slate-600 max-w-3xl mx-auto leading-relaxed">
            Real-time performance metrics across all organisations with enterprise-grade monitoring and analytics
          </p>
        </div>

        {/* Dashboard Grid */}
        <div className="grid md:grid-cols-4 gap-8">
          {metrics.map((item, idx) => (
            <div 
              key={idx}
              className={`rounded-[24px] text-card-foreground border-0 shadow-xl hover:shadow-2xl transition-all duration-500 hover:scale-105 bg-gradient-to-br ${item.bgGradient} group overflow-hidden relative border border-slate-100`}
            >
              {/* Hover Glow Effect */}
              <div className={`absolute inset-0 bg-gradient-to-br ${item.glowColor} to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500`}></div>
              
              <div className="p-8 text-center relative z-10 flex flex-col h-full items-center">
                {/* Icon Container with Glassmorphism / Shadow */}
                <div className="flex items-center justify-center mb-6">
                  <div className={`bg-gradient-to-br ${item.gradient} text-white rounded-[24px] p-5 shadow-xl group-hover:shadow-2xl transition-all duration-300 group-hover:scale-110 flex items-center justify-center`}>
                    {item.icon}
                  </div>
                </div>

                {/* Metric/Title Logic */}
                {item.isMetric ? (
                  <>
                    <div className={`text-[40px] font-bold ${item.textClass} mb-3 tracking-tight transition-colors duration-300`}>
                      {item.metric}
                    </div>
                    <div className="text-[14px] font-semibold text-slate-700 mb-4 h-auto min-h-[20px]">
                      {item.title}
                    </div>
                    {item.subtext && (
                      <div className={`text-[12px] px-4 py-2 rounded-full border ${item.badgeClass} font-medium`}>
                        {item.subtext}
                      </div>
                    )}
                  </>
                ) : (
                  <>
                    <div className={`text-[24px] font-bold leading-tight ${item.textClass} mb-3 tracking-tight transition-colors duration-300`}>
                      {item.title}
                    </div>
                    <div className="text-[14px] font-semibold text-slate-700 mb-4 leading-snug">
                      {item.description}
                    </div>
                    {item.badge && (
                      <div className={`text-[12px] px-4 py-2 rounded-full border ${item.badgeClass} inline-block font-medium`}>
                        {item.badge}
                      </div>
                    )}
                  </>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default IntelligenceDashboard;