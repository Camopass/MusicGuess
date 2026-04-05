from imageio_ffmpeg import get_ffmpeg_exe
import subprocess
import shlex

def aac_to_ogg(input_path):
    ffmpeg = get_ffmpeg_exe()
    output_path = input_path.replace(".aac", ".ogg")

    cmd = f"{(shlex.quote(ffmpeg))} -y -i {shlex.quote(input_path)} -vn -c:a libvorbis -q:a 5 {shlex.quote(output_path)}"
    proc = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg error: {proc.stderr}")
    return output_path


# reimplementation of count_frames_and_seconds made to work with pure audio files
def get_length(path):
    """if isinstance(path, pathlib.PurePath):
        path = str(path)
    if not isinstance(path, str):
        raise TypeError("Video path must be a string or pathlib.Path.")

    cmd = [
        get_ffmpeg_exe(),
        "-i",
        path,
        "-map",
        "0:v:0?",
        "-vf",
        "null",
        "-f",
        "null",
        "-",
    ]
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, **_popen_kwargs())
    except subprocess.CalledProcessError as err:
        out = err.output.decode(errors="ignore")
        raise RuntimeError(
            "FFMPEG call failed with {}:\n{}".format(err.returncode, out)
        )

    # Note that other than with the subprocess calls below, ffmpeg won't hang here.
    # Worst case Python will stop/crash and ffmpeg will continue running until done.

    nframes = nsecs = None
    for line in reversed(out.splitlines()):
        if line.startswith(b"frame="):
            line = line.decode(errors="ignore")
            i = line.find("frame=")
            if i >= 0:
                s = line[i:].split("=", 1)[-1].lstrip().split(" ", 1)[0].strip()
                nframes = int(s)
            i = line.find("time=")
            if i >= 0:
                s = line[i:].split("=", 1)[-1].lstrip().split(" ", 1)[0].strip()
                nsecs = cvsecs(*s.split(":"))
            return nframes, nsecs

    raise RuntimeError("Could not get number of frames")  # pragma: no cover

def _popen_kwargs(prevent_sigint=False):
    startupinfo = None
    preexec_fn = None
    creationflags = 0
    if sys.platform.startswith("win"):
        # Stops executable from flashing on Windows (see #22)
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    if prevent_sigint:
        # Prevent propagation of sigint (see #4)
        # https://stackoverflow.com/questions/5045771
        if sys.platform.startswith("win"):
            creationflags = 0x00000200
        else:
            preexec_fn = os.setpgrp  # the _pre_exec does not seem to work

    falsy = ("", "0", "false", "no")
    if os.getenv("IMAGEIO_FFMPEG_NO_PREVENT_SIGINT", "").lower() not in falsy:
        # Unset preexec_fn to work around a strange hang on fork() (see #58)
        preexec_fn = None

    return {
        "startupinfo": startupinfo,
        "creationflags": creationflags,
        "preexec_fn": preexec_fn,
    }

def cvsecs(*args):
    converts a time to second. Either cvsecs(min, secs) or
    cvsecs(hours, mins, secs).

    if len(args) == 1:
        return float(args[0])
    elif len(args) == 2:
        return 60 * float(args[0]) + float(args[1])
    elif len(args) == 3:
        return 3600 * float(args[0]) + 60 * float(args[1]) + float(args[2])
"""
    return 30
