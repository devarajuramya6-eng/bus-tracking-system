/**
 * CityBus Enterprise Platform - Transit Analytics & Charts Center
 * File: js/admin/analytics_center.js
 */

document.addEventListener('DOMContentLoaded', async () => {
  if (!window.CityBusChartEngine) return;

  // 1. Weekly Ridership Line Chart
  window.CityBusChartEngine.renderLineChart('analytics-ridership-chart', {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        data: [14200, 15800, 16100, 15400, 17200, 18900, 13400],
        color: '#2563EB',
        fillColor: 'rgba(37, 99, 235, 0.22)'
      }
    ],
    yAxisUnit: ''
  });

  // 2. On-Time Performance (OTP) Line Chart
  window.CityBusChartEngine.renderLineChart('analytics-otp-chart', {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        data: [95, 94, 93, 96, 92, 91, 97],
        color: '#10B981',
        fillColor: 'rgba(16, 185, 129, 0.2)'
      }
    ],
    yAxisUnit: '%'
  });

  // 3. Fleet Distribution Donut Chart
  window.CityBusChartEngine.renderDonutChart('analytics-fleet-donut', {
    segments: [
      { value: 42, color: '#10B981', label: 'On Route' },
      { value: 5, color: '#F59E0B', label: 'Delayed' },
      { value: 3, color: '#EF4444', label: 'Offline / Depot' }
    ],
    totalLabel: 'Active Fleet'
  });
});
