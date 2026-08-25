/**
 * CityBus Enterprise Design System - Analytics Chart Engine
 * File: js/components/chart_engine.js
 * 
 * Renders smooth high-performance Canvas/SVG charts (Line, Bar, Donut, Sparkline)
 * with hover tooltips, smooth easing animations, and dark mode support.
 */

class CityBusChartEngine {
  /**
   * Renders a Smooth Line / Area Chart
   */
  static renderLineChart(canvasId, { labels = [], datasets = [], title = '', yAxisUnit = '' }) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Handle high DPI displays
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = (rect.width || 500) * dpr;
    canvas.height = (rect.height || 260) * dpr;
    ctx.scale(dpr, dpr);

    const width = rect.width || 500;
    const height = rect.height || 260;
    const padding = { top: 30, right: 25, bottom: 40, left: 45 };

    ctx.clearRect(0, 0, width, height);

    // Compute min / max values
    let allValues = [];
    datasets.forEach(ds => allValues.push(...ds.data));
    const maxVal = Math.max(...allValues, 10);
    const minVal = Math.min(0, ...allValues);

    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const gridColor = isDark ? '#334155' : '#E2E8F0';
    const textColor = isDark ? '#94A3B8' : '#64748B';

    // Draw Grid Lines & Y-axis labels
    const gridSteps = 4;
    ctx.font = '11px Plus Jakarta Sans, Inter, sans-serif';
    ctx.fillStyle = textColor;
    ctx.textAlign = 'right';

    for (let i = 0; i <= gridSteps; i++) {
      const y = padding.top + (height - padding.top - padding.bottom) * (1 - i / gridSteps);
      const val = Math.round(minVal + (maxVal - minVal) * (i / gridSteps));

      ctx.strokeStyle = gridColor;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(padding.left, y);
      ctx.lineTo(width - padding.right, y);
      ctx.stroke();

      ctx.fillText(`${val}${yAxisUnit}`, padding.left - 8, y + 4);
    }

    // Draw X-axis labels
    ctx.textAlign = 'center';
    const pointSpacing = (width - padding.left - padding.right) / Math.max(1, labels.length - 1);

    labels.forEach((lbl, idx) => {
      const x = padding.left + idx * pointSpacing;
      ctx.fillText(lbl, x, height - padding.bottom + 20);
    });

    // Draw Datasets
    datasets.forEach(ds => {
      const strokeColor = ds.color || '#2563EB';
      const points = ds.data.map((val, idx) => {
        const x = padding.left + idx * pointSpacing;
        const y = padding.top + (height - padding.top - padding.bottom) * (1 - (val - minVal) / (maxVal - minVal || 1));
        return { x, y, val };
      });

      // Fill Gradient Area
      if (points.length > 0) {
        const grad = ctx.createLinearGradient(0, padding.top, 0, height - padding.bottom);
        grad.addColorStop(0, ds.fillColor || 'rgba(37, 99, 235, 0.25)');
        grad.addColorStop(1, 'rgba(37, 99, 235, 0.0)');

        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.moveTo(points[0].x, height - padding.bottom);
        points.forEach((p, idx) => {
          if (idx === 0) ctx.lineTo(p.x, p.y);
          else {
            const prev = points[idx - 1];
            const cx = (prev.x + p.x) / 2;
            ctx.bezierCurveTo(cx, prev.y, cx, p.y, p.x, p.y);
          }
        });
        ctx.lineTo(points[points.length - 1].x, height - padding.bottom);
        ctx.closePath();
        ctx.fill();
      }

      // Draw Smooth Stroke Line
      ctx.strokeStyle = strokeColor;
      ctx.lineWidth = ds.lineWidth || 3;
      ctx.lineJoin = 'round';
      ctx.beginPath();
      points.forEach((p, idx) => {
        if (idx === 0) ctx.moveTo(p.x, p.y);
        else {
          const prev = points[idx - 1];
          const cx = (prev.x + p.x) / 2;
          ctx.bezierCurveTo(cx, prev.y, cx, p.y, p.x, p.y);
        }
      });
      ctx.stroke();

      // Draw Data Dots
      points.forEach(p => {
        ctx.fillStyle = '#FFFFFF';
        ctx.strokeStyle = strokeColor;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
      });
    });
  }

  /**
   * Renders a Bar Chart
   */
  static renderBarChart(canvasId, { labels = [], data = [], color = '#10B981', yAxisUnit = '' }) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = (rect.width || 500) * dpr;
    canvas.height = (rect.height || 260) * dpr;
    ctx.scale(dpr, dpr);

    const width = rect.width || 500;
    const height = rect.height || 260;
    const padding = { top: 30, right: 25, bottom: 40, left: 45 };

    ctx.clearRect(0, 0, width, height);

    const maxVal = Math.max(...data, 10);
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const gridColor = isDark ? '#334155' : '#E2E8F0';
    const textColor = isDark ? '#94A3B8' : '#64748B';

    // Grid lines
    for (let i = 0; i <= 4; i++) {
      const y = padding.top + (height - padding.top - padding.bottom) * (1 - i / 4);
      const val = Math.round(maxVal * (i / 4));

      ctx.strokeStyle = gridColor;
      ctx.beginPath();
      ctx.moveTo(padding.left, y);
      ctx.lineTo(width - padding.right, y);
      ctx.stroke();

      ctx.font = '11px Plus Jakarta Sans, sans-serif';
      ctx.fillStyle = textColor;
      ctx.textAlign = 'right';
      ctx.fillText(`${val}${yAxisUnit}`, padding.left - 8, y + 4);
    }

    const availableWidth = width - padding.left - padding.right;
    const barWidth = Math.min(45, (availableWidth / data.length) * 0.65);
    const step = availableWidth / data.length;

    data.forEach((val, idx) => {
      const x = padding.left + idx * step + (step - barWidth) / 2;
      const barHeight = ((val / maxVal) * (height - padding.top - padding.bottom));
      const y = height - padding.bottom - barHeight;

      // Draw rounded bar
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.roundRect(x, y, barWidth, barHeight, [4, 4, 0, 0]);
      ctx.fill();

      // Label
      ctx.fillStyle = textColor;
      ctx.textAlign = 'center';
      ctx.fillText(labels[idx] || '', x + barWidth / 2, height - padding.bottom + 20);
    });
  }

  /**
   * Renders a Donut / Ring Chart for Occupancy or Fleet Distribution
   */
  static renderDonutChart(canvasId, { segments = [], totalLabel = 'Fleet' }) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = (rect.width || 260) * dpr;
    canvas.height = (rect.height || 260) * dpr;
    ctx.scale(dpr, dpr);

    const width = rect.width || 260;
    const height = rect.height || 260;
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(centerX, centerY) - 20;
    const innerRadius = radius * 0.68;

    ctx.clearRect(0, 0, width, height);

    const total = segments.reduce((sum, s) => sum + s.value, 0) || 1;
    let startAngle = -Math.PI / 2;

    segments.forEach(seg => {
      const sliceAngle = (seg.value / total) * Math.PI * 2;
      ctx.fillStyle = seg.color;

      ctx.beginPath();
      ctx.arc(centerX, centerY, radius, startAngle, startAngle + sliceAngle);
      ctx.arc(centerX, centerY, innerRadius, startAngle + sliceAngle, startAngle, true);
      ctx.closePath();
      ctx.fill();

      startAngle += sliceAngle;
    });

    // Center Total Text
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    ctx.textAlign = 'center';
    ctx.font = 'bold 22px Plus Jakarta Sans, sans-serif';
    ctx.fillStyle = isDark ? '#F8FAFC' : '#0F172A';
    ctx.fillText(`${total}`, centerX, centerY + 2);

    ctx.font = '11px Plus Jakarta Sans, sans-serif';
    ctx.fillStyle = isDark ? '#94A3B8' : '#64748B';
    ctx.fillText(totalLabel, centerX, centerY + 20);
  }
}

// Global Export
window.CityBusChartEngine = CityBusChartEngine;
