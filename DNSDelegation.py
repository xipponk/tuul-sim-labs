import dns.resolver
import dns.name
import dns.query
import dns.message
import dns.rdatatype

# Hardcoded TLD type dictionary (can be expanded)
tld_types = {
    # Sponsored TLDs (sTLD)
    'edu': 'sTLD (sponsored)',
    'gov': 'sTLD (sponsored)',
    'mil': 'sTLD (sponsored)',
    'int': 'sTLD (sponsored)',
    'museum': 'sTLD (sponsored)',
    'aero': 'sTLD (sponsored)',
    'coop': 'sTLD (sponsored)',
    'post': 'sTLD (sponsored)',
    'travel': 'sTLD (sponsored)',
    # Infrastructure
    'arpa': 'Infrastructure',
    # Common gTLDs
    'com': 'gTLD (generic)',
    'org': 'gTLD (generic)',
    'net': 'gTLD (generic)',
    'info': 'gTLD (generic)',
    'biz': 'gTLD (generic)',
    'name': 'gTLD (generic)',
    'xyz': 'gTLD (generic)',
    'top': 'gTLD (generic)',
    'site': 'gTLD (generic)',
    # Add more if needed
}

def get_tld_type(tld):
    if tld.lower() in tld_types:
        return tld_types[tld.lower()]
    elif len(tld) == 2:
        return 'ccTLD (country-code)'
    else:
        return 'gTLD (generic)'

def get_delegation_chain(domain):
    name = dns.name.from_text(domain)
    nameservers = ['198.41.0.4']  # Root server A
    chain = []

    print("\n🧭 Starting DNS Delegation from the root zone:")
    for i in range(len(name.labels) - 1, -1, -1):
        current = dns.name.Name(name.labels[i:])
        if not current.is_absolute():
            current = current.concatenate(dns.name.root)

        zone_name = str(current).strip('.')
        print(f"🔹 Checking Zone: {zone_name or '(root)'}")

        try:
            query = dns.message.make_query(current, dns.rdatatype.NS)
            for ns_ip in nameservers:
                try:
                    print(f"  ↪ Using NS IP: {ns_ip}")
                    response = dns.query.udp(query, ns_ip, timeout=3)
                    ns_list = []
                    for rrset in response.authority:
                        if rrset.rdtype == dns.rdatatype.NS:
                            ns_list = [ns.to_text() for ns in rrset]
                    if ns_list:
                        print(f"  ✅ NS found: {ns_list}")
                        if not chain or chain[-1][0] != str(current):
                            chain.append((str(current), ns_list))
                        # Resolve IPs of NS
                        nameservers = []
                        for ns in ns_list:
                            try:
                                ip = dns.resolver.resolve(ns, 'A')[0].to_text()
                                print(f"     ↪ {ns} → {ip}")
                                nameservers.append(ip)
                            except:
                                print(f"     ⚠️  Could not resolve IP for {ns}")
                        break
                except Exception as e:
                    print(f"  ⚠️  NS {ns_ip} did not respond: {e}")
        except Exception as e:
            print(f"❌ Query failed: {e}")
    return chain

def summarize_dns_info(domain, chain):
    name = dns.name.from_text(domain)
    labels = [label.decode() for label in name.labels if label]
    label_count = len(labels)

    root = '.'
    tld = labels[-1] if label_count >= 1 else "(none)"
    sld = f"{labels[-2]}.{labels[-1]}" if label_count >= 2 else "(none)"
    subdomain = ".".join(labels[:-2]) if label_count > 2 else "(none)"

    tld_type = get_tld_type(tld)

    print("\n📌 Domain Structure Summary:")
    print(f"- Root Domain: {root}")
    print(f"- Top-Level Domain (TLD): {tld}")
    print(f"- Second-Level Domain (SLD): {sld}")
    print(f"- Subdomain: {subdomain}")
    print(f"- TLD Type: {tld_type}")
    print(f"- Total Zones Discovered: {len(chain)}\n")

    print("🧾 Zones and their Authoritative Name Servers:")
    for zone, ns_list in chain:
        print(f"Zone: {zone}")
        for ns in ns_list:
            print(f"  ↳ NS: {ns}")

# === Main Entry ===
if __name__ == "__main__":
    domain = input("Enter a URL or domain (e.g., blog.sit.kmutt.ac.th): ").strip()
    chain = get_delegation_chain(domain)
    if not chain:
        chain = [(domain, ["(no delegation found)"])]
    summarize_dns_info(domain, chain)