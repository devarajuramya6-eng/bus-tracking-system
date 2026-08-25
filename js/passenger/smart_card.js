/**
 * CityBus Enterprise Platform - Virtual RFID / NFC Smart Card Wallet
 * File: js/passenger/smart_card.js
 * 
 * Provides contactless tap-to-pay transit card management:
 * - NFC / RFID card simulation with visual chip & balance
 * - Instant balance top-up via UPI / Cards
 * - Auto-recharge threshold rules (e.g. auto top-up ₹200 when balance < ₹50)
 * - Tap-in and Tap-out journey history ledger
 */

class CityBusSmartCard {
  constructor() {
    this.storageKey = 'citybus_smart_card_data';
    this.card = this.loadCard();
  }

  loadCard() {
    const saved = localStorage.getItem(this.storageKey);
    if (saved) {
      try { return JSON.parse(saved); } catch (e) {}
    }

    const defaultCard = {
      cardNumber: 'CB-8849-2094-1029',
      cardHolder: 'COMMUTER PASSENGER',
      balance: 340.0,
      cardType: 'Metro Regular (Concession 10%)',
      autoRechargeEnabled: true,
      autoRechargeThreshold: 50.0,
      autoRechargeAmount: 200.0,
      expiryDate: '12/29',
      activeTrip: null, // Holds tap-in stop details
      transactions: [
        { id: 'TX-901', type: 'TAP_OUT', amount: -25.0, route: '27A (PNBS ⇄ Guntur)', time: 'Yesterday, 6:45 PM', balanceAfter: 340.0 },
        { id: 'TX-902', type: 'TOP_UP', amount: +200.0, method: 'UPI / PhonePe', time: 'Yesterday, 10:15 AM', balanceAfter: 365.0 },
        { id: 'TX-903', type: 'TAP_OUT', amount: -20.0, route: '5K (Autonagar ⇄ Railway Stn)', time: '24 Aug, 8:30 AM', balanceAfter: 165.0 }
      ]
    };
    this.saveCard(defaultCard);
    return defaultCard;
  }

  saveCard(card) {
    this.card = card;
    localStorage.setItem(this.storageKey, JSON.stringify(this.card));
    window.dispatchEvent(new CustomEvent('citybus:smartcard_updated', { detail: this.card }));
  }

  topUp(amount, method = 'UPI') {
    if (amount <= 0) return false;
    this.card.balance += parseFloat(amount);
    this.card.transactions.unshift({
      id: `TX-${Date.now().toString().slice(-4)}`,
      type: 'TOP_UP',
      amount: parseFloat(amount),
      method,
      time: 'Just now',
      balanceAfter: this.card.balance
    });
    this.saveCard(this.card);
    if (window.showToast) {
      window.showToast(`Card topped up successfully with ₹${amount}! Balance: ₹${this.card.balance.toFixed(2)}`, 'success');
    }
    return true;
  }

  tapIn(stopName, busNumber, routeNumber) {
    if (this.card.activeTrip) {
      return { success: false, message: 'You already have an ongoing trip. Please tap out first.' };
    }
    if (this.card.balance < 20.0) {
      return { success: false, message: 'Insufficient card balance. Please top up before boarding.' };
    }

    this.card.activeTrip = {
      originStop: stopName,
      busNumber,
      routeNumber,
      tapInTime: new Date().toISOString()
    };
    this.saveCard(this.card);
    return { success: true, message: `Tap-in recorded at ${stopName}. Have a safe journey!` };
  }

  tapOut(stopName, fareAmount = 25.0) {
    if (!this.card.activeTrip) {
      return { success: false, message: 'No active tap-in journey detected on this smart card.' };
    }

    const trip = this.card.activeTrip;
    this.card.balance -= fareAmount;

    // Check auto-recharge
    let autoRecharged = false;
    if (this.card.autoRechargeEnabled && this.card.balance < this.card.autoRechargeThreshold) {
      this.card.balance += this.card.autoRechargeAmount;
      autoRecharged = true;
    }

    this.card.transactions.unshift({
      id: `TX-${Date.now().toString().slice(-4)}`,
      type: 'TAP_OUT',
      amount: -fareAmount,
      route: `${trip.routeNumber} (${trip.originStop} ➔ ${stopName})`,
      time: 'Just now',
      balanceAfter: this.card.balance
    });

    this.card.activeTrip = null;
    this.saveCard(this.card);

    let msg = `Tap-out successful at ${stopName}. Fare: ₹${fareAmount.toFixed(2)}. Balance: ₹${this.card.balance.toFixed(2)}.`;
    if (autoRecharged) {
      msg += ` (Auto-recharged ₹${this.card.autoRechargeAmount})`;
    }
    return { success: true, message: msg };
  }
}

// Global Export
window.CityBusSmartCard = new CityBusSmartCard();
