# Clock setup correction

The copied initializer overwrote the P3-12 configuration with discovery fields.
The first report failed before any event or interval was recorded. The process
exited; its configuration/control/log are preserved under setup0. The adapter
now validates the saved P3-12 configuration without replacing it. Zero research
or engaged time is credited to this failed administrative setup.
