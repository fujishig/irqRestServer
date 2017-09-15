SERVER_HOST = 'localhost'
SERVER_PORT = 8001
# Log path where your logs are generated
logPath = "/var/log/irqLogs/"
irqPath = "/proc/irq/"
# Log path where your irq affinity is written.  This is distinct for testing purposes, otherwise should be the same as irqPath.
# Note:  you need to create dummy smp_affinity files like iqrWritePath/0/smp_affinity
#irqWritePath = irqPath
irqWritePath = "/tmp/fakeirq"

