# Raspberry Pi Temperature Monitor (DS18B20 → Supabase)

This project runs on a Raspberry Pi 4 and reads DS18B20 temperature sensors via 1-Wire, then uploads readings to Supabase.

## Related project (Phone App / PWA)
📱 Live dashboard PWA: **temp-pwa**  
- Repo: https://github.com/muasvoos/temp-pwa
- Purpose: View live temperatures on your phone (local time: America/Chicago)

## Architecture
Pi (DS18B20) → Supabase table `temperature_readings` → PWA dashboard (Realtime)

## Hardware
- Raspberry Pi 4
- 3× DS18B20 sensors
  - `28-011912555951` → ambient_room
  - `28-011912765725` → test_probe
  - `28-0119127640b5` → control_probe
- 4.7k pull-up resistor (DATA → 3.3V)
- Wiring / breadboard or terminal blocks

## Pi Setup
### Enable 1-Wire
```bash
sudo raspi-config
# Interface Options → 1-Wire → Enable → reboot
