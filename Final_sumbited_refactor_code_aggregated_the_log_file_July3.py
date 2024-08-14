LOG_FILE_CONTENT = """
*.amazon.co.uk    89,
*.doubleclick.net    139,
*.fbcdn.net    212,
 *.in-addr.arpa    384,
 *.l.google.com    317,
 1.client-channel.google.com    110,
 6.client-channel.google.com    45,
 a.root-servers.net    1059,
 apis.google.com    43,
  clients4.google.com    71,
  clients6.google.com    81,
   connect.facebook.net    68,
    edge-mqtt.facebook.com    56,
    graph.facebook.com    150,
    mail.google.com    128,
    mqtt-mini.facebook.com    47,
    ssl.google-analytics.com    398,
    star-mini.c10r.facebook.com    46,
    staticxx.facebook.com    48,
    www.facebook.com    178,
    www.google.com    162,
    www.google-analytics.com    127,
    www.googleapis.com    87
"""

def get_base_domain(domain):
    parts = domain.split('.')
    if len(parts) > 2:
        return '.'.join(parts[-2:])
    return domain

def count_domains(log_file, min_hits):
    # Remove newlines and extra spaces, then split by comma
    # Ensures each entry is stripped of leading and trailing spaces.
    log_file_split = [entry.strip() for entry in log_file.replace("\n", "").split(',')]
    domain_hits = {}

    for entry in log_file_split:
        try:
            domain, hits = entry.rsplit(maxsplit=1)  # Ensures the split is correctly performed even if domains contain spaces.
            hits = int(hits)
            base_domain = get_base_domain(domain)
            if base_domain in domain_hits:
                domain_hits[base_domain] += hits
            else:
                domain_hits[base_domain] = hits
        except ValueError:
            print(f"Skipping malformed line: {entry}")

    filtered_domain_hits = {domain: hits for domain, hits in domain_hits.items() if hits >= min_hits}
    return filtered_domain_hits


#Define the Minimum Hits Threshold (min_hits = 500):
def main():
    min_hits = 500
    domain_hits = count_domains(LOG_FILE_CONTENT, min_hits)

    sorted_domains = sorted(domain_hits.items(), key=lambda item: item[1], reverse=True)

    for domain, hits in sorted_domains:
        print(f"{domain} ({hits})")    # Filter out domains with fewer than 500 hits.

if __name__ == "__main__":
    main()
