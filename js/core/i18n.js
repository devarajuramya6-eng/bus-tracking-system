/**
 * CityBus Enterprise Platform - Internationalization (i18n) Engine
 * File: js/core/i18n.js
 * 
 * Provides runtime multi-language translation and localization for:
 * - English (en)
 * - Telugu / తెలుగు (te)
 * - Hindi / हिन्दी (hi)
 */

class CityBusi18n {
  constructor() {
    this.currentLocale = localStorage.getItem('citybus_lang') || 'en';
    this.translations = {
      en: {
        appName: "CityBus Transit",
        liveTracking: "Live GPS Radar",
        journeyPlanner: "Journey Planner",
        buses: "Fleet Directory",
        routes: "Transit Routes",
        stops: "Bus Stops",
        tickets: "Book Ticket",
        myTickets: "My Passes",
        driverCockpit: "Driver Cockpit",
        conductorPOS: "Conductor Terminal",
        dispatcherRadar: "Dispatcher Radar",
        adminConsole: "Operations Admin",
        searchPlaceholder: "Search buses, routes, stops... (Ctrl + K)",
        speed: "Speed",
        heading: "Heading",
        occupancy: "Occupancy",
        status: "Status",
        fare: "Fare",
        eta: "ETA",
        distance: "Distance",
        mins: "mins",
        km: "km",
        kmh: "km/h",
        onRoute: "On Route",
        delayed: "Delayed",
        maintenance: "Maintenance",
        emergency: "Emergency",
        sosPanic: "EMERGENCY SOS",
        ticketValid: "VALID PASS",
        ticketUsed: "USED PASS",
        ticketExpired: "EXPIRED",
        scanQR: "Scan Ticket QR",
        boardPassenger: "Board (+1)",
        alightPassenger: "Alight (-1)",
        routePlannerTitle: "Find Your Route Across Vijayawada & Amaravati",
        fromStop: "Departure Stop",
        toStop: "Destination Stop",
        findRoutes: "Calculate Fast Routes",
        emergencyAlert: "Emergency Alert Broadcasted",
        offlineNotice: "Working in offline mode"
      },
      te: {
        appName: "సిటీ బస్సు రవాణా",
        liveTracking: "లైవ్ బస్ ట్రాకింగ్",
        journeyPlanner: "ప్రయాణ ప్రణాళిక",
        buses: "బస్సుల జాబితా",
        routes: "బస్సు మార్గాలు",
        stops: "బస్టాపులు",
        tickets: "టికెట్ బుకింగ్",
        myTickets: "నా టిక్కెట్లు",
        driverCockpit: "డ్రైవర్ కాక్‌పిట్",
        conductorPOS: "కండక్టర్ టెర్మినల్",
        dispatcherRadar: "డిస్పాచర్ రాడార్",
        adminConsole: "అడ్మిన్ నిర్వహణ",
        searchPlaceholder: "బస్సులు, మార్గాలు, స్టాప్‌ల కోసం వెతకండి...",
        speed: "వేగం",
        heading: "దిశ",
        occupancy: "ప్రయాణికుల సంఖ్య",
        status: "స్థితి",
        fare: "ఛార్జీ",
        eta: "చేరుకునే సమయం",
        distance: "దూరం",
        mins: "నిమిషాలు",
        km: "కి.మీ",
        kmh: "కి.మీ/గంట",
        onRoute: "ప్రయాణంలో ఉంది",
        delayed: "ఆలస్యం",
        maintenance: "మరమ్మత్తులో ఉంది",
        emergency: "అత్యవసర పరిస్థితి",
        sosPanic: "అత్యవసర SOS",
        ticketValid: "చెల్లుబాటు అయ్యే టికెట్",
        ticketUsed: "ఉపయోగించిన టికెట్",
        ticketExpired: "గడువు ముగిసింది",
        scanQR: "QR కోడ్ స్కాన్ చేయండి",
        boardPassenger: "ఎక్కినవారు (+1)",
        alightPassenger: "దిగినవారు (-1)",
        routePlannerTitle: "విజయవాడ & అమరావతి అంతటా ప్రయాణ మార్గాలు",
        fromStop: "బయలుదేరే స్టాప్",
        toStop: "గమ్యస్థాన స్టాప్",
        findRoutes: "మార్గాలను కనుగొనండి",
        emergencyAlert: "అత్యవసర హెచ్చరిక జారీ చేయబడింది",
        offlineNotice: "ఆఫ్‌లైన్ మోడ్‌లో పని చేస్తోంది"
      },
      hi: {
        appName: "सिटी बस पारगमन",
        liveTracking: "लाइव बस ट्रैकिंग",
        journeyPlanner: "यात्रा योजना",
        buses: "बस सूची",
        routes: "बस मार्ग",
        stops: "बस स्टॉप",
        tickets: "टिकट बुक करें",
        myTickets: "मेरे टिकट",
        driverCockpit: "ड्राइवर कॉकपिट",
        conductorPOS: "कंडक्टर टर्मिनल",
        dispatcherRadar: "डिस्पैचर रडार",
        adminConsole: "प्रशासन",
        searchPlaceholder: "बसें, मार्ग, स्टॉप खोजें...",
        speed: "गति",
        heading: "दिशा",
        occupancy: "यात्री संख्या",
        status: "स्थिति",
        fare: "किराया",
        eta: "पहुंचने का समय",
        distance: "दूरी",
        mins: "मिनट",
        km: "किमी",
        kmh: "किमी/घंटा",
        onRoute: "मार्ग पर",
        delayed: "विलंबित",
        maintenance: "रखरखाव",
        emergency: "आपातकालीन",
        sosPanic: "आपातकालीन SOS",
        ticketValid: "वैध पास",
        ticketUsed: "उपयोग किया गया",
        ticketExpired: "समाप्त",
        scanQR: "QR स्कैन करें",
        boardPassenger: "यात्री चढ़े (+1)",
        alightPassenger: "यात्री उतरे (-1)",
        routePlannerTitle: "विजयवाड़ा और अमरावती के बीच यात्रा मार्ग",
        fromStop: "प्रारंभिक स्टॉप",
        toStop: "गंतव्य स्टॉप",
        findRoutes: "मार्ग खोजें",
        emergencyAlert: "आपातकालीन चेतावनी जारी",
        offlineNotice: "ऑफ़लाइन मोड सक्रिय"
      }
    };
  }

  setLocale(locale) {
    if (this.translations[locale]) {
      this.currentLocale = locale;
      localStorage.setItem('citybus_lang', locale);
      this.translatePage();
      window.dispatchEvent(new CustomEvent('citybus:locale_changed', { detail: { locale } }));
    }
  }

  t(key, defaultVal = '') {
    const dict = this.translations[this.currentLocale] || this.translations.en;
    return dict[key] || this.translations.en[key] || defaultVal || key;
  }

  translatePage() {
    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(el => {
      const key = el.getAttribute('data-i18n');
      const translation = this.t(key);
      if (translation) {
        if (el.tagName === 'INPUT' && el.placeholder) {
          el.placeholder = translation;
        } else {
          el.textContent = translation;
        }
      }
    });
  }
}

// Global Singleton Export
window.CityBusi18n = new CityBusi18n();
document.addEventListener('DOMContentLoaded', () => {
  window.CityBusi18n.translatePage();
});
