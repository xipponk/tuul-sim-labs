import matplotlib.pyplot as plt
import random

def manual_fragmentation():
    print("=== Manual IP Fragmentation Trainer ===")

    # Input Header size
    ip_header_size = input("Enter Transport Layer Header size in bytes: ")
    if ip_header_size.strip() == "":
        ip_header_size = 20
    else:
        ip_header_size = int(ip_header_size)

    # Input IP ID
    ip_id_input = input("Enter IP ID (decimal) or leave blank for random: ")
    ip_id = int(ip_id_input) if ip_id_input.strip() != "" else random.randint(1, 65535)

    # Input Payload
    total_payload_size = int(input("Enter total Payload size in bytes: "))
    total_packet_size = ip_header_size + total_payload_size

    print(f"\n Total Packet Size: {total_packet_size} bytes (Header: {ip_header_size}, Payload: {total_payload_size})")

    # Input number of desired fragments
    try:
        num_fragments = int(input("Enter number of fragments you want to divide into (0 = no fragmentation): "))
    except ValueError:
        print(" Invalid input. Please enter a number.")
        return

    fragments = []
    df_flag = 0  # Assume fragmentation is allowed (DF = 0)

    if num_fragments <= 0:
        print("\n No fragmentation performed. Entire packet sent as one.\n")
        fragments = [{
            "index": 1,
            "IP ID": ip_id,
            "Header": ip_header_size,
            "Payload": total_payload_size,
            "Total": total_packet_size,
            "Flag": "000",
            "Offset": 0,
            "Start": 0,
            "End": total_payload_size - 1
        }]
    else:
        # Check if fragmentation is possible
        if total_payload_size < num_fragments * 8:
            max_possible = total_payload_size // 8
            print(f"\n Cannot divide into {num_fragments} fragments.")
            print(f" Maximum number of fragments possible (aligned to 8 bytes): {max_possible}")
            return

        fragment_payload_size = total_payload_size // num_fragments
        aligned_payload_size = fragment_payload_size - (fragment_payload_size % 8)

        if aligned_payload_size < 8:
            print("\n Fragment size too small after alignment. Each must be at least 8 bytes.")
            return

        # Begin fragmentation
        offset = 0
        remaining_payload = total_payload_size
        fragment_index = 0

        while remaining_payload > 0:
            if fragment_index == num_fragments - 1:
                frag_payload = remaining_payload  # last fragment takes the rest
            else:
                frag_payload = min(aligned_payload_size, remaining_payload)
            mf_flag = 1 if remaining_payload > frag_payload else 0

            fragments.append({
                "index": fragment_index + 1,
                "IP ID": ip_id,
                "Header": ip_header_size,
                "Payload": frag_payload,
                "Total": ip_header_size + frag_payload,
                "Flag": f"0{df_flag}{mf_flag}",
                "Offset": offset // 8,
                "Start": offset,
                "End": offset + frag_payload - 1
            })

            offset += frag_payload
            remaining_payload -= frag_payload
            fragment_index += 1

    # Display fragment info
    print(f"\n Total Fragments Created: {len(fragments)}\n")
    for frag in fragments:
        print(f"  Fragment {frag['index']}:")
        print(f"    IP ID: {frag['IP ID']}")
        print(f"    Header Size: {frag['Header']} bytes")
        print(f"    Payload Size: {frag['Payload']} bytes")
        print(f"    Total Fragment Size: {frag['Total']} bytes")
        print(f"    Flags (3-bit): {frag['Flag']}")
        print(f"    Fragment Offset: {frag['Start']} / 8 = {frag['Offset']} (in 8-byte units)")
        print(f"    First Byte Offset: {frag['Start']}")
        print(f"    Last Byte Offset:  {frag['End']}\n")

    # Visualization
    max_display = 30
    fig_height = max(5, min(20, len(fragments) * 0.4))

    fig, ax = plt.subplots(figsize=(12, fig_height))
    for i, frag in enumerate(fragments[:max_display]):
        ax.barh(y=i, width=frag['Payload'], left=frag['Start'], color='skyblue', edgecolor='black', label='Payload' if i==0 else "")
        ax.barh(y=i, width=frag['Header'], left=frag['Start'] - frag['Header'], color='orange', edgecolor='black', label='Header' if i==0 else "")
        ax.text(frag['Start'] + frag['Payload'] / 2, i, f"Frag {frag['index']}", ha='center', va='center', fontsize=8)

    ax.set_yticks(range(min(len(fragments), max_display)))
    ax.set_yticklabels([f"Frag {frag['index']}" for frag in fragments[:max_display]])
    ax.set_xlabel("Byte Offset")
    ax.set_title("Manual IP Fragmentation Visualization (showing first {} fragments)".format(min(len(fragments), max_display)))
    ax.legend()
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    if len(fragments) > max_display:
        print(f"\n Note: Only first {max_display} of {len(fragments)} fragments were visualized to keep the chart readable.")

if __name__ == "__main__":
    manual_fragmentation()