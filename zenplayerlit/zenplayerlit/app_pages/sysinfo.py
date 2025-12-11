import streamlit as st
from psutil import cpu_percent, virtual_memory, boot_time, disk_usage
from datetime import datetime
from time import time
import subprocess


class System:
    """Perform various system commands."""

    @staticmethod
    def shutdown():
        subprocess.run(["/usr/bin/shutdown", "now"], text=True)

    @staticmethod
    def sleep():
        subprocess.run(["/usr/bin/systemctl", "suspend"], text=True)

    @staticmethod
    def restart():
        subprocess.run(["/usr/bin/reboot"], text=True)

    @staticmethod
    def lock_screen():
        subprocess.run(["loginctl", "lock-session"], text=True)


class SysInfo:
    @staticmethod
    def show_cpu():
        """Display the CPU times as a progress bar"""
        perc = cpu_percent()
        st.progress(perc / 100.0, f"CPU: {int(perc)}%")

    @staticmethod
    def show_memory():
        """Display the memory usage as a progress bar"""
        memory = virtual_memory()
        perc = memory.percent
        st.progress(
            perc / 100.0,
            f"Memory: {int(perc)}% of {int(float(memory.total) / (1024**3))}GB",
        )

    @staticmethod
    def show_buttons():
        """Adds a row of control buttons for system control."""
        button_width = "stretch"
        lock_, suspend_, restart_, shutdown_ = st.columns(
            spec=[1, 1, 1, 1], border=True
        )
        lock_.button(
            "Lock",
            on_click=System.lock_screen,
            icon=":material/lock:",
            width=button_width,
        )
        suspend_.button(
            "Suspend",
            on_click=System.sleep,
            icon=":material/content_copy:",
            width=button_width,
        )
        restart_.button(
            "Restart",
            on_click=System.restart,
            width=button_width,
            icon=":material/restart_alt:",
        )
        shutdown_.button(
            "Shutdown",
            on_click=System.shutdown,
            icon=":material/power_settings_new:",
            width=button_width,
        )

    @staticmethod
    def show_start_time():
        """Show the system startup time."""
        start_time = boot_time()
        display_time = datetime.fromtimestamp(start_time).strftime("%d %B, %Y, %H:%M")
        time_diff = time() - start_time

        days = int(time_diff / (60 * 60 * 24))
        hours = int((time_diff / (60 * 60)) % 24)
        st.markdown(f"**Uptime:** {days}d {hours}h")
        st.markdown(f"**Started:** {display_time}")

        now = datetime.now().strftime("%d %B, %Y, %H:%M:%S")
        st.markdown(f"**Now:** {now}")

    @staticmethod
    def show_disk():
        usage = disk_usage("/")
        st.progress(
            usage.percent / 100.0,
            f"Disc usage (/): {int(usage.percent)}% of {usage.total / (1024**3):.2f} GB",
        )


def show_sysinfo():
    """Show information and sleep, shutdown and restart buttons."""

    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        st.image("images/cpu.jpg", width=128)
    with col1:
        st.markdown("# System Information")

    SysInfo.show_cpu()
    SysInfo.show_memory()
    SysInfo.show_disk()
    st.divider()
    SysInfo.show_start_time()
    SysInfo.show_buttons()
