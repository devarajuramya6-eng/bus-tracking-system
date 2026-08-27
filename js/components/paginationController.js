/**
 * CityBus Enterprise Platform - Client Pagination Controller
 * File: js/components/paginationController.js
 * 
 * Reusable pagination component for tables, cards, and grid views.
 */

class PaginationController {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.totalItems = options.totalItems || 0;
        this.pageSize = options.pageSize || 10;
        this.currentPage = options.currentPage || 1;
        this.onPageChange = options.onPageChange || (() => {});
    }

    setPagination(totalItems, currentPage = 1) {
        this.totalItems = totalItems;
        this.currentPage = currentPage;
        this.render();
    }

    render() {
        if (!this.container) return;
        const totalPages = Math.ceil(this.totalItems / this.pageSize) || 1;

        let html = `
            <div class="pagination-wrapper d-flex justify-content-between align-items-center mt-3">
                <span class="pagination-info text-muted small">
                    Page ${this.currentPage} of ${totalPages} (${this.totalItems} total items)
                </span>
                <ul class="pagination pagination-sm mb-0">
                    <li class="page-item ${this.currentPage === 1 ? 'disabled' : ''}">
                        <button class="page-link page-prev-btn">&laquo; Prev</button>
                    </li>
        `;

        const maxButtons = 5;
        let startPage = Math.max(1, this.currentPage - 2);
        let endPage = Math.min(totalPages, startPage + maxButtons - 1);
        if (endPage - startPage < maxButtons - 1) {
            startPage = Math.max(1, endPage - maxButtons + 1);
        }

        for (let p = startPage; p <= endPage; p++) {
            html += `
                <li class="page-item ${p === this.currentPage ? 'active' : ''}">
                    <button class="page-link page-num-btn" data-page="${p}">${p}</button>
                </li>
            `;
        }

        html += `
                    <li class="page-item ${this.currentPage >= totalPages ? 'disabled' : ''}">
                        <button class="page-link page-next-btn">Next &raquo;</button>
                    </li>
                </ul>
            </div>
        `;

        this.container.innerHTML = html;
        this.bindEvents(totalPages);
    }

    bindEvents(totalPages) {
        const prevBtn = this.container.querySelector('.page-prev-btn');
        if (prevBtn) {
            prevBtn.onclick = () => {
                if (this.currentPage > 1) {
                    this.currentPage--;
                    this.render();
                    this.onPageChange(this.currentPage);
                }
            };
        }

        const nextBtn = this.container.querySelector('.page-next-btn');
        if (nextBtn) {
            nextBtn.onclick = () => {
                if (this.currentPage < totalPages) {
                    this.currentPage++;
                    this.render();
                    this.onPageChange(this.currentPage);
                }
            };
        }

        this.container.querySelectorAll('.page-num-btn').forEach(btn => {
            btn.onclick = () => {
                const p = Number(btn.dataset.page);
                if (p !== this.currentPage) {
                    this.currentPage = p;
                    this.render();
                    this.onPageChange(this.currentPage);
                }
            };
        });
    }
}

// Global Export
window.PaginationController = PaginationController;
