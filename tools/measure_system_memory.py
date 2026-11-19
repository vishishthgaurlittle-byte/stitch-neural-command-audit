import ctypes
import subprocess
import json

class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ('dwLength', ctypes.c_ulong),
        ('dwMemoryLoad', ctypes.c_ulong),
        ('ullTotalPhys', ctypes.c_ulonglong),
        ('ullAvailPhys', ctypes.c_ulonglong),
        ('ullTotalPageFile', ctypes.c_ulonglong),
        ('ullAvailPageFile', ctypes.c_ulonglong),
        ('ullTotalVirtual', ctypes.c_ulonglong),
        ('ullAvailVirtual', ctypes.c_ulonglong),
        ('ullAvailExtendedVirtual', ctypes.c_ulonglong),
    ]

stat = MEMORYSTATUSEX()
stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))

total_phys = stat.ullTotalPhys
avail_phys = stat.ullAvailPhys
in_use_phys = total_phys - avail_phys
commit_total = stat.ullTotalPageFile
commit_avail = stat.ullAvailPageFile
commit_used = commit_total - commit_avail

print("=== LIVE HOST MEMORY STATE ===")
print(f"Total Visible Physical RAM: {total_phys:,} B ({total_phys/(1024**2):.2f} MiB / {total_phys/(1024**3):.4f} GiB)")
print(f"Available Physical RAM:     {avail_phys:,} B ({avail_phys/(1024**2):.2f} MiB / {avail_phys/(1024**3):.4f} GiB)")
print(f"In-Use Physical RAM:        {in_use_phys:,} B ({in_use_phys/(1024**2):.2f} MiB / {in_use_phys/(1024**3):.4f} GiB)")
print(f"System Commit Limit:        {commit_total:,} B ({commit_total/(1024**2):.2f} MiB / {commit_total/(1024**3):.4f} GiB)")
print(f"System Commit Used:         {commit_used:,} B ({commit_used/(1024**2):.2f} MiB / {commit_used/(1024**3):.4f} GiB)")
print(f"System Commit Available:    {commit_avail:,} B ({commit_avail/(1024**2):.2f} MiB / {commit_avail/(1024**3):.4f} GiB)")
print(f"dwMemoryLoad:               {stat.dwMemoryLoad}%")

# Query Win32_OperatingSystem for pools
ps_script = """
Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory, TotalVirtualMemorySize, FreeVirtualMemory, SizeStoredInPagingFiles | ConvertTo-Json
"""
res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], capture_output=True, text=True)
print("\n=== Win32_OperatingSystem ===")
print(res.stdout)

# Query Performance Counters for pools and cache
ps_script_perf = """
Get-Counter -Counter @(
    "\\Memory\\Pool Nonpaged Bytes",
    "\\Memory\\Pool Paged Bytes",
    "\\Memory\\Standby Cache Normal Priority Bytes",
    "\\Memory\\Standby Cache Reserve Bytes",
    "\\Memory\\Standby Cache Core Bytes",
    "\\Memory\\Modified Page List Bytes",
    "\\Memory\\Cache Bytes"
) | Select-Object -ExpandProperty CounterSamples | Select-Object Path, CookedValue | Format-Table -AutoSize
"""
res_perf = subprocess.run(["powershell", "-NoProfile", "-Command", ps_script_perf], capture_output=True, text=True)
print("\n=== Memory Performance Counters ===")
print(res_perf.stdout)
