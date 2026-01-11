"use client";

import { useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  AreaChart,
  Area,
} from "recharts";

// Sample training data
const trainingData = [
  { epoch: 1, train_loss: 2.5, val_loss: 2.8, tm_score: 0.15, rmsd: 25.2 },
  { epoch: 5, train_loss: 1.8, val_loss: 2.1, tm_score: 0.28, rmsd: 18.5 },
  { epoch: 10, train_loss: 1.2, val_loss: 1.6, tm_score: 0.42, rmsd: 12.3 },
  { epoch: 15, train_loss: 0.9, val_loss: 1.3, tm_score: 0.51, rmsd: 9.8 },
  { epoch: 20, train_loss: 0.7, val_loss: 1.1, tm_score: 0.58, rmsd: 7.5 },
  { epoch: 25, train_loss: 0.5, val_loss: 0.9, tm_score: 0.63, rmsd: 6.2 },
  { epoch: 30, train_loss: 0.4, val_loss: 0.8, tm_score: 0.67, rmsd: 5.5 },
];

// Comparison data with Part 1 winners
const comparisonData = [
  { name: "john (1st)", tm_score: 0.671, rmsd: 4.2 },
  { name: "odat (2nd)", tm_score: 0.653, rmsd: 4.8 },
  { name: "Eigen (3rd)", tm_score: 0.615, rmsd: 5.5 },
  { name: "AlphaFold 3", tm_score: 0.52, rmsd: 7.8 },
  { name: "Your Model", tm_score: 0.67, rmsd: 5.5 },
];

// Radar chart data for model comparison
const radarData = [
  { metric: "TM-Score", yourModel: 85, winner: 100, alphafold: 78 },
  { metric: "RMSD", yourModel: 82, winner: 100, alphafold: 70 },
  { metric: "GDT-TS", yourModel: 78, winner: 95, alphafold: 72 },
  { metric: "lDDT", yourModel: 80, winner: 92, alphafold: 75 },
  { metric: "Clash Score", yourModel: 90, winner: 88, alphafold: 85 },
];

// Metrics by structure type
const structureTypeData = [
  { type: "tRNA", tm_score: 0.72, count: 15 },
  { type: "Riboswitch", tm_score: 0.65, count: 23 },
  { type: "Ribozyme", tm_score: 0.58, count: 12 },
  { type: "mRNA", tm_score: 0.61, count: 31 },
  { type: "snRNA", tm_score: 0.69, count: 8 },
];

export default function MetricsPage() {
  const [selectedMetric, setSelectedMetric] = useState<"loss" | "tm_score" | "rmsd">("tm_score");

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">
          <span className="mr-3">📊</span>
          Metrics Dashboard
        </h1>
        <p className="text-gray-600">
          Track model performance, compare with baselines, and analyze predictions
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="stat-card">
          <div className="flex items-center justify-between mb-2">
            <span className="text-3xl">🎯</span>
            <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">Best</span>
          </div>
          <div className="text-3xl font-bold text-gray-900">0.670</div>
          <div className="text-sm text-gray-600">TM-Score</div>
          <div className="mt-2 text-xs text-green-600">+0.05 from baseline</div>
        </div>

        <div className="stat-card">
          <div className="flex items-center justify-between mb-2">
            <span className="text-3xl">📏</span>
            <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">Latest</span>
          </div>
          <div className="text-3xl font-bold text-gray-900">5.5 A</div>
          <div className="text-sm text-gray-600">RMSD</div>
          <div className="mt-2 text-xs text-blue-600">Lower is better</div>
        </div>

        <div className="stat-card">
          <div className="flex items-center justify-between mb-2">
            <span className="text-3xl">📉</span>
          </div>
          <div className="text-3xl font-bold text-gray-900">0.80</div>
          <div className="text-sm text-gray-600">Validation Loss</div>
          <div className="mt-2 text-xs text-gray-500">Epoch 30</div>
        </div>

        <div className="stat-card">
          <div className="flex items-center justify-between mb-2">
            <span className="text-3xl">🏆</span>
          </div>
          <div className="text-3xl font-bold text-gray-900">#4</div>
          <div className="text-sm text-gray-600">vs Part 1 Winners</div>
          <div className="mt-2 text-xs text-purple-600">0.001 behind 1st</div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Training Progress */}
        <div className="glassmorphism rounded-xl p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Training Progress</h3>
            <div className="flex gap-2">
              {["loss", "tm_score", "rmsd"].map((metric) => (
                <button
                  key={metric}
                  onClick={() => setSelectedMetric(metric as typeof selectedMetric)}
                  className={`px-3 py-1 text-sm rounded-lg transition-all ${
                    selectedMetric === metric
                      ? "bg-blue-500 text-white"
                      : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                  }`}
                >
                  {metric === "loss" ? "Loss" : metric === "tm_score" ? "TM-Score" : "RMSD"}
                </button>
              ))}
            </div>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={trainingData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="epoch" stroke="#888" />
              <YAxis stroke="#888" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "rgba(255,255,255,0.9)",
                  backdropFilter: "blur(10px)",
                  border: "none",
                  borderRadius: "8px",
                  boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
                }}
              />
              <Legend />
              {selectedMetric === "loss" && (
                <>
                  <Line
                    type="monotone"
                    dataKey="train_loss"
                    stroke="#3B82F6"
                    strokeWidth={2}
                    dot={{ fill: "#3B82F6" }}
                    name="Train Loss"
                  />
                  <Line
                    type="monotone"
                    dataKey="val_loss"
                    stroke="#8B5CF6"
                    strokeWidth={2}
                    dot={{ fill: "#8B5CF6" }}
                    name="Val Loss"
                  />
                </>
              )}
              {selectedMetric === "tm_score" && (
                <Line
                  type="monotone"
                  dataKey="tm_score"
                  stroke="#10B981"
                  strokeWidth={2}
                  dot={{ fill: "#10B981" }}
                  name="TM-Score"
                />
              )}
              {selectedMetric === "rmsd" && (
                <Line
                  type="monotone"
                  dataKey="rmsd"
                  stroke="#F59E0B"
                  strokeWidth={2}
                  dot={{ fill: "#F59E0B" }}
                  name="RMSD"
                />
              )}
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Comparison with Part 1 Winners */}
        <div className="glassmorphism rounded-xl p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Comparison with Part 1 Winners</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={comparisonData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis type="number" domain={[0, 0.8]} stroke="#888" />
              <YAxis dataKey="name" type="category" stroke="#888" width={100} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "rgba(255,255,255,0.9)",
                  backdropFilter: "blur(10px)",
                  border: "none",
                  borderRadius: "8px",
                  boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
                }}
              />
              <Bar
                dataKey="tm_score"
                fill="#3B82F6"
                radius={[0, 4, 4, 0]}
                name="TM-Score"
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Radar Comparison */}
        <div className="glassmorphism rounded-xl p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Multi-Metric Comparison</h3>
          <ResponsiveContainer width="100%" height={300}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="#e0e0e0" />
              <PolarAngleAxis dataKey="metric" stroke="#888" />
              <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#888" />
              <Radar
                name="Your Model"
                dataKey="yourModel"
                stroke="#3B82F6"
                fill="#3B82F6"
                fillOpacity={0.3}
              />
              <Radar
                name="Part 1 Winner"
                dataKey="winner"
                stroke="#10B981"
                fill="#10B981"
                fillOpacity={0.3}
              />
              <Radar
                name="AlphaFold 3"
                dataKey="alphafold"
                stroke="#F59E0B"
                fill="#F59E0B"
                fillOpacity={0.3}
              />
              <Legend />
              <Tooltip />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        {/* Performance by Structure Type */}
        <div className="glassmorphism rounded-xl p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance by Structure Type</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={structureTypeData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="type" stroke="#888" />
              <YAxis stroke="#888" domain={[0, 1]} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "rgba(255,255,255,0.9)",
                  backdropFilter: "blur(10px)",
                  border: "none",
                  borderRadius: "8px",
                  boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
                }}
              />
              <Area
                type="monotone"
                dataKey="tm_score"
                stroke="#8B5CF6"
                fill="url(#colorGradient)"
                name="TM-Score"
              />
              <defs>
                <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8B5CF6" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#8B5CF6" stopOpacity={0.1} />
                </linearGradient>
              </defs>
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Metrics Explanation */}
      <div className="glassmorphism rounded-xl p-8">
        <h3 className="text-xl font-semibold text-gray-900 mb-6">Understanding the Metrics</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
            <div className="text-2xl mb-2">TM-Score</div>
            <div className="text-sm text-blue-900 mb-2">Range: 0 to 1</div>
            <p className="text-sm text-blue-800">
              Template Modeling score. Scale-independent measure of structural similarity.
              &gt;0.5 indicates same fold.
            </p>
          </div>

          <div className="p-4 bg-green-50 rounded-lg border border-green-200">
            <div className="text-2xl mb-2">RMSD</div>
            <div className="text-sm text-green-900 mb-2">Unit: Angstroms</div>
            <p className="text-sm text-green-800">
              Root Mean Square Deviation. Measures average distance between atoms.
              Lower is better.
            </p>
          </div>

          <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
            <div className="text-2xl mb-2">GDT-TS</div>
            <div className="text-sm text-purple-900 mb-2">Range: 0 to 100</div>
            <p className="text-sm text-purple-800">
              Global Distance Test - Total Score. Percentage of residues within
              distance cutoffs.
            </p>
          </div>

          <div className="p-4 bg-orange-50 rounded-lg border border-orange-200">
            <div className="text-2xl mb-2">lDDT</div>
            <div className="text-sm text-orange-900 mb-2">Range: 0 to 1</div>
            <p className="text-sm text-orange-800">
              Local Distance Difference Test. Measures local distance agreement
              within cutoff radius.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
