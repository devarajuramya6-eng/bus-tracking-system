/**
 * CityBus Enterprise Platform - Lightweight Canvas & SVG Chart Visualizer
 * File: js/components/chartVisualizer.js
 * 
 * Generates interactive SVG charts (line, bar, donut, sparkline) without external heavy libraries.
 */

class ChartVisualizer {
    static renderBarChart(containerId, data = [], { xKey = 'label', yKey = 'value', height = 240, barColor = '#2563EB' } = {}) {
        const container = document.getElementById(containerId);
        if (!container || data.length === 0) return;

        const maxVal = Math.max(...data.map(d => Number(d[yKey]) || 0), 1);
        const barWidth = 100 / data.length;

        let svg = `
            <svg viewBox="0 0 500 ${height}" class="citybus-svg-chart" style="width:100%; height:${height}px;">
                <defs>
                    <linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stop-color="${barColor}" stop-opacity="0.9"/>
                        <stop offset="100%" stop-color="${barColor}" stop-opacity="0.4"/>
                    </linearGradient>
                </defs>
                <!-- Grid lines -->
                <line x1="40" y1="20" x2="490" y2="20" stroke="var(--border-color, #e2e8f0)" stroke-dasharray="3,3"/>
                <line x1="40" y1="${height / 2}" x2="490" y2="${height / 2}" stroke="var(--border-color, #e2e8f0)" stroke-dasharray="3,3"/>
                <line x1="40" y1="${height - 30}" x2="490" y2="${height - 30}" stroke="var(--border-color, #e2e8f0)"/>
        `;

        const chartWidth = 450;
        const colWidth = chartWidth / data.length;
        const availableHeight = height - 60;

        data.forEach((item, idx) => {
            const val = Number(item[yKey]) || 0;
            const barH = (val / maxVal) * availableHeight;
            const x = 45 + idx * colWidth + (colWidth * 0.15);
            const y = (height - 30) - barH;
            const w = colWidth * 0.7;

            svg += `
                <rect x="${x}" y="${y}" width="${w}" height="${barH}" rx="4" fill="url(#barGrad)">
                    <title>${item[xKey]}: ${val}</title>
                </rect>
                <text x="${x + w / 2}" y="${height - 12}" text-anchor="middle" font-size="10" fill="var(--text-muted, #64748b)">${item[xKey]}</text>
                <text x="${x + w / 2}" y="${y - 4}" text-anchor="middle" font-size="10" font-weight="bold" fill="var(--text-color, #1e293b)">${val}</text>
            `;
        });

        svg += '</svg>';
        container.innerHTML = svg;
    }

    static renderDonutChart(containerId, data = [], { size = 180, holeRadius = 55 } = {}) {
        const container = document.getElementById(containerId);
        if (!container || data.length === 0) return;

        const total = data.reduce((sum, d) => sum + (Number(d.value) || 0), 0) || 1;
        const colors = ['#2563EB', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899'];
        let accumulatedAngle = 0;
        const center = size / 2;
        const radius = size / 2 - 10;

        let paths = '';
        data.forEach((slice, idx) => {
            const val = Number(slice.value) || 0;
            const angle = (val / total) * 360;
            const startAngle = accumulatedAngle;
            const endAngle = accumulatedAngle + angle;
            accumulatedAngle += angle;

            const x1 = center + radius * Math.cos(Math.PI * (startAngle - 90) / 180);
            const y1 = center + radius * Math.sin(Math.PI * (startAngle - 90) / 180);
            const x2 = center + radius * Math.cos(Math.PI * (endAngle - 90) / 180);
            const y2 = center + radius * Math.sin(Math.PI * (endAngle - 90) / 180);

            const largeArc = angle > 180 ? 1 : 0;
            const color = slice.color || colors[idx % colors.length];

            paths += `
                <path d="M ${center} ${center} L ${x1} ${y1} A ${radius} ${radius} 0 ${largeArc} 1 ${x2} ${y2} Z" fill="${color}">
                    <title>${slice.label}: ${val} (${Math.round((val/total)*100)}%)</title>
                </path>
            `;
        });

        // Donut inner hole
        paths += `<circle cx="${center}" cy="${center}" r="${holeRadius}" fill="var(--card-bg, #ffffff)"/>`;

        const svg = `
            <svg viewBox="0 0 ${size} ${size}" style="width:${size}px; height:${size}px; display:block; margin:auto;">
                ${paths}
            </svg>
            <div class="donut-legend mt-2 d-flex flex-wrap justify-content-center gap-2">
                ${data.map((d, i) => `
                    <span class="legend-item badge" style="background:${d.color || colors[i % colors.length]}15; color:${d.color || colors[i % colors.length]}; border:1px solid ${d.color || colors[i % colors.length]}">
                        ${d.label}: ${d.value}
                    </span>
                `).join('')}
            </div>
        `;
        container.innerHTML = svg;
    }
}

// Global Export
window.ChartVisualizer = ChartVisualizer;
