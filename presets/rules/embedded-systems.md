# Embedded Systems Rules

- Strictly avoid dynamic memory allocation (`malloc`/`new`) after initialization to prevent fragmentation.
- Use fixed-width integer types (e.g., `uint32_t`, `int16_t`) instead of standard `int`.
- Mark hardware registers and shared memory variables as `volatile`.
- Keep Interrupt Service Routines (ISRs) as short and fast as possible; defer heavy processing to the main loop.
- Optimize for low power consumption when idle.