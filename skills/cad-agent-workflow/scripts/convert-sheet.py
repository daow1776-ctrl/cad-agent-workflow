from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path
import subprocess


def text_for_console(path: Path) -> str:
    return '"' + str(path) + '"'


def run_core(exe: Path, source: Path, commands: list[str], job: Path, phase: str,
             language: str, profile_id: str, profile: Path) -> str:
    script = job / f"{phase}.scr"
    log = job / f"{phase}.log"
    script.write_bytes(("\r\n".join(commands) + "\r\n").encode("gb18030" if language == "zh-CN" else "ascii"))
    args = [str(exe), "/isolate", profile_id, str(profile), "/i", str(source),
            "/s", str(script), "/l", language]
    try:
        result = subprocess.run(
            args, input=b"", stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=45, cwd=job, creationflags=subprocess.CREATE_NO_WINDOW,
        )
    except subprocess.TimeoutExpired as error:
        log.write_bytes(error.stdout or b"")
        raise RuntimeError(f"Core Console timeout, partial output at {log}") from error
    raw = result.stdout
    encoding = "utf-16le" if b"\x00" in raw[:200] else "gb18030"
    output = raw.decode(encoding, errors="replace")
    log.write_text(output, encoding="utf-8")
    if result.returncode:
        raise RuntimeError(f"Core Console exited {result.returncode}, see {log}")
    return output


def model_counts() -> list[str]:
    return [
        '(progn (setq qa-types \'("LINE" "CIRCLE" "ARC" "LWPOLYLINE" "DIMENSION" "LEADER" "MTEXT" "TEXT")) (foreach qa-type qa-types (setq qa-ss (ssget "_X" (list (cons 0 qa-type) (cons 410 "Model")))) (princ (strcat "\\nQA_" qa-type "=" (itoa (if qa-ss (sslength qa-ss) 0))))) (princ))',
        '(progn (princ (strcat "\\nQA_INSUNITS=" (itoa (getvar "INSUNITS")))) (princ))',
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="AutoCAD Core Console DWG conversion and optional A4 PDF plot.")
    parser.add_argument("source", type=Path, help="Input DXF with a millimeter Model-space drawing")
    parser.add_argument("job", type=Path, help="Separate job directory for outputs and logs")
    parser.add_argument("--exe", type=Path, required=True, help="Path to the installed AutoCAD Core Console executable")
    parser.add_argument("--language", default="zh-CN")
    parser.add_argument("--pdf", action="store_true", help="Plot model-space window (0,0)–(297,210) at 1:1")
    parser.add_argument("--basename", help="Destination stem; defaults to the input stem")
    parser.add_argument("--profile", type=Path, required=True, help="Existing directory for the isolated console profile")
    parser.add_argument("--profile-id", default="CadAgentWorkflow")
    args = parser.parse_args()

    source = args.source.absolute()
    job = args.job.absolute()
    profile = args.profile.absolute()
    if source.suffix.lower() != ".dxf" or not source.is_file():
        parser.error("the source must be an existing .dxf")
    if not profile.is_dir():
        parser.error("the isolated profile directory must exist")
    job.mkdir(parents=True, exist_ok=True)
    basename = args.basename or source.stem
    if Path(basename).name != basename or basename in (".", ".."):
        parser.error("basename must be a single filename stem")
    dwg = job / f"{basename}.dwg"
    pdf = job / f"{basename}.pdf"
    if dwg.exists() or (args.pdf and pdf.exists()):
        parser.error("choose a fresh output name or job folder")
    source_digest = hashlib.sha256(source.read_bytes()).digest()
    commands = [
        "_FILEDIA", "0", "_ISAVEPERCENT", "0", "_TILEMODE", "1",
        "_.ZOOM", "_W", "0,0", "297,210",
        "_.SAVEAS", "2018", text_for_console(dwg),
        *model_counts(),
    ]
    if args.pdf:
        commands.extend([
            "_BACKGROUNDPLOT", "0",
            "_.-PLOT", "_Y", "", "DWG To PDF.pc3",
            ("ISO full bleed A4 (297.00 x 210.00 毫米)" if args.language == "zh-CN"
             else "ISO full bleed A4 (297.00 x 210.00 MM)"), "_M", "_L", "_N",
            "_W", "0,0", "297,210", "1=1", "_C",
            "_Y", "monochrome.ctb", "_Y", "_A",
            text_for_console(pdf), "_N", "_Y",
        ])
    commands.extend(["_.QUIT", "_Y", ""])
    output = run_core(args.exe.absolute(), source, commands, job, "native-convert",
                      args.language, args.profile_id, profile)
    if not dwg.is_file() or dwg.read_bytes()[:6] != b"AC1032":
        raise RuntimeError(f"Missing native DWG output {dwg}, see native-convert.log")
    if args.pdf and (not pdf.is_file() or not pdf.read_bytes().startswith(b"%PDF-")):
        raise RuntimeError(f"Missing PDF output {pdf}, see native-convert.log")
    if hashlib.sha256(source.read_bytes()).digest() != source_digest:
        raise RuntimeError("Source DXF changed")

    reopened = run_core(
        args.exe.absolute(), dwg, [*model_counts(), "_.AUDIT", "_N", "_.QUIT", "_Y", ""],
        job, "native-reopen", args.language, args.profile_id, profile,
    )
    converted = {line.strip() for line in output.splitlines() if line.startswith("QA_")}
    round_trip = {line.strip() for line in reopened.splitlines() if line.startswith("QA_")}
    if len(converted) < 9 or converted != round_trip:
        raise RuntimeError(f"Model entity counts differ: {sorted(converted)} vs {sorted(round_trip)}")
    if "QA_INSUNITS=4" not in round_trip:
        raise RuntimeError("Reopened DWG is not in millimeters")
    audit_patterns = (r"共发现\s+0\s+个错误", r"Total errors found\s+0\b")
    if not any(re.search(pattern, reopened, re.IGNORECASE) for pattern in audit_patterns):
        raise RuntimeError("Native AUDIT did not confirm zero errors, see native-reopen.log")
    print(dwg)
    if args.pdf:
        print(pdf)
    print("\n".join(sorted(round_trip)))


if __name__ == "__main__":
    main()

