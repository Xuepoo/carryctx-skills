# Computer Networking Rules

- Specify IP versions (IPv4 vs IPv6) explicitly in socket programming.
- Always set appropriate timeouts for connections, reads, and writes.
- Handle partial reads/writes in stream sockets (TCP).
- For UDP, account for packet loss and out-of-order delivery.
- Log source IP and ports for all incoming requests for auditability.
