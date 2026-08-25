class AdvancedDataTable extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.data = [];
        this.columns = [];
        this.sortColumn = null;
        this.sortDirection = 'asc';
        this.currentPage = 1;
        this.rowsPerPage = 10;
        this.searchQuery = '';
    }

    connectedCallback() {
        this.render();
        this.setupListeners();
    }

    set config(config) {
        this.columns = config.columns || [];
        this.data = config.data || [];
        this.render();
    }

    sortData(column) {
        if (this.sortColumn === column) {
            this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            this.sortColumn = column;
            this.sortDirection = 'asc';
        }

        this.data.sort((a, b) => {
            let valA = a[column];
            let valB = b[column];

            if (typeof valA === 'string') valA = valA.toLowerCase();
            if (typeof valB === 'string') valB = valB.toLowerCase();

            if (valA < valB) return this.sortDirection === 'asc' ? -1 : 1;
            if (valA > valB) return this.sortDirection === 'asc' ? 1 : -1;
            return 0;
        });

        this.render();
    }

    get filteredAndPaginatedData() {
        let filtered = this.data;
        if (this.searchQuery) {
            filtered = filtered.filter(row => {
                return Object.values(row).some(val => 
                    String(val).toLowerCase().includes(this.searchQuery.toLowerCase())
                );
            });
        }
        
        const start = (this.currentPage - 1) * this.rowsPerPage;
        const end = start + this.rowsPerPage;
        return filtered.slice(start, end);
    }

    render() {
        const dataToRender = this.filteredAndPaginatedData;
        
        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    font-family: 'Inter', sans-serif;
                    background: var(--surface-color, #fff);
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    overflow: hidden;
                }
                .toolbar {
                    display: flex;
                    justify-content: space-between;
                    padding: 16px;
                    border-bottom: 1px solid var(--border-color, #eee);
                }
                input[type="search"] {
                    padding: 8px 12px;
                    border: 1px solid var(--border-color, #ccc);
                    border-radius: 4px;
                    width: 250px;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    padding: 12px 16px;
                    text-align: left;
                    border-bottom: 1px solid var(--border-color, #eee);
                }
                th {
                    background: var(--header-bg, #f8f9fa);
                    cursor: pointer;
                    user-select: none;
                    font-weight: 600;
                    color: var(--text-color, #333);
                }
                th:hover {
                    background: var(--header-hover-bg, #e9ecef);
                }
                tr:hover {
                    background: var(--row-hover-bg, #f1f3f5);
                }
                .pagination {
                    display: flex;
                    justify-content: flex-end;
                    padding: 16px;
                    gap: 8px;
                }
                button {
                    padding: 6px 12px;
                    border: 1px solid var(--border-color, #ccc);
                    background: #fff;
                    cursor: pointer;
                    border-radius: 4px;
                }
                button:disabled {
                    opacity: 0.5;
                    cursor: not-allowed;
                }
            </style>
            
            <div class="toolbar">
                <input type="search" placeholder="Search across all columns..." id="searchInput" value="${this.searchQuery}">
                <button id="exportCsv">Export CSV</button>
            </div>
            
            <table>
                <thead>
                    <tr>
                        ${this.columns.map(col => `
                            <th data-column="${col.key}">
                                ${col.label}
                                ${this.sortColumn === col.key ? (this.sortDirection === 'asc' ? ' ↑' : ' ↓') : ''}
                            </th>
                        `).join('')}
                    </tr>
                </thead>
                <tbody>
                    ${dataToRender.map(row => `
                        <tr>
                            ${this.columns.map(col => `
                                <td>${row[col.key] !== undefined ? row[col.key] : '-'}</td>
                            `).join('')}
                        </tr>
                    `).join('')}
                </tbody>
            </table>
            
            <div class="pagination">
                <button id="prevPage" ${this.currentPage === 1 ? 'disabled' : ''}>Previous</button>
                <span>Page ${this.currentPage}</span>
                <button id="nextPage" ${dataToRender.length < this.rowsPerPage ? 'disabled' : ''}>Next</button>
            </div>
        `;
        this.setupListeners();
    }

    setupListeners() {
        const headers = this.shadowRoot.querySelectorAll('th');
        headers.forEach(th => {
            th.addEventListener('click', () => {
                this.sortData(th.dataset.column);
            });
        });

        const searchInput = this.shadowRoot.querySelector('#searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.searchQuery = e.target.value;
                this.currentPage = 1;
                this.render();
            });
        }

        const prevBtn = this.shadowRoot.querySelector('#prevPage');
        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                if (this.currentPage > 1) {
                    this.currentPage--;
                    this.render();
                }
            });
        }

        const nextBtn = this.shadowRoot.querySelector('#nextPage');
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                this.currentPage++;
                this.render();
            });
        }
        
        const exportBtn = this.shadowRoot.querySelector('#exportCsv');
        if(exportBtn) {
            exportBtn.addEventListener('click', () => this.exportToCsv());
        }
    }
    
    exportToCsv() {
        const headers = this.columns.map(c => c.label).join(',');
        const rows = this.data.map(row => 
            this.columns.map(c => `"${row[c.key] || ''}"`).join(',')
        ).join('\n');
        
        const csvContent = "data:text/csv;charset=utf-8," + headers + "\n" + rows;
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "export.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

customElements.define('advanced-data-table', AdvancedDataTable);
