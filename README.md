# Title: pc-monitor: Your Web-Based PC Monitoring and Management Dashboard

**Key Features:**

*   **Real-time System Monitoring:**
    *   **CPU Usage:** See the current CPU load percentage, keeping you informed about resource-intensive processes.
    *   **GPU Monitoring:** Get detailed information about your graphics card(s), including their names, current load, temperature, and memory usage, ideal for tracking gaming or rendering performance.
    *   **RAM Status:**  View total, available and used RAM, helping you identify memory bottlenecks.
*   **Remote Desktop Preview:**
    *   **Live Screenshots:**  View live screenshots of your PC, displayed on the dashboard. You can see exactly what is happening on your screen(s), allowing for visual remote monitoring.
*   **Active Window Management:**
    *   **View Open Windows:** See a list of all currently open windows, including their titles and process IDs.
    *   **Process Termination:**  Forcefully end processes by selecting a process and clicking a button. This tool is useful for terminating unresponsive applications or controlling resource usage (use with caution). 
*   **Easy Web Access:**
    *   **Browser-Based:** Access `pc-monitor` via a web browser from any device on your local network, no installation is required.
    *   **Simple Interface:** The interface is designed to be clean and user-friendly for a simple way to check up on and remotely manage your PC.

**Important Considerations:**

*   **Local Network Only:** This application is designed for use within your local network only. It is not meant to be accessible directly from the Internet for security reasons.
*   **Security Notes:**
    *   This tool gives access to potentially sensitive information (like process names, screen contents) and the ability to terminate processes. It is important to be mindful of who has access to your network, as someone with access to the service via your network may use this tool to terminate any processes running on your machine.
    *   `pc-monitor` does **not** include any security features like password protection or user authentication. Use it in a trusted network environment only.
*   **Intended Use:** This tool is primarily intended for personal use and system administration within your own home or office network.
*   **Experimental:** This is a personal monitoring tool, it may have bugs or unexpected behaviour. This code is provided "as is" without warranty.

**Technical Notes:**

*   Developed using Python, Flask, and several libraries including `psutil`, `GPUtil`, `pyautogui`, `pygetwindow`, and `mss`.

**How to Use:**

1.  Run the Python script (`pc-monitor.py` or similar name).
2.  Open a web browser on another device on your local network - https://pcmon.vercel.app/.
3.  You should be able to access the monitoring dashboard.
