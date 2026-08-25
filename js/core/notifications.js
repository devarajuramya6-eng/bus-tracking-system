/**
 * CityBus Enterprise Platform - Notification & Alert Center
 * File: js/core/notifications.js
 * 
 * Manages in-app notifications, browser notifications, sound chimes,
 * unread badges, and category filters (Bus, Ticket, Payment, Alert, Incident, Emergency).
 */

class CityBusNotificationManager {
  constructor() {
    this.notifications = [];
    this.storageKey = 'citybus_notifications_list';
    this.unreadCount = 0;
    this.loadFromStorage();
  }

  loadFromStorage() {
    try {
      const data = localStorage.getItem(this.storageKey);
      this.notifications = data ? JSON.parse(data) : this.getDefaultNotifications();
      this.updateUnreadCount();
    } catch {
      this.notifications = this.getDefaultNotifications();
    }
  }

  saveToStorage() {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(this.notifications));
      this.updateUnreadCount();
    } catch {}
  }

  getDefaultNotifications() {
    return [
      {
        id: 'notif-1',
        category: 'Bus',
        title: 'Bus 27A Approaching',
        message: 'Bus 27A is 2 stops away from Benz Circle Junction (~4 mins).',
        timestamp: new Date(Date.now() - 1000 * 60 * 3).toISOString(),
        read: false,
        severity: 'info'
      },
      {
        id: 'notif-2',
        category: 'Alert',
        title: 'Road Maintenance on MG Road',
        message: 'Routes 12B and 45C are experiencing mild 5-min delays near DV Manor.',
        timestamp: new Date(Date.now() - 1000 * 60 * 25).toISOString(),
        read: false,
        severity: 'warning'
      },
      {
        id: 'notif-3',
        category: 'Ticket',
        title: 'Ticket Confirmed',
        message: 'Ticket #TCK-8829 for Route 27A (PNBS → Guntur) has been issued.',
        timestamp: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
        read: true,
        severity: 'success'
      }
    ];
  }

  addNotification(notif) {
    const newNotif = {
      id: `notif-${Date.now()}`,
      category: notif.category || 'System',
      title: notif.title,
      message: notif.message,
      timestamp: new Date().toISOString(),
      read: false,
      severity: notif.severity || 'info',
      meta: notif.meta || {}
    };

    this.notifications.unshift(newNotif);
    this.saveToStorage();

    // Show instant toast notification
    if (window.showToast) {
      window.showToast(`<strong>${newNotif.title}</strong>: ${newNotif.message}`, newNotif.severity);
    }

    // Play subtle chime for high priority alerts
    if (newNotif.severity === 'danger' || newNotif.severity === 'warning') {
      this.playChime();
    }

    window.dispatchEvent(new CustomEvent('citybus:notification-received', { detail: newNotif }));
  }

  markAsRead(id) {
    const notif = this.notifications.find(n => n.id === id);
    if (notif) {
      notif.read = true;
      this.saveToStorage();
    }
  }

  markAllAsRead() {
    this.notifications.forEach(n => n.read = true);
    this.saveToStorage();
  }

  deleteNotification(id) {
    this.notifications = this.notifications.filter(n => n.id !== id);
    this.saveToStorage();
  }

  clearAll() {
    this.notifications = [];
    this.saveToStorage();
  }

  updateUnreadCount() {
    this.unreadCount = this.notifications.filter(n => !n.read).length;
    document.querySelectorAll('.notif-badge-count').forEach(el => {
      el.textContent = this.unreadCount;
      el.style.display = this.unreadCount > 0 ? 'inline-flex' : 'none';
    });
  }

  playChime() {
    try {
      const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.type = 'sine';
      osc.frequency.setValueAtTime(587.33, audioCtx.currentTime); // D5
      osc.frequency.setValueAtTime(880, audioCtx.currentTime + 0.1); // A5
      gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.4);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.4);
    } catch {}
  }
}

// Global Singleton Export
window.CityBusNotifications = new CityBusNotificationManager();
