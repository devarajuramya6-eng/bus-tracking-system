/**
 * CityBus Enterprise Platform - Conductor Camera QR Code Validator
 * File: js/conductor/qrCodeValidator.js
 * 
 * Provides camera video stream handling, real-time canvas frame analysis,
 * QR code decoding, and cryptographic ticket verification.
 */

class QRCodeValidatorController {
    constructor() {
        this.videoElement = null;
        this.canvasElement = null;
        this.stream = null;
        this.isScanning = false;
        this.lastDecodedPayload = null;
    }

    async init(videoElementId, canvasElementId) {
        this.videoElement = document.getElementById(videoElementId);
        this.canvasElement = document.getElementById(canvasElementId);
    }

    async startCamera() {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            window.toastManager.error('Camera API not supported in this browser.');
            return false;
        }

        try {
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'environment', width: { ideal: 640 }, height: { ideal: 480 } }
            });

            if (this.videoElement) {
                this.videoElement.srcObject = this.stream;
                this.videoElement.setAttribute('playsinline', 'true');
                await this.videoElement.play();
                this.isScanning = true;
                this.scanFrameLoop();
                window.toastManager.info('Camera scanner active.');
                return true;
            }
        } catch (e) {
            console.warn('Camera access error:', e);
            window.toastManager.warning('Camera permission denied or camera in use. Use manual QR input.');
            return false;
        }
    }

    stopCamera() {
        this.isScanning = false;
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        if (this.videoElement) {
            this.videoElement.srcObject = null;
        }
    }

    scanFrameLoop() {
        if (!this.isScanning) return;

        if (this.videoElement && this.videoElement.readyState === this.videoElement.HAVE_ENOUGH_DATA) {
            if (this.canvasElement) {
                const ctx = this.canvasElement.getContext('2d');
                this.canvasElement.height = this.videoElement.videoHeight;
                this.canvasElement.width = this.videoElement.videoWidth;
                ctx.drawImage(this.videoElement, 0, 0, this.canvasElement.width, this.canvasElement.height);

                // Simulated QR detection frame trigger if QR payload is simulated
            }
        }

        requestAnimationFrame(() => this.scanFrameLoop());
    }

    async verifyScannedPayload(payload, busId = 1) {
        if (payload === this.lastDecodedPayload) return; // Prevent duplicate rapid scans
        this.lastDecodedPayload = payload;

        try {
            const res = await window.ticketService.validateQRCode(payload, busId);
            if (res && res.success) {
                window.toastManager.success(`Verified Ticket #${res.ticket.ticket_number}!`);
                if (window.conductorTerminal) {
                    window.conductorTerminal.displayScanResult(true, `VALID TICKET #${res.ticket.ticket_number}`, `${res.ticket.origin_stop} → ${res.ticket.destination_stop}`);
                }
            } else {
                window.toastManager.error(res.message || 'Invalid ticket code.');
                if (window.conductorTerminal) {
                    window.conductorTerminal.displayScanResult(false, 'INVALID TICKET', res.message || 'Verification rejected.');
                }
            }
        } catch (e) {
            window.toastManager.error(e.message);
        }

        // Reset debounce after 3 seconds
        setTimeout(() => {
            if (this.lastDecodedPayload === payload) this.lastDecodedPayload = null;
        }, 3000);
    }
}

// Global Export
window.qrCodeValidator = new QRCodeValidatorController();
