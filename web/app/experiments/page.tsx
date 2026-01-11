"use client";

import { useState } from "react";

// Sample experiment data
const experiments = [
  {
    id: "exp_001",
    name: "Baseline LSTM",
    status: "completed",
    tm_score: 0.52,
    rmsd: 8.2,
    epochs: 50,
    date: "2026-01-10",
    duration: "2h 15m",
    params: { hidden_dim: 256, layers: 4, dropout: 0.2 },
  },
  {
    id: "exp_002",
    name: "Transformer v1",
    status: "completed",
    tm_score: 0.61,
    rmsd: 6.5,
    epochs: 100,
    date: "2026-01-11",
    duration: "5h 30m",
    params: { d_model: 512, heads: 8, layers: 6 },
  },
  {
    id: "exp_003",
    name: "Template-Based Hybrid",
    status: "running",
    tm_score: 0.67,
    rmsd: 5.5,
    epochs: 75,
    date: "2026-01-11",
    duration: "3h 45m",
    params: { template_search: true, refinement: "iterative" },
  },
  {
    id: "exp_004",
    name: "RhoFold+ Fine-tune",
    status: "queued",
    tm_score: null,
    rmsd: null,
    epochs: 0,
    date: "2026-01-11",
    duration: "-",
    params: { pretrained: "rhofold_v2", lr: 1e-5 },
  },
];

const statusColors: Record<string, { bg: string; text: string; dot: string }> = {
  completed: { bg: "bg-green-100", text: "text-green-800", dot: "bg-green-500" },
  running: { bg: "bg-blue-100", text: "text-blue-800", dot: "bg-blue-500" },
  queued: { bg: "bg-yellow-100", text: "text-yellow-800", dot: "bg-yellow-500" },
  failed: { bg: "bg-red-100", text: "text-red-800", dot: "bg-red-500" },
};

export default function ExperimentsPage() {
  const [selectedExperiment, setSelectedExperiment] = useState(experiments[2]);
  const [showNewExperiment, setShowNewExperiment] = useState(false);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            <span className="mr-3">🧪</span>
            Experiment Tracker
          </h1>
          <p className="text-gray-600">
            Manage and compare your model experiments
          </p>
        </div>
        <button
          onClick={() => setShowNewExperiment(true)}
          className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-lg font-medium hover:shadow-lg transform hover:scale-105 transition-all"
        >
          + New Experiment
        </button>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="stat-card">
          <div className="text-3xl font-bold text-gray-900">{experiments.length}</div>
          <div className="text-sm text-gray-600">Total Experiments</div>
        </div>
        <div className="stat-card">
          <div className="text-3xl font-bold text-green-600">
            {experiments.filter((e) => e.status === "completed").length}
          </div>
          <div className="text-sm text-gray-600">Completed</div>
        </div>
        <div className="stat-card">
          <div className="text-3xl font-bold text-blue-600">
            {experiments.filter((e) => e.status === "running").length}
          </div>
          <div className="text-sm text-gray-600">Running</div>
        </div>
        <div className="stat-card">
          <div className="text-3xl font-bold text-purple-600">0.670</div>
          <div className="text-sm text-gray-600">Best TM-Score</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Experiments List */}
        <div className="lg:col-span-2">
          <div className="glassmorphism rounded-xl overflow-hidden">
            <div className="p-4 border-b border-gray-200 bg-gray-50">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold text-gray-900">All Experiments</h3>
                <div className="flex gap-2">
                  <select className="px-3 py-1 border border-gray-300 rounded-lg text-sm">
                    <option>All Status</option>
                    <option>Completed</option>
                    <option>Running</option>
                    <option>Queued</option>
                  </select>
                  <select className="px-3 py-1 border border-gray-300 rounded-lg text-sm">
                    <option>Sort: Date</option>
                    <option>Sort: TM-Score</option>
                    <option>Sort: RMSD</option>
                  </select>
                </div>
              </div>
            </div>

            <div className="divide-y divide-gray-100">
              {experiments.map((exp) => (
                <div
                  key={exp.id}
                  onClick={() => setSelectedExperiment(exp)}
                  className={`p-4 cursor-pointer transition-all hover:bg-gray-50 ${
                    selectedExperiment.id === exp.id ? "bg-blue-50 border-l-4 border-blue-500" : ""
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <div className="flex items-center gap-2">
                        <h4 className="font-semibold text-gray-900">{exp.name}</h4>
                        <span
                          className={`px-2 py-0.5 text-xs rounded-full flex items-center gap-1 ${
                            statusColors[exp.status].bg
                          } ${statusColors[exp.status].text}`}
                        >
                          <span
                            className={`w-1.5 h-1.5 rounded-full ${statusColors[exp.status].dot} ${
                              exp.status === "running" ? "animate-pulse" : ""
                            }`}
                          />
                          {exp.status}
                        </span>
                      </div>
                      <div className="text-sm text-gray-500 mt-1">
                        {exp.date} | {exp.duration} | {exp.epochs} epochs
                      </div>
                    </div>
                    <div className="text-right">
                      {exp.tm_score !== null ? (
                        <>
                          <div className="text-lg font-bold text-gray-900">{exp.tm_score}</div>
                          <div className="text-xs text-gray-500">TM-Score</div>
                        </>
                      ) : (
                        <div className="text-sm text-gray-400">Pending</div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Experiment Details */}
        <div className="lg:col-span-1">
          <div className="glassmorphism rounded-xl p-6 sticky top-24">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Experiment Details</h3>

            <div className="space-y-4">
              <div>
                <div className="text-sm text-gray-500">Name</div>
                <div className="font-semibold text-gray-900">{selectedExperiment.name}</div>
              </div>

              <div>
                <div className="text-sm text-gray-500">Status</div>
                <span
                  className={`inline-flex items-center gap-1 px-2 py-1 text-sm rounded-full ${
                    statusColors[selectedExperiment.status].bg
                  } ${statusColors[selectedExperiment.status].text}`}
                >
                  <span
                    className={`w-2 h-2 rounded-full ${statusColors[selectedExperiment.status].dot} ${
                      selectedExperiment.status === "running" ? "animate-pulse" : ""
                    }`}
                  />
                  {selectedExperiment.status}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="p-3 bg-gray-50 rounded-lg">
                  <div className="text-sm text-gray-500">TM-Score</div>
                  <div className="text-xl font-bold text-gray-900">
                    {selectedExperiment.tm_score ?? "-"}
                  </div>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <div className="text-sm text-gray-500">RMSD</div>
                  <div className="text-xl font-bold text-gray-900">
                    {selectedExperiment.rmsd ? `${selectedExperiment.rmsd} A` : "-"}
                  </div>
                </div>
              </div>

              <div>
                <div className="text-sm text-gray-500 mb-2">Hyperparameters</div>
                <div className="bg-gray-900 rounded-lg p-3 overflow-auto">
                  <pre className="text-xs text-green-400">
                    {JSON.stringify(selectedExperiment.params, null, 2)}
                  </pre>
                </div>
              </div>

              <div className="flex gap-2">
                <button className="flex-1 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-all text-sm">
                  View Logs
                </button>
                <button className="flex-1 px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-all text-sm">
                  Compare
                </button>
              </div>

              {selectedExperiment.status === "running" && (
                <button className="w-full px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-all text-sm">
                  Stop Experiment
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* New Experiment Modal */}
      {showNewExperiment && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="glassmorphism rounded-2xl p-8 w-full max-w-lg mx-4">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">New Experiment</h3>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Experiment Name
                </label>
                <input
                  type="text"
                  placeholder="e.g., Transformer v2"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Model Type</label>
                <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                  <option>LSTM Baseline</option>
                  <option>Transformer</option>
                  <option>Template-Based</option>
                  <option>Hybrid Approach</option>
                  <option>Fine-tune Pretrained</option>
                </select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Epochs</label>
                  <input
                    type="number"
                    defaultValue={100}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Learning Rate
                  </label>
                  <input
                    type="text"
                    defaultValue="1e-4"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  onClick={() => setShowNewExperiment(false)}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-all"
                >
                  Cancel
                </button>
                <button
                  onClick={() => setShowNewExperiment(false)}
                  className="flex-1 px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-lg hover:shadow-lg transition-all"
                >
                  Start Experiment
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
