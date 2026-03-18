import os, sys, subprocess, base64, functools, inspect

def clear_console(): os.system('cls')
class UnknownError(Exception): pass

def notify(text: str, title: str="EZtools Notification", icon_path: str=None):
    if sys.platform=="win32":
        text, title = text.replace('"', "'"), title.replace('"', "'")
        if icon_path and os.path.exists(icon_path): icon_line = f"$n.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon('{os.path.abspath(icon_path)}');"
        else: icon_line = "$n.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon((Get-Process -Id $PID).Path);"
        ps_code = f"""
        [reflection.assembly]::loadwithpartialname('System.Windows.Forms') | Out-Null;
        $n = New-Object System.Windows.Forms.NotifyIcon;
        {icon_line}
        $n.BalloonTipText = '{text}';
        $n.BalloonTipTitle = '{title}';
        $n.Visible = $True;
        $n.ShowBalloonTip(5000);
        Start-Sleep -Seconds 6;
        $n.Dispose();
        """
        utf16_code = ps_code.encode('utf-16-le')
        encoded_cmd = base64.b64encode(utf16_code).decode('utf-8')
        subprocess.Popen(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-EncodedCommand", encoded_cmd],
            creationflags=subprocess.CREATE_NO_WINDOW)
    else: raise Exception(f"Функция notify не доступна на платформе {sys.platform}")

def safe_run(output=True, *args, **kwargs):
    def decorator(func, *args, **kwargs):
        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if output: print(f"Функция {func.__name__} вызвала ошибку {e}")
                    return False
            return wrapper
        else:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if output: print(f"Функция {func.__name__} вызвала ошибку {e}")
                    return False
            return wrapper
    return decorator

def run_once(func):
    if inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if not getattr(wrapper, 'has_run', False):
                wrapper.has_run = True
                result = await func(*args, **kwargs)
                return result
            else: return
    else:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not getattr(wrapper, 'has_run', False):
                wrapper.has_run = True
                result = func(*args, **kwargs)
                return result
            return
    return wrapper