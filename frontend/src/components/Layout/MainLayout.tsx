import React from 'react';
import DataSophLogo from '../DataSophLogo';

interface MainLayoutProps {
  children: React.ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Professional Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            {/* Logo and Professional Branding */}
            <div className="flex items-center space-x-6">
              <DataSophLogo variant="compact" />
              
              {/* Professional Credentials */}
              <div className="hidden md:flex items-center space-x-4 pl-6 border-l border-gray-200">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-sm font-medium text-gray-700">
                    PhD-Level Analysis Ready
                  </span>
                </div>
                
                <div className="flex items-center space-x-3 text-xs text-gray-500">
                  <span className="flex items-center space-x-1">
                    <svg className="w-3 h-3 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    <span>ASA Compliant</span>
                  </span>
                  
                  <span className="flex items-center space-x-1">
                    <svg className="w-3 h-3 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    <span>Production Ready</span>
                  </span>
                  
                  <span className="flex items-center space-x-1">
                    <svg className="w-3 h-3 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    <span>Enterprise Grade</span>
                  </span>
                </div>
              </div>
            </div>

            {/* Professional Actions */}
            <div className="flex items-center space-x-4">
              {/* Expertise Level Indicator */}
              <div className="hidden sm:flex items-center space-x-2">
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                  <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                  <div className="w-2 h-2 bg-blue-300 rounded-full"></div>
                  <div className="w-2 h-2 bg-blue-200 rounded-full"></div>
                </div>
                <span className="text-xs font-medium text-gray-600">
                  Expert Level
                </span>
              </div>

              {/* Quick Actions */}
              <div className="flex items-center space-x-2">
                <button className="px-3 py-1.5 text-xs font-medium text-blue-600 bg-blue-50 rounded-md hover:bg-blue-100 transition-colors">
                  Upload Data
                </button>
                <button className="px-3 py-1.5 text-xs font-medium text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors">
                  Help
                </button>
              </div>
            </div>
          </div>

          {/* Professional Capabilities Bar */}
          <div className="hidden lg:block pb-4">
            <div className="flex items-center justify-between text-xs">
              <div className="flex items-center space-x-6">
                <div className="flex items-center space-x-2">
                  <div className="w-1.5 h-1.5 bg-green-500 rounded-full"></div>
                  <span className="text-gray-600 font-medium">Statistical Testing</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-1.5 h-1.5 bg-green-500 rounded-full"></div>
                  <span className="text-gray-600 font-medium">Machine Learning</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-1.5 h-1.5 bg-green-500 rounded-full"></div>
                  <span className="text-gray-600 font-medium">Business Intelligence</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-1.5 h-1.5 bg-green-500 rounded-full"></div>
                  <span className="text-gray-600 font-medium">Executive Reporting</span>
                </div>
              </div>
              
              <div className="flex items-center space-x-2 text-gray-500">
                <span>15+ Years Fortune 500 Experience</span>
                <span>•</span>
                <span>PhD Statistical Standards</span>
                <span>•</span>
                <span>Production Deployment Ready</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1">
        {children}
      </main>

      {/* Professional Footer */}
      <footer className="bg-white border-t border-gray-200 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            {/* Professional Standards */}
            <div className="flex flex-col space-y-2">
              <div className="flex items-center space-x-4 text-xs text-gray-600">
                <span className="flex items-center space-x-1">
                  <svg className="w-3 h-3 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span>ASA Statistical Guidelines</span>
                </span>
                
                <span className="flex items-center space-x-1">
                  <svg className="w-3 h-3 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span>MLOps Best Practices</span>
                </span>
                
                <span className="flex items-center space-x-1">
                  <svg className="w-3 h-3 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span>Enterprise Security</span>
                </span>
              </div>
              
              <div className="text-xs text-gray-500">
                Professional data science analysis with Fortune 500 standards and academic rigor
              </div>
            </div>

            {/* Expertise Indicators */}
            <div className="flex items-center space-x-6 text-xs text-gray-600">
              <div className="flex flex-col items-center space-y-1">
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                  <span className="font-medium">Statistical Rigor</span>
                </div>
                <span className="text-gray-500">PhD Level</span>
              </div>
              
              <div className="flex flex-col items-center space-y-1">
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                  <span className="font-medium">Business Focus</span>
                </div>
                <span className="text-gray-500">Fortune 500</span>
              </div>
              
              <div className="flex flex-col items-center space-y-1">
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-purple-600 rounded-full"></div>
                  <span className="font-medium">Communication</span>
                </div>
                <span className="text-gray-500">Executive Ready</span>
              </div>
            </div>
          </div>

          {/* Copyright and Professional Statement */}
          <div className="mt-4 pt-4 border-t border-gray-200 flex flex-col sm:flex-row justify-between items-center text-xs text-gray-500">
            <div>
              © 2025 Datasoph. Professional data science analysis with academic rigor.
            </div>
            <div className="mt-2 sm:mt-0">
              Think like a consultant • Communicate like a professor • Deliver like a Fortune 500 team
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default MainLayout; 