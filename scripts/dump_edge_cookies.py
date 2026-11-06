import ctypes
import os
import sqlite3

def copy_locked_file(src, dst):
    from ctypes import wintypes
    kernel32 = ctypes.windll.kernel32
    GENERIC_READ = 0x80000000
    FILE_SHARE_READ = 0x00000001
    FILE_SHARE_WRITE = 0x00000002
    FILE_SHARE_DELETE = 0x00000004
    OPEN_EXISTING = 3
    FILE_ATTRIBUTE_NORMAL = 0x80

    handle = kernel32.CreateFileW(
        src,
        GENERIC_READ,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
        None,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        None
    )
    if handle == -1 or handle == 0xFFFFFFFFFFFFFFFF:
        err = ctypes.GetLastError()
        raise Exception(f"CreateFileW failed with error {err}")

    buffer_size = 64 * 1024
    buf = ctypes.create_string_buffer(buffer_size)
    bytes_read = wintypes.DWORD()

    with open(dst, 'wb') as out_f:
        while True:
            success = kernel32.ReadFile(handle, buf, buffer_size, ctypes.byref(bytes_read), None)
            if not success or bytes_read.value == 0:
                break
            out_f.write(buf.raw[:bytes_read.value])

    kernel32.CloseHandle(handle)

cookie_path = os.path.expanduser(r'~\AppData\Local\Microsoft\Edge\User Data\Default\Network\Cookies')
dst = 'temp_cookies.sqlite'

try:
    copy_locked_file(cookie_path, dst)
    print("Copied cookies database successfully!")
    conn = sqlite3.connect(dst)
    c = conn.cursor()
    c.execute("SELECT host_key, name, value, path, expires_utc FROM cookies WHERE host_key LIKE '%capivara%'")
    rows = c.fetchall()
    print(f"Found {len(rows)} cookies for capivara:")
    for r in rows:
        print(" ", r)
    conn.close()
    if os.path.exists(dst):
        os.remove(dst)
except Exception as e:
    print("Error:", e)
