# iot-embedded

Firmware, embedded devices, and device-paired services.

## Detection signals

- Firmware toolchains: PlatformIO.ini, ESP-IDF, Zephyr, mbed, MCUboot, linker scripts for MCU targets
- C/C++ bare-metal or RTOS code, .bin/.elf firmware artifacts, OTA update services
- Hardware SDKs paired with mobile/cloud apps (BLE/Matter/MQTT device code)

## Stack quick-map

- Any firmware/OTA/device-provisioning code → iot-embedded, supply-chain
- Device + cloud backend → also backend categories for the paired API
- Device credentials, pairing or provisioning present → authentication, secrets-crypto
