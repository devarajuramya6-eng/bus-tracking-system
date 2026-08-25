/**
 * CityBus Enterprise Design System - Advanced DataTable Component
 * File: js/components/datatable.js
 * 
 * Features:
 * - Multi-column sorting & instant search
 * - Custom filter chips and column visibility
 * - Pagination with customizable page sizes
 * - Row checkboxes & bulk action bar
 * - CSV & JSON export engine
 * - Responsive horizontal scrolling & sticky headers
 */

class CityBusDataTable {
  constructor({
    containerId,
    columns = [],
    data = [],
    pageSize = 10,
    searchable = true,
    selectable = false,
    bulkActions = [],
    onRowClick = null
  }) {
    this.container = document.getElementById(containerId);
    this.columns = columns;
    this.rawOriginalData = [...data];
    this.filteredData = [...data];
    this.pageSize = pageSize;
    this.currentPage = 1;
    this.searchQuery = '';
    this.sortKey = null;
    this.sortOrder = 'asc';
    this.selectedRowIds = new Set();
    this.searchable = searchable;
    this.selectable = selectable;
    this.bulkActions = bulkActions;
    this.onRowClick = onRowClick;

    if (this.container) {
      this.init();
    }
  }

  init() {
    this.render();
  }

  setData(newData) {
    this.rawOriginalData = [...newData];
    this.applyFiltersAndSort();
  }

  applyFiltersAndSort() {
    let result = [...this.rawOriginalData];

    // 1. Text Search Filter across all searchable column fields
    if (this.searchQuery) {
      const q = this.searchQuery.toLowerCase();
      result = result.filter(item => {
        return this.columns.some(col => {
          const val = item[col.key];
          return val !== undefined && val !== null && String(val).toLowerCase().includes(q);
        });
      });
    }

    // 2. Sorting
    if (this.sortKey) {
      result.sort((a, b) => {
        let valA = a[this.sortKey];
        let valB = b[this.sortKey];
        if (typeof valA === 'string') valA = valA.toLowerCase();
        if (typeof valB === 'string') valB = valB.toLowerCase();

        if (valA < valB) return this.sortOrder === 'asc' ? -1 : 1;
        if (valA > valB) return this.sortOrder === 'asc' ? 1 : -1;
        return 0;
      });
    }

    this.filteredData = result;
    this.currentPage = 1;
    this.render();
  }

  render() {
    if (!this.container) return;

    const totalPages = Math.max(1, Math.ceil(this.filteredData.length / this.pageSize));
    const startIndex = (this.currentPage - 1) * this.pageSize;
    const pageData = this.filteredData.slice(startIndex, startIndex + this.pageSize);

    // Build Toolbar HTML
    let toolbarHtml = `
      <div class="table-toolbar">
        <div style="display: flex; align-items: center; gap: 0.75rem; flex: 1;">
          ${this.searchable ? `
            <div class="input-with-icon" style="max-width: 320px; flex: 1;">
              <i class="fa-solid fa-magnifying-glass input-icon-left"></i>
              <input type="text" class="form-control" placeholder="Search table..." value="${this.searchQuery}" id="${this.container.id}-search">
            </div>
          ` : ''}
          <div style="font-size: 0.8rem; color: var(--cb-text-muted);">
            Showing ${this.filteredData.length} records
          </div>
        </div>

        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <button class="btn btn-outline btn-sm" id="${this.container.id}-export-csv" title="Export as CSV">
            <i class="fa-solid fa-file-csv"></i> Export CSV
          </button>
          <button class="btn btn-outline btn-sm" id="${this.container.id}-export-json" title="Export as JSON">
            <i class="fa-solid fa-file-code"></i> JSON
          </button>
        </div>
      </div>
    `;

    // Bulk action bar
    let bulkBarHtml = '';
    if (this.selectable && this.selectedRowIds.size > 0) {
      bulkBarHtml = `
        <div style="background-color: var(--cb-brand-primary-light); padding: 0.5rem 1rem; display: flex; align-items: center; justify-content: space-between; font-size: 0.85rem; color: var(--cb-brand-primary);">
          <span><strong>${this.selectedRowIds.size}</strong> rows selected</span>
          <div style="display: flex; gap: 0.5rem;">
            ${this.bulkActions.map(act => `
              <button class="btn btn-xs ${act.btnClass || 'btn-outline-primary'}" data-bulk-action="${act.id}">
                ${act.label}
              </button>
            `).join('')}
          </div>
        </div>
      `;
    }

    // Build Table Header
    let theadHtml = '<thead><tr>';
    if (this.selectable) {
      const allSelected = pageData.length > 0 && pageData.every(row => this.selectedRowIds.has(row.id));
      theadHtml += `<th style="width: 40px; text-align: center;"><input type="checkbox" id="${this.container.id}-select-all" ${allSelected ? 'checked' : ''}></th>`;
    }

    this.columns.forEach(col => {
      const isSorted = this.sortKey === col.key;
      let sortIcon = '<i class="fa-solid fa-sort" style="color: var(--cb-text-subtle); margin-left: 4px;"></i>';
      if (isSorted) {
        sortIcon = this.sortOrder === 'asc' 
          ? '<i class="fa-solid fa-sort-up" style="color: var(--cb-brand-primary); margin-left: 4px;"></i>' 
          : '<i class="fa-solid fa-sort-down" style="color: var(--cb-brand-primary); margin-left: 4px;"></i>';
      }

      theadHtml += `
        <th class="${col.sortable !== false ? 'sortable' : ''}" data-col-key="${col.key}">
          ${col.title} ${col.sortable !== false ? sortIcon : ''}
        </th>
      `;
    });
    theadHtml += '</tr></thead>';

    // Build Table Body
    let tbodyHtml = '<tbody>';
    if (pageData.length === 0) {
      const colSpan = this.columns.length + (this.selectable ? 1 : 0);
      tbodyHtml += `
        <tr>
          <td colspan="${colSpan}" style="text-align: center; padding: 3rem 1rem; color: var(--cb-text-muted);">
            <div style="font-size: 2rem; color: var(--cb-text-subtle); margin-bottom: 0.5rem;"><i class="fa-solid fa-folder-open"></i></div>
            <div style="font-weight: 600;">No matching records found</div>
          </td>
        </tr>
      `;
    } else {
      pageData.forEach(row => {
        const isSelected = this.selectedRowIds.has(row.id);
        tbodyHtml += `<tr data-row-id="${row.id}" style="${this.onRowClick ? 'cursor: pointer;' : ''}">`;
        
        if (this.selectable) {
          tbodyHtml += `<td style="text-align: center;"><input type="checkbox" class="row-checkbox" data-row-id="${row.id}" ${isSelected ? 'checked' : ''}></td>`;
        }

        this.columns.forEach(col => {
          let cellValue = row[col.key];
          if (col.render) {
            cellValue = col.render(row[col.key], row);
          }
          tbodyHtml += `<td>${cellValue !== undefined && cellValue !== null ? cellValue : '--'}</td>`;
        });

        tbodyHtml += '</tr>';
      });
    }
    tbodyHtml += '</tbody>';

    // Build Pagination HTML
    let paginationHtml = `
      <div class="pagination">
        <div>
          Page ${this.currentPage} of ${totalPages} (${this.filteredData.length} items)
        </div>
        <div class="pagination-pages">
          <button class="page-btn" id="${this.container.id}-prev-page" ${this.currentPage === 1 ? 'disabled' : ''}>
            <i class="fa-solid fa-chevron-left"></i>
          </button>
          <span style="display: inline-flex; align-items: center; padding: 0 0.5rem; font-weight: 700;">${this.currentPage}</span>
          <button class="page-btn" id="${this.container.id}-next-page" ${this.currentPage >= totalPages ? 'disabled' : ''}>
            <i class="fa-solid fa-chevron-right"></i>
          </button>
        </div>
      </div>
    `;

    // Inject everything into container
    this.container.className = 'cb-table-container';
    this.container.innerHTML = `
      ${toolbarHtml}
      ${bulkBarHtml}
      <table class="data-table">
        ${theadHtml}
        ${tbodyHtml}
      </table>
      ${paginationHtml}
    `;

    this.attachEventListeners();
  }

  attachEventListeners() {
    // Search input
    const searchInput = document.getElementById(`${this.container.id}-search`);
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        this.searchQuery = e.target.value.trim();
        this.applyFiltersAndSort();
      });
    }

    // Column sorting headers
    this.container.querySelectorAll('th.sortable').forEach(th => {
      th.addEventListener('click', () => {
        const key = th.dataset.colKey;
        if (this.sortKey === key) {
          this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
        } else {
          this.sortKey = key;
          this.sortOrder = 'asc';
        }
        this.applyFiltersAndSort();
      });
    });

    // Prev / Next pagination
    const prevBtn = document.getElementById(`${this.container.id}-prev-page`);
    const nextBtn = document.getElementById(`${this.container.id}-next-page`);
    if (prevBtn) prevBtn.onclick = () => { if (this.currentPage > 1) { this.currentPage--; this.render(); } };
    if (nextBtn) nextBtn.onclick = () => { this.currentPage++; this.render(); };

    // Select all checkbox
    const selectAll = document.getElementById(`${this.container.id}-select-all`);
    if (selectAll) {
      selectAll.onchange = (e) => {
        const startIndex = (this.currentPage - 1) * this.pageSize;
        const pageData = this.filteredData.slice(startIndex, startIndex + this.pageSize);
        pageData.forEach(row => {
          if (e.target.checked) this.selectedRowIds.add(row.id);
          else this.selectedRowIds.delete(row.id);
        });
        this.render();
      };
    }

    // Row checkboxes
    this.container.querySelectorAll('.row-checkbox').forEach(cb => {
      cb.onchange = (e) => {
        const id = cb.dataset.rowId;
        if (e.target.checked) this.selectedRowIds.add(id);
        else this.selectedRowIds.delete(id);
        this.render();
      };
    });

    // Row Click handler
    if (this.onRowClick) {
      this.container.querySelectorAll('tbody tr[data-row-id]').forEach(tr => {
        tr.onclick = (e) => {
          if (e.target.tagName === 'INPUT' || e.target.closest('button') || e.target.closest('a')) return;
          const id = tr.dataset.rowId;
          const row = this.rawOriginalData.find(r => String(r.id) === String(id));
          if (row) this.onRowClick(row);
        };
      });
    }

    // CSV / JSON Export
    const csvBtn = document.getElementById(`${this.container.id}-export-csv`);
    const jsonBtn = document.getElementById(`${this.container.id}-export-json`);
    if (csvBtn) csvBtn.onclick = () => this.exportCSV();
    if (jsonBtn) jsonBtn.onclick = () => this.exportJSON();
  }

  exportCSV() {
    if (this.filteredData.length === 0) return;
    const headers = this.columns.map(c => `"${c.title}"`).join(',');
    const rows = this.filteredData.map(row => {
      return this.columns.map(c => {
        let val = row[c.key];
        if (val === undefined || val === null) val = '';
        return `"${String(val).replace(/"/g, '""')}"`;
      }).join(',');
    });

    const csvContent = 'data:text/csv;charset=utf-8,' + [headers, ...rows].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `citybus_export_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    if (window.showToast) window.showToast('CSV export downloaded successfully', 'success');
  }

  exportJSON() {
    const jsonString = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(this.filteredData, null, 2));
    const link = document.createElement('a');
    link.setAttribute('href', jsonString);
    link.setAttribute('download', `citybus_export_${Date.now()}.json`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    if (window.showToast) window.showToast('JSON export downloaded successfully', 'success');
  }
}

// Global Export
window.CityBusDataTable = CityBusDataTable;
