# Conceptual Electrical Block Diagram

**Status: CONCEPTUAL.** Not matched to datasheets.

```
            +---------------------------+
  AC/DC --> |  Mains / Bench PSU / Pack |
            +------------+--------------+
                         |  (actuator bus, e.g. 24-48V)
              +----------+-----------+
              |   E-STOP (manual)    |  <-- latching, hardware, in power path
              |   + Safety Contactor |  <-- also droppable by Safety MCU
              +----------+-----------+
                         |
          +--------------+----------------+
          |      Fused actuator bus       |
          |  (per-group branch fusing)    |
          +--+--------+---------+---------+
             |        |         |
        [Joint drv][Joint drv][Joint drv] ... (CAN FD / RS-485)
             |        |         |
          [Motor]  [Motor]   [Motor] + encoders + temp sense

   Logic domain (separate converter, separately fused):
   +-----------+     +-----------+     +------------------+
   |  Host PC  |<--->| Motion MCU|<--->|  Safety MCU      |
   | (AI stack)| USB | (RT ctrl) | bus | (indep. watchdog,|
   +-----+-----+     +-----+-----+     |  estop, power)   |
         |                 |          +---------+---------+
   [Cam][Mic][Spk]   [IMU][current]            |
   [Wi-Fi/Eth]        [temp][encoders]   drops contactor on fault
```

Trust boundary: the manual E-STOP and safety contactor remove motor-bus power
regardless of the Host PC or Motion MCU state.
