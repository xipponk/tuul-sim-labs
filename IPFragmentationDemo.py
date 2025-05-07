import matplotlib.pyplot as plt
import random

def calculate_fragments():
    print("=== IP Fragmentation Calculator ===")

    # Step 1: IP Header Size
    ip_header_size = input("Enter Transport Layer Header size in bytes: ")
    if ip_header_size.strip() == "":
        ip_header_size = 20
    else:
        ip_header_size = int(ip_header_size)

    # Step 1.1: IP ID
    ip_id_input = input("Enter IP ID (decimal) or leave blank for random: ")
    ip_id = int(ip_id_input) if ip_id_input.strip() != "" else random.randint(1, 65535)

    # Step 2: Payload Size
    total_payload_size = int(input("Enter total Payload size in bytes: "))

    # Step 3: MTU
    mtu = int(input("Enter MTU size in bytes: "))

    # Total packet size
    total_packet_size = ip_header_size + total_payload_size

    print("\n[INFO] Total Packet Size:", total_packet_size, "bytes")
    print("[INFO] MTU:", mtu, "bytes")

    if total_packet_size <= mtu:
        print("\n No fragmentation needed.")
        return

    print("\n Fragmentation is required.")

    # Step 5: Fragmentation
    max_data_per_fragment = mtu - ip_header_size
    max_data_per_fragment -= max_data_per_fragment % 8  # must align to 8 bytes

    fragments = []
    offset = 0
    remaining_payload = total_payload_size
    fragment_index = 0
    df_flag = 0  # Don't Fragment flag = 0, allow fragmentation

    while remaining_payload > 0:
        fragment_payload_size = min(max_data_per_fragment, remaining_payload)
        mf_flag = 1 if remaining_payload > fragment_payload_size else 0
        fragment_offset = offset // 8

        fragments.append({
            "index": fragment_index + 1,
            "IP ID": ip_id,
            "Header": ip_header_size,
            "Payload": fragment_payload_size,
            "Total": ip_header_size + fragment_payload_size,
            "Flag": f"0{df_flag}{mf_flag}",
            "Offset": fragment_offset,
            "Start": offset,                          # First byte of this fragment (payload only)
            "End": offset + fragment_payload_size - 1 # Last byte (inclusive)
        })

        remaining_payload -= fragment_payload_size
        offset += fragment_payload_size
        fragment_index += 1

    print(f"\n Number of fragments required: {len(fragments)}\n")
    for frag in fragments:
        print(f"  Fragment {frag['index']}:")
        print(f"    IP ID: {frag['IP ID']}")
        print(f"    Header Size: {frag['Header']} bytes")
        print(f"    Payload Size: {frag['Payload']} bytes")
        print(f"    Total Fragment Size: {frag['Total']} bytes")
        print(f"    Flags (3-bit): {frag['Flag']}")
        print(f"    First Byte Offset: {frag['Start']}")
        print(f"    Last Byte Offset:  {frag['End']}")
        print(f"    Fragment Offset: {frag['Start']} / 8 = {frag['Offset']} (in 8-byte units)\n")

    # Visualization
    fig, ax = plt.subplots(figsize=(10, len(fragments) * 1.2))
    for i, frag in enumerate(fragments):
        # Plot payload block
        ax.barh(y=i, width=frag['Payload'], left=frag['Start'], color='skyblue', edgecolor='black', label='Payload' if i==0 else "")
        # Plot header block
        ax.barh(y=i, width=frag['Header'], left=frag['Start'] - frag['Header'], color='orange', edgecolor='black', label='Header' if i==0 else "")
        # Label
        ax.text(frag['Start'] + frag['Payload'] / 2, i, f"Frag {frag['index']}", ha='center', va='center', fontsize=9, color='black')

    ax.set_yticks(range(len(fragments)))
    ax.set_yticklabels([f"Frag {frag['index']}" for frag in fragments])
    ax.set_xlabel("Byte Offset")
    ax.set_title("IP Fragmentation Visualization")
    ax.legend()
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    calculate_fragments()