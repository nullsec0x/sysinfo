import psutil
import time
import platform
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.bar import Bar
from collections import deque
from random import choice

cpu_history = deque([0] * 30, maxlen=30)
cpu_cute_chars = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
cute_emojis = ["🐱", "🐶", "🦊", "🐻", "🐼", "🦁", "🐯", "🐨", "🐹", "🐰"]
current_emoji = choice(cute_emojis)

def get_system_info():
    global current_emoji
    if time.time() % 10 < 0.1:
        current_emoji = choice(cute_emojis)

    cpu_percent = psutil.cpu_percent(interval=None, percpu=True)
    cpu_overall = psutil.cpu_percent(interval=None)
    cpu_history.append(cpu_overall)

    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()

    disk_partitions = psutil.disk_partitions()
    disk_usage = {}
    for partition in disk_partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_usage[partition.mountpoint] = usage
        except PermissionError:
            continue
        except Exception as e:
            print(f"Error accessing disk {partition.mountpoint}: {e}")
            continue

    net_io_counters = psutil.net_io_counters()

    processes = []
    for proc in psutil.process_iter(["pid", "name", "username", "cpu_percent", "memory_percent"]):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
        except Exception as e:
            print(f"Error accessing process {proc.pid}: {e}")
            continue
    processes = sorted(processes, key=lambda x: x["cpu_percent"], reverse=True)[:10]

    return {
        "cpu_overall": cpu_overall,
        "cpu_per_core": cpu_percent,
        "memory": memory,
        "swap": swap,
        "disk_usage": disk_usage,
        "net_io_counters": net_io_counters,
        "processes": processes,
        "cpu_history": list(cpu_history),
        "emoji": current_emoji
    }

def generate_cpu_graph(history):
    graph = []
    max_value = max(history) if max(history) > 0 else 100
    for value in history[-20:]:
        scaled_value = min(int((value / max_value) * 7), 7)
        graph.append(cpu_cute_chars[scaled_value])
    return "".join(graph)

def generate_layout(info):
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1)
    )

    header_text = Text(f"{info['emoji']} System Monitor {info['emoji']}", style="bold magenta")
    layout["header"].update(Align.center(header_text, vertical="middle"))

    layout["main"].split_row(
        Layout(name="left_panel"),
        Layout(name="right_panel")
    )

    cpu_table = Table.grid(expand=True)
    cpu_table.add_column(justify="left")
    cpu_table.add_column(justify="right")
    cpu_table.add_row("CPU Overall:", f"{info['cpu_overall']:.1f}%")
    for i, core_percent in enumerate(info["cpu_per_core"]):
        cpu_table.add_row(f"  Core {i+1}:", f"{core_percent:.1f}%")

    cpu_graph = generate_cpu_graph(info["cpu_history"])
    cpu_graph_panel = Panel(
        Text(cpu_graph, style="bold green"),
        title="CPU History Graph",
        border_style="green",
        height=5
    )

    mem_used = info['memory'].used / info['memory'].total
    mem_indicator = "🟢" if mem_used < 0.7 else ("🟡" if mem_used < 0.9 else "🔴")

    mem_table = Table.grid(expand=True)
    mem_table.add_column(justify="left")
    mem_table.add_column(justify="right")
    mem_table.add_row(f"Memory {mem_indicator}:", f"{info['memory'].percent:.1f}% used")
    mem_table.add_row("", f"{round(info['memory'].used / (1024**3), 2)}GB / {round(info['memory'].total / (1024**3), 2)}GB")

    swap_used = info['swap'].used / info['swap'].total if info['swap'].total > 0 else 0
    swap_indicator = "🟢" if swap_used < 0.3 else ("🟡" if swap_used < 0.7 else "🔴")

    swap_table = Table.grid(expand=True)
    swap_table.add_column(justify="left")
    swap_table.add_column(justify="right")
    swap_table.add_row(f"Swap {swap_indicator}:", f"{info['swap'].percent:.1f}% used")
    swap_table.add_row("", f"{round(info['swap'].used / (1024**3), 2)}GB / {round(info['swap'].total / (1024**3), 2)}GB")

    layout["left_panel"].split(
        Panel(cpu_table, title="CPU Usage", border_style="green"),
        cpu_graph_panel,
        Panel(mem_table, title="Memory Usage", border_style="blue"),
        Panel(swap_table, title="Swap Usage", border_style="yellow"),
    )

    disk_table = Table(title="Disk Usage", border_style="cyan", show_header=True, header_style="bold")
    disk_table.add_column("Mountpoint")
    disk_table.add_column("Used %")
    disk_table.add_column("Used")
    disk_table.add_column("Total")
    for mountpoint, usage in info["disk_usage"].items():
        usage_percent = usage.percent / 100
        disk_indicator = "🟢" if usage_percent < 0.7 else ("🟡" if usage_percent < 0.9 else "🔴")
        disk_table.add_row(
            f"{disk_indicator} {mountpoint}",
            f"{usage.percent:.1f}%",
            f"{round(usage.used / (1024**3), 2)}GB",
            f"{round(usage.total / (1024**3), 2)}GB"
        )

    net_table = Table.grid(expand=True)
    net_table.add_column(justify="left")
    net_table.add_column(justify="right")
    net_table.add_row("📤 Bytes Sent:", f"{round(info['net_io_counters'].bytes_sent / (1024**2), 2)}MB")
    net_table.add_row("📥 Bytes Received:", f"{round(info['net_io_counters'].bytes_recv / (1024**2), 2)}MB")

    process_table = Table(title="Top 10 Processes by CPU", border_style="red", show_header=True, header_style="bold")
    process_table.add_column("PID")
    process_table.add_column("Name")
    process_table.add_column("CPU %")
    process_table.add_column("Mem %")
    for p in info["processes"]:
        process_emoji = "🔥" if p['cpu_percent'] > 50 else ("⚡" if p['cpu_percent'] > 20 else "🐌")
        process_table.add_row(
            str(p["pid"]),
            f"{process_emoji} {p['name']}",
            f"{p['cpu_percent']:.1f}%",
            f"{p['memory_percent']:.1f}%"
        )

    layout["right_panel"].split(
        Panel(disk_table, title="💾 Disk Usage", border_style="cyan"),
        Panel(net_table, title="🌐 Network I/O", border_style="magenta"),
        Panel(process_table, title="🖥️ Processes", border_style="red", height=15),
    )

    return layout

if __name__ == "__main__":
    system_os = platform.system()
    print(f"Running on: {system_os}")
    if system_os == "Windows":
        print("Ensure you are running this in a modern terminal like Windows Terminal or PowerShell for best display.")
    elif system_os == "Linux" or system_os == "Darwin":
        print("Ensure your terminal supports ANSI escape codes for best display.")

    with Live(generate_layout(get_system_info()), screen=True, refresh_per_second=4) as live:
        while True:
            info = get_system_info()
            live.update(generate_layout(info))
            time.sleep(1)
