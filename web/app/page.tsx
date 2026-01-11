export default function Home() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <div className="inline-flex items-center px-4 py-2 rounded-full bg-purple-100 text-purple-800 text-sm font-medium mb-4">
          <span className="mr-2">🏆</span>
          Kaggle Competition | $75,000 Prize Pool
        </div>
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          Stanford RNA 3D Folding
          <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            {" "}Part 2
          </span>
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Predict the 3D structure of RNA molecules from their sequences.
          Track experiments, visualize structures, and compete for the top score.
        </p>
        <div className="mt-8 flex justify-center gap-4">
          <a
            href="/visualizer"
            className="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-medium hover:shadow-lg transform hover:scale-105 transition-all"
          >
            Launch Visualizer
          </a>
          <a
            href="/experiments"
            className="px-8 py-3 glassmorphism rounded-lg font-medium hover:shadow-lg transform hover:scale-105 transition-all"
          >
            View Experiments
          </a>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        <div className="stat-card">
          <div className="flex items-center justify-between mb-2">
            <span className="text-3xl">📊</span>
            <span className="text-sm text-gray-500">Dataset</span>
          </div>
          <div className="text-3xl font-bold text-gray-900">23.4 GB</div>
          <div className="text-sm text-gray-600 mt-1">Competition Data</div>
        </div>

        <div className="stat-card">
          <div className="flex items-center justify-between mb-2">
            <span className="text-3xl">🧪</span>
            <span className="text-sm text-gray-500">Models</span>
          </div>
          <div className="text-3xl font-bold text-gray-900">0</div>
          <div className="text-sm text-gray-600 mt-1">Trained Models</div>
        </div>

        <div className="stat-card">
          <div className="flex items-center justify-between mb-2">
            <span className="text-3xl">🎯</span>
            <span className="text-sm text-gray-500">Best Score</span>
          </div>
          <div className="text-3xl font-bold text-gray-900">-</div>
          <div className="text-sm text-gray-600 mt-1">TM-Score</div>
        </div>

        <div className="stat-card">
          <div className="flex items-center justify-between mb-2">
            <span className="text-3xl">⏰</span>
            <span className="text-sm text-gray-500">Deadline</span>
          </div>
          <div className="text-2xl font-bold text-gray-900">Mar 18</div>
          <div className="text-sm text-gray-600 mt-1">2026</div>
        </div>
      </div>

      {/* Part 1 Winners Section */}
      <div className="glassmorphism rounded-2xl p-8 mb-12">
        <div className="flex items-center mb-6">
          <span className="text-3xl mr-3">🏆</span>
          <h2 className="text-2xl font-bold text-gray-900">Part 1 Winners Insights</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 rounded-xl p-6 border border-yellow-200">
            <div className="text-4xl font-bold text-yellow-900 mb-2">john</div>
            <div className="text-sm text-yellow-700 mb-4">1st Place</div>
            <div className="text-2xl font-bold text-yellow-900">0.671</div>
            <div className="text-sm text-yellow-700">TM-Score</div>
            <div className="mt-4 text-sm text-yellow-800">
              Template-based approach
            </div>
          </div>

          <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-6 border border-gray-200">
            <div className="text-4xl font-bold text-gray-900 mb-2">odat</div>
            <div className="text-sm text-gray-700 mb-4">2nd Place</div>
            <div className="text-2xl font-bold text-gray-900">0.653</div>
            <div className="text-sm text-gray-700">TM-Score</div>
            <div className="mt-4 text-sm text-gray-800">
              Template-based approach
            </div>
          </div>

          <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-xl p-6 border border-orange-200">
            <div className="text-4xl font-bold text-orange-900 mb-2">Eigen</div>
            <div className="text-sm text-orange-700 mb-4">3rd Place</div>
            <div className="text-2xl font-bold text-orange-900">0.615</div>
            <div className="text-sm text-orange-700">TM-Score</div>
            <div className="mt-4 text-sm text-orange-800">
              Template-based approach
            </div>
          </div>
        </div>

        <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <p className="text-blue-900 font-medium">
            Key Insight: All top 3 teams used template-based modeling WITHOUT deep learning
            and outperformed AlphaFold 3
          </p>
        </div>
      </div>

      {/* Approach Comparison */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        <div className="glassmorphism rounded-2xl p-8">
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <span className="text-2xl mr-2">🔍</span>
            Template-Based Approach
          </h3>
          <ul className="space-y-3">
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              <span className="text-gray-700">Template discovery pipeline</span>
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              <span className="text-gray-700">No deep learning required</span>
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              <span className="text-gray-700">Outperformed AlphaFold 3</span>
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              <span className="text-gray-700">Human-competitive results</span>
            </li>
          </ul>
        </div>

        <div className="glassmorphism rounded-2xl p-8">
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <span className="text-2xl mr-2">🤖</span>
            Deep Learning Approach
          </h3>
          <ul className="space-y-3">
            <li className="flex items-start">
              <span className="text-blue-500 mr-2">•</span>
              <span className="text-gray-700">RhoFold+ (23.7M sequences)</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-500 mr-2">•</span>
              <span className="text-gray-700">AlphaFold 3 (DeepMind)</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-500 mr-2">•</span>
              <span className="text-gray-700">RoseTTAFoldNA</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-500 mr-2">•</span>
              <span className="text-gray-700">RNA foundation models</span>
            </li>
          </ul>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="glassmorphism rounded-2xl p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="p-4 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:shadow-lg transform hover:scale-105 transition-all">
            <div className="text-3xl mb-2">🧬</div>
            <div className="font-medium">Visualize Structure</div>
            <div className="text-sm opacity-80">3D molecular viewer</div>
          </button>

          <button className="p-4 bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-lg hover:shadow-lg transform hover:scale-105 transition-all">
            <div className="text-3xl mb-2">📊</div>
            <div className="font-medium">Train Model</div>
            <div className="text-sm opacity-80">Start new experiment</div>
          </button>

          <button className="p-4 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg hover:shadow-lg transform hover:scale-105 transition-all">
            <div className="text-3xl mb-2">📈</div>
            <div className="font-medium">View Metrics</div>
            <div className="text-sm opacity-80">TM-score, RMSD, GDT-TS</div>
          </button>
        </div>
      </div>
    </div>
  );
}
