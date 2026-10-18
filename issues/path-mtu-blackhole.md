---
categories: [cloud-network]
domains: [infrastructure]
---

# Path MTU blackholes diagnosed on tunnel/VPN paths

**SHOULD** verify path MTU handling on every tunnel, VPN, or encapsulated route: clamp MSS at tunnel ingress and never blanket-drop ICMP "fragmentation needed" messages.

**Why:** When ICMP Type 3 Code 4 is blocked, packets larger than the tunnel's reduced MTU vanish silently — TLS handshakes and small requests succeed while larger payloads hang forever, a failure pattern users describe as "some sites work, others just spin."

**Detect:** Probe with `ping -M do -s 1472` (and descending sizes) across the tunnel; check tunnel interface MTU vs underlay, iptables rules dropping ICMP unreachables, MSS clamping presence (`--clamp-mss-to-pmtu` or LB/Cloud NAT settings), and VPN configs (WireGuard `MTU=1420`, IPsec overhead). Look for TCP windows stalling at handshake in packet captures.

**Bad:**
```
iptables -A FORWARD -p icmp --icmp-type fragmentation-needed -j DROP
# oversized packets now disappear with no error back to the sender
```

**Good:**
```
iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN \
         -j TCPMSS --clamp-mss-to-pmtu
```

**References:** RFC 8899 (PMTUD), RFC 1191, AWS VPN MTU docs, Black Hole Router / PMTU blackhole literature
