import oci
import getpass

# =========================
# CONFIGURATION
# =========================
CONFIG_FILE = "~/.oci/config"
PROFILE = "DEFAULT"

config = oci.config.from_file(CONFIG_FILE, PROFILE)
config["pass_phrase"] = getpass.getpass("Enter passphrase for your OCI key (press Enter if none): ")

target_ip = input("Enter Load Balancer IP address (private or public): ").strip()
print(f"\n🔍 Searching for CLASSIC Load Balancer with IP: {target_ip} in ALL compartments...")

# Initialize clients
identity_client = oci.identity.IdentityClient(config)
lb_client = oci.load_balancer.LoadBalancerClient(config)

tenancy_id = config["tenancy"]

# =========================
# 1️⃣ Get all compartments (recursive)
# =========================
def list_all_compartments(client, tenancy_id):
    """Return all compartments (including sub-compartments)"""
    compartments = []
    response = client.list_compartments(
        tenancy_id, compartment_id_in_subtree=True, access_level="ACCESSIBLE"
    )
    compartments.extend(response.data)
    return compartments

compartments = list_all_compartments(identity_client, tenancy_id)
compartments.append(identity_client.get_tenancy(tenancy_id).data)  # include root tenancy

print(f"📦 Found {len(compartments)} compartments to search.\n")

found = False

# =========================
# 2️⃣ Search Classic Load Balancers
# =========================
for compartment in compartments:
    try:
        lbs = lb_client.list_load_balancers(compartment_id=compartment.id).data
    except Exception:
        continue

    for lb in lbs:
        details = lb_client.get_load_balancer(lb.id).data
        for ip in details.ip_addresses:
            if ip.ip_address == target_ip:
                found = True
                print(f"\n✅ Found CLASSIC Load Balancer in: {compartment.name}")
                print(f"Name: {details.display_name}")
                print(f"Shape: {details.shape_name}")
                print(f"Private: {details.is_private}")
                print(f"Lifecycle: {details.lifecycle_state}")
                print(f"Time Created: {details.time_created}")
                print(f"Subnet IDs: {details.subnet_ids}\n")

                # 🎧 Listeners (L4 vs L7)
                print("🎧 Listeners:")
                for name, listener in details.listeners.items():
                    proto = listener.protocol.upper()
                    layer = "L7" if proto in ["HTTP", "HTTPS"] else "L4"
                    print(f" - {name}: {proto} ({layer}) on port {listener.port}")

                # 🖥️ Backend Sets and Backends
                print("\n🖥️ Backend Sets:")
                for bs_name, bs in details.backend_sets.items():
                    print(f"  Backend Set: {bs_name}")
                    hc = bs.health_checker
                    print(f"   Health Checker: {hc.protocol}:{hc.port} (url: {hc.url_path})")
                    for backend in bs.backends:
                        ip = getattr(backend, "ip_address", "N/A")
                        port = getattr(backend, "port", "N/A")
                        print(f"    → {ip}:{port}")
                break
        if found:
            break
    if found:
        break

if not found:
    print("\n⚠️ No Classic Load Balancer found with that IP in any compartment.")
else:
    print("\n✅ Done — details displayed above.")
