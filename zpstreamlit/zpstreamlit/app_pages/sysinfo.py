import streamlit as st
from psutil import cpu_percent, virtual_memory, boot_time
from datetime import datetime
from time import time, sleep


def show_cpu():
    """Display the CPU times as a progress bar"""
    perc = cpu_percent()
    st.progress(perc / 100.0, f"CPU: {int(perc)}%")


def show_memory():
    """Display the memory usage as a progress bar"""
    memory = virtual_memory()
    perc = memory.percent
    st.progress(
        perc / 100.0,
        f"Memory: {int(perc)}% of {int(float(memory.total) / (1024**3))}GB",
    )


def show_start_time():
    """Show the system startup time."""
    start_time = boot_time()
    display_time = datetime.fromtimestamp(start_time).strftime("%Y-%m-%d, %H:%M")
    time_diff = time() - start_time

    days = int(time_diff / (60 * 60 * 24))
    hours = int((time_diff / (60 * 60)) % 24)
    st.markdown(f"*Started:* {display_time}. *Uptime:* {days}d, {hours}h")


def get_sysinfo():
    """Show information and sleep, shutdown and restart buttons."""
    st.empty()
    st.image("images/cpu.jpg", width=128)
    st.markdown("# System Information")

    show_cpu()
    show_memory()
    show_start_time()

    placeholder = st.empty()
    while True:
        with placeholder.container():
            sleep(1)
            st.rerun()
