#!/usr/bin/env python3
"""将本仓与完整精确 gitlink 源码打包为确定性 Mbed TLS 4.1.0 完整源归档。"""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
import tarfile
import io
import hashlib

def git(root: Path, *args: str) -> str:
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()

def collect(root: Path, prefix: str = '') -> dict[str, tuple[Path, int]]:
    if git(root, 'status', '--porcelain', '--untracked-files=normal'):
        raise ValueError(f'源码必须干净：{prefix or "."}')
    if git(root, 'rev-parse', '--is-shallow-repository') != 'false':
        raise ValueError('源码必须是完整 Git clone')
    files = {}
    for line in git(root, 'ls-files', '--stage').splitlines():
        index, path = line.split('\t', 1)
        mode, sha, stage = index.split()
        if stage != '0':
            raise ValueError('源码索引存在未解决冲突')
        file = root / path
        if mode == '160000':
            if not (file / '.git').exists() or git(file, 'rev-parse', 'HEAD') != sha:
                raise ValueError(f'子来源未完整匹配：{prefix + path}')
            files.update(collect(file, prefix + path + '/'))
        elif mode in ('100644', '100755'):
            files[prefix + path] = (file, 0o755 if mode == '100755' else 0o644)
        elif mode == '120000':
            files[prefix + path] = (file, 0o777)
        else:
            raise ValueError(f'不支持的 Git 文件模式：{mode}')
    return files

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.output.exists():
        raise ValueError('输出必须是新路径')
    files = collect(root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(args.output, 'w:bz2', format=tarfile.PAX_FORMAT) as archive:
        for rel, (file, mode) in sorted(files.items()):
            item = tarfile.TarInfo('mbedtls-4.1.0/' + rel)
            item.mode = mode
            item.mtime = 0
            item.uid = item.gid = 0
            item.uname = item.gname = ''
            if file.is_symlink():
                item.type = tarfile.SYMTYPE
                item.linkname = file.readlink().as_posix()
                archive.addfile(item)
            else:
                data = file.read_bytes()
                item.size = len(data)
                archive.addfile(item, io.BytesIO(data))
    print('Mbed TLS 源归档\n  结果  已生成完整确定性源归档\n'
          f'  文件  {args.output}\n  SHA-256  {hashlib.sha256(args.output.read_bytes()).hexdigest()}')

if __name__ == '__main__':
    main()
