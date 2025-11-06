# 🧭 OCI Load Balancer Discovery Toolkit

A lightweight, **read-only** Python toolkit for exploring and analyzing **Oracle Cloud Infrastructure (OCI)** Classic Load Balancers using the official OCI Python SDK.

---

## 📘 Overview

These utilities let you:

- 🔑 Authenticate securely with OCI using an API key  
- 📦 List all accessible compartments in your tenancy  
- 🌐 Discover Classic Load Balancers by compartment or IP address  
- 🧩 Identify listener protocol level (**L4 TCP / L7 HTTP or HTTPS**)  
- 🖥️ List backend IPs and ports  
- 🧯 Operate entirely in **read-only mode** — safe for production environments  

---

## 🧰 Requirements

- **Python 3.8+**
- **OCI Python SDK**
- *(Optional)* Pandas and Matplotlib for analysis or visualization

Install dependencies:

```bash
pip install oci pandas matplotlib
```

---

## ⚙️ Configuration

Create or verify your OCI configuration file at:

```
~/.oci/config
```

Example:

```ini
[DEFAULT]
user=ocid1.user.oc1..aaaaaaaaxxxxxxxx
fingerprint=aa:bb:cc:dd:ee:ff:11:22
tenancy=ocid1.tenancy.oc1..aaaaaaaayyyyyyyy
region=eu-frankfurt-1
key_file=/home/user/.oci/oci_api_key.pem
```

If your private key is encrypted, the scripts will securely prompt for its **passphrase** at runtime.

---

## 🚀 Scripts

### 1️⃣ List Compartments
`list_compartments_with_passphrase.py`

Lists all compartments visible to your OCI API key (read-only).

### 2️⃣ List Load Balancers by Compartment
`list_load_balancers_by_compartment.py`

Lists Classic Load Balancers in a selected compartment.

### 3️⃣ Find Load Balancer by IP
`OCI-Fetch-LB-Full-Details-Using-IP.py`

Finds which Load Balancer owns a specific IP, and shows listeners + backends.

---

## 🔒 Security

All scripts use only read-only OCI SDK operations and are safe to run in production.

| SDK Method | Description | Safe |
|-------------|--------------|------|
| list_compartments() | List visible compartments | ✅ |
| list_load_balancers() | List Classic Load Balancers | ✅ |
| get_load_balancer() | Get LB details | ✅ |
| get_private_ip() | Resolve private IPs | ✅ |

IAM policies (minimal example):

```text
Allow group read-only-users to read compartments in tenancy
Allow group read-only-users to read load-balancers in tenancy
Allow group read-only-users to read virtual-network-family in tenancy
```

---

## ⚙️ Quick Setup (Local or Virtual Environment)

### 1️⃣ Clone this repository

```bash
git clone https://github.com/<your-username>/oci-lb-toolkit.git
cd oci-lb-toolkit
```

### 2️⃣ Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # On Linux/macOS
venv\Scripts\activate         # On Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure your OCI credentials

Ensure you have a valid config file at `~/.oci/config`.

### 5️⃣ Run the tools

```bash
python list_compartments_with_passphrase.py
python list_load_balancers_by_compartment.py
python OCI-Fetch-LB-Full-Details-Using-IP.py
```

---

🧱 **All scripts are read-only and safe for production.**
