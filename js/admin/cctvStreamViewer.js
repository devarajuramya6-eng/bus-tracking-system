class CCTVStreamViewerController {
    constructor() { this.activeBusId = 1; }
    async init() {
        if (!window.authService.requireAuth(['admin', 'super_admin', 'dispatcher'])) return;
        this.renderStreamMatrix();
    }
    renderStreamMatrix() {
        const container = document.getElementById('cctv-matrix-container');
        if (!container) return;
        container.innerHTML = `
            <div class="row g-2">
                <div class="col-md-6"><div class="cctv-box bg-dark text-white p-4 text-center rounded"><i class="fas fa-video fa-2x mb-2"></i><div>Cam 1: Driver Forward View</div><small class="text-success">● LIVE 1080p</small></div></div>
                <div class="col-md-6"><div class="cctv-box bg-dark text-white p-4 text-center rounded"><i class="fas fa-video fa-2x mb-2"></i><div>Cam 2: Saloon Cabin</div><small class="text-success">● LIVE 1080p</small></div></div>
                <div class="col-md-6"><div class="cctv-box bg-dark text-white p-4 text-center rounded"><i class="fas fa-video fa-2x mb-2"></i><div>Cam 3: Rear Door Exit</div><small class="text-success">● LIVE 1080p</small></div></div>
                <div class="col-md-6"><div class="cctv-box bg-dark text-white p-4 text-center rounded"><i class="fas fa-video fa-2x mb-2"></i><div>Cam 4: Passenger Step</div><small class="text-success">● LIVE 1080p</small></div></div>
            </div>
        `;
    }
}
window.cctvStreamViewer = new CCTVStreamViewerController();
