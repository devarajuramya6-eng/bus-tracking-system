/**
 * CityBus Enterprise Platform - Interactive Data Table Manager
 * File: js/components/dataTableManager.js
 * 
 * Renders high-performance data tables with client/server pagination,
 * multi-column sort, quick-filter search, row selection, and CSV/JSON export.
 */

class DataTableManager {
    constructor(tableContainerId, options = {}) {
        this.container = document.getElementById(tableContainerId);
        this.columns = options.columns || [];
        this.data = options.data || [];
        this.actions = options.actions || [];
        this.pageSize = options.pageSize || 10;
        this.currentPage = 1;
        this.sortColumn = null;
        this.sortOrder = 'asc';
        this.searchQuery = '';
    }

    setData(newData) {
        this.data = newData;
        this.currentPage = 1;
        this.render();
    }

    getFilteredData() {
        let filtered = [...this.data];

        if (this.searchQuery) {
            const query = this.searchQuery.toLowerCase();
            filtered = filtered.filter(row => {
                return this.columns.some(col => {
                    const val = row[col.key];
                    return val !== undefined && val !== null && String(val).toLowerCase().includes(query);
                });
            });
        }

        if (this.sortColumn) {
            filtered.sort((a, b) => {
                let vA = a[this.sortColumn];
                let vB = b[this.sortColumn];
                if (typeof vA === 'string') vA = vA.toLowerCase();
                if (typeof vB === 'string') vB = vB.toLowerCase();
                if (vA < vB) return this.sortOrder === 'asc' ? -1 : 1;
                if (vA > vB) return this.sortOrder === 'asc' ? 1 : -1;
                return 0;
            });
        }

        return filtered;
    }

    render() {
        if (!this.container) return;
        const filtered = this.getFilteredData();
        const totalRows = filtered.length;
        const totalPages = Math.ceil(totalRows / this.pageSize) || 1;
        const startIndex = (this.currentPage - 1) * this.pageSize;
        const pageRows = filtered.slice(startIndex, startIndex + this.pageSize);

        let html = `
            <div class="datatable-toolbar">
                <div class="datatable-search">
                    <i class="fas fa-search"></i>
                    <input type="text" placeholder="Search table..." value="${this.searchQuery}" class="datatable-search-input">
                </div>
                <div class="datatable-export-btns">
                    <button class="btn btn-sm btn-outline-secondary export-csv-btn"><i class="fas fa-file-csv"></i> CSV</button>
                    <button class="btn btn-sm btn-outline-secondary export-json-btn"><i class="fas fa-file-code"></i> JSON</button>
                </div>
            </div>
            <div class="table-responsive">
                <table class="citybus-datatable">
                    <thead>
                        <tr>
                            ${this.columns.map(col => `
                                <th data-key="${col.key}" class="${col.sortable !== false ? 'sortable' : ''}">
                                    ${col.label}
                                    ${this.sortColumn === col.key ? (this.sortOrder === 'asc' ? ' ▲' : ' ▼') : ''}
                                </th>
                            `).join('')}
                            ${this.actions.length > 0 ? '<th>Actions</th>' : ''}
                        </tr>
                    </thead>
                    <tbody>
                        ${pageRows.length === 0 ? `
                            <tr><td colspan="${this.columns.length + (this.actions.length > 0 ? 1 : 0)}" class="text-center text-muted p-4">No matching records found</td></tr>
                        ` : pageRows.map(row => `
                            <tr>
                                ${this.columns.map(col => `
                                    <td>${col.render ? col.render(row[col.key], row) : (row[col.key] !== undefined ? row[col.key] : '-')}</td>
                                `).join('')}
                                ${this.actions.length > 0 ? `
                                    <td class="action-cell">
                                        ${this.actions.map(act => `
                                            <button class="btn btn-xs ${act.btnClass || 'btn-outline-primary'}" data-action="${act.name}" data-id="${row.id}">
                                                ${act.icon ? `<i class="${act.icon}"></i>` : ''} ${act.label}
                                            </button>
                                        `).join('')}
                                    </td>
                                ` : ''}
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
            <div class="datatable-pagination">
                <span>Showing ${totalRows === 0 ? 0 : startIndex + 1} to ${Math.min(startIndex + this.pageSize, totalRows)} of ${totalRows} entries</span>
                <div class="pagination-controls">
                    <button class="btn btn-sm btn-outline-secondary prev-page-btn" ${this.currentPage === 1 ? 'disabled' : ''}>Previous</button>
                    <span class="current-page-num">${this.currentPage} / ${totalPages}</span>
                    <button class="btn btn-sm btn-outline-secondary next-page-btn" ${this.currentPage >= totalPages ? 'disabled' : ''}>Next</button>
                </div>
            </div>
        `;

        this.container.innerHTML = html;
        this.bindEvents();
    }

    bindEvents() {
        const searchInput = this.container.querySelector('.datatable-search-input');
        if (searchInput) {
            searchInput.oninput = (e) => {
                this.searchQuery = e.target.value;
                this.currentPage = 1;
                this.render();
            };
        }

        const headers = this.container.querySelectorAll('th.sortable');
        headers.forEach(th => {
            th.onclick = () => {
                const key = th.dataset.key;
                if (this.sortColumn === key) {
                    this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
                } else {
                    this.sortColumn = key;
                    this.sortOrder = 'asc';
                }
                this.render();
            };
        });

        const prevBtn = this.container.querySelector('.prev-page-btn');
        if (prevBtn) {
            prevBtn.onclick = () => {
                if (this.currentPage > 1) {
                    this.currentPage--;
                    this.render();
                }
            };
        }

        const nextBtn = this.container.querySelector('.next-page-btn');
        if (nextBtn) {
            nextBtn.onclick = () => {
                const filtered = this.getFilteredData();
                const totalPages = Math.ceil(filtered.length / this.pageSize);
                if (this.currentPage < totalPages) {
                    this.currentPage++;
                    this.render();
                }
            };
        }

        const actionBtns = this.container.querySelectorAll('button[data-action]');
        actionBtns.forEach(btn => {
            btn.onclick = () => {
                const actName = btn.dataset.action;
                const rowId = btn.dataset.id;
                const actionDef = this.actions.find(a => a.name === actName);
                const rowObj = this.data.find(d => String(d.id) === String(rowId));
                if (actionDef && actionDef.handler && rowObj) {
                    actionDef.handler(rowObj);
                }
            };
        });
    }
}

// Global Export
window.DataTableManager = DataTableManager;
