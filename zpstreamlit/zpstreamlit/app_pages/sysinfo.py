import streamlit as st
from psutil import cpu_percent, virtual_memory, boot_time
from datetime import datetime
from time import time, sleep


def show_cpu(container):
    """Display the CPU times as a progress bar"""
    perc = cpu_percent()
    container.progress(perc / 100.0, f"CPU: {int(perc)}%")


def show_memory(container):
    """Display the memory usage as a progress bar"""
    memory = virtual_memory()
    perc = memory.percent
    container.progress(
        perc / 100.0,
        f"Memory: {int(perc)}% of {int(float(memory.total) / (1024**3))}GB",
    )


def show_buttons(container):
    """Adds a row of control buttons for system control."""
    button_width = 180
    suspend_, restart_, shutdown_ = container.columns(spec=[1, 1, 1], border=True)
    suspend_.button(
        "Suspend",
        on_click=lambda *args: print("Suspend"),
        args=("play_previous",),
        width=button_width,
    )
    restart_.button(
        "Restart", on_click=lambda *args: print("Restart"), width=button_width
    )
    shutdown_.button(
        "Shutdown",
        on_click=lambda *args: print("Shutdown"),
        width=button_width,
    )


def show_start_time(container):
    """Show the system startup time."""
    start_time = boot_time()
    display_time = datetime.fromtimestamp(start_time).strftime("%Y-%m-%d, %H:%M")
    time_diff = time() - start_time

    days = int(time_diff / (60 * 60 * 24))
    hours = int((time_diff / (60 * 60)) % 24)
    container.markdown(f"*Started:* {display_time}. *Uptime:* {days}d, {hours}h")


def get_sysinfo():
    """Show information and sleep, shutdown and restart buttons."""
    container = st.container()
    container.empty()
    container.image("images/cpu.jpg", width=128)
    container.markdown("# System Information")

    show_cpu(container)
    show_memory(container)
    show_start_time(container)
    show_buttons(container)

    while True:
        with container:
            sleep(1)
            st.rerun()
