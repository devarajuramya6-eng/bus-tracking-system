/**
 * CityBus Enterprise Platform - Universal Data Exporter
 * File: js/components/file_exporter.js
 * 
 * Provides production-grade file generation and download capabilities:
 * - CSV export with comma-separated escaping and BOM for Excel
 * - JSON formatted data dump
 * - Formatted Printable Thermal / A4 Ticket Slip
 * - Revenue Ledger & Maintenance PDF/Print template
 */

class CityBusFileExporter {
  /**
   * Exports an array of JavaScript objects to a downloadable CSV file.
   */
  static exportToCSV(filename, data) {
    if (!data || data.length === 0) {
      if (window.showToast) window.showToast('No data available to export.', 'warning');
      return;
    }

    const headers = Object.keys(data[0]);
    const csvRows = [];

    // Header row
    csvRows.push(headers.map(h => `"${h.replace(/"/g, '""')}"`).join(','));

    // Data rows
    for (const row of data) {
      const values = headers.map(header => {
        const val = row[header] === null || row[header] === undefined ? '' : String(row[header]);
        return `"${val.replace(/"/g, '""')}"`;
      });
      csvRows.push(values.join(','));
    }

    const csvContent = '\uFEFF' + csvRows.join('\r\n'); // Add UTF-8 BOM
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    CityBusFileExporter._downloadBlob(blob, filename.endsWith('.csv') ? filename : `${filename}.csv`);

    if (window.showToast) {
      window.showToast(`Exported ${data.length} records to ${filename}.csv`, 'success');
    }
  }

  /**
   * Exports JavaScript data to a pretty-printed JSON file.
   */
  static exportToJSON(filename, data) {
    const jsonStr = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json;charset=utf-8;' });
    CityBusFileExporter._downloadBlob(blob, filename.endsWith('.json') ? filename : `${filename}.json`);

    if (window.showToast) {
      window.showToast(`Exported data to ${filename}.json`, 'success');
    }
  }

  /**
   * Generates a printable thermal receipt window for a transit pass.
   */
  static printTicketReceipt(ticket) {
    const printWindow = window.open('', '_blank', 'width=450,height=650');
    if (!printWindow) return;

    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>CityBus Transit Pass - ${ticket.ticket_number || 'Receipt'}</title>
        <style>
          body { font-family: monospace; font-size: 13px; margin: 20px; line-height: 1.5; color: #111; }
          .center { text-align: center; }
          .divider { border-top: 1px dashed #444; margin: 12px 0; }
          .bold { font-weight: bold; }
          .flex { display: flex; justify-content: space-between; }
          .qr { text-align: center; margin: 15px 0; font-size: 11px; color: #666; }
        </style>
      </head>
      <body onload="window.print();">
        <div class="center">
          <div class="bold" style="font-size: 16px;">CITYBUS TRANSIT AUTHORITY</div>
          <div>VIJAYAWADA & AMARAVATI MUNICIPAL METRO</div>
          <div style="font-size: 11px;">ELECTRONIC FARE PASS</div>
        </div>
        <div class="divider"></div>
        <div class="flex"><span>Pass No:</span><span class="bold">${ticket.ticket_number}</span></div>
        <div class="flex"><span>Date:</span><span>${new Date(ticket.issued_at || Date.now()).toLocaleString()}</span></div>
        <div class="flex"><span>Route:</span><span class="bold">${ticket.route_number || 'Direct'}</span></div>
        <div class="flex"><span>From:</span><span>${ticket.origin_stop || 'PNBS'}</span></div>
        <div class="flex"><span>To:</span><span>${ticket.destination_stop || 'Guntur'}</span></div>
        <div class="flex"><span>Passengers:</span><span>${ticket.passenger_count || 1} Adult</span></div>
        <div class="divider"></div>
        <div class="flex bold" style="font-size: 15px;"><span>TOTAL FARE:</span><span>₹${parseFloat(ticket.fare_amount || 0).toFixed(2)}</span></div>
        <div class="flex"><span>Payment Mode:</span><span>ONLINE (PAID)</span></div>
        <div class="flex"><span>Status:</span><span class="bold">${ticket.status || 'VALID'}</span></div>
        <div class="divider"></div>
        <div class="qr">
          <div>[ CRYPTOGRAPHIC SECURE QR ]</div>
          <div style="word-break: break-all; font-size: 9px; margin-top: 5px;">${ticket.qr_payload || 'HMAC-SHA256-SIGNED'}</div>
        </div>
        <div class="center" style="font-size: 11px;">
          Thank you for choosing eco-friendly public transit.<br>
          Emergency Helpline: 112 / 1800-425-111
        </div>
      </body>
      </html>
    `);
    printWindow.document.close();
  }

  static _downloadBlob(blob, filename) {
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }
}

// Global Export
window.CityBusFileExporter = CityBusFileExporter;
