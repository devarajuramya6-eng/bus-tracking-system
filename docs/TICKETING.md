# CityBus Enterprise Platform - Digital Ticketing & Cryptographic QR Verification

## 1. Cryptographic QR Token Architecture
CityBus passes are digitally signed with HMAC-SHA256:

```
Payload = {
   "tck": "TCK-260825-4F8A92",
   "uid": 104,
   "amt": 45.0,
   "sig": HMAC_SHA256("CITYBUS|TCK-260825-4F8A92|104|45.0", SECRET_KEY)[0:16]
}
```

The payload is Base64 encoded and rendered as a 2D QR matrix for conductor scanning.

## 2. Validation State Machine
```
       +--------------+
       |   CREATED    |
       +-------+------+
               |
               v
       +--------------+
       |    VALID     +--------[ Expired (>6 hrs) ]-------> [ EXPIRED ]
       +-------+------+
               |
       [ Conductor Scan ]
               |
               v
       +--------------+
       |     USED     +--------[ Subsequent Scan ]---------> [ ALREADY_USED Warning ]
       +--------------+
```
