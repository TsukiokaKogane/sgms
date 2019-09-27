# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['manage.py'],
             pathex=['D:\\Program\\DBE\\DBE'],
             binaries=[],
             datas=[],
             hiddenimports=[
              'django.contrib.admin',
    			'django.contrib.auth',
    			'django.contrib.contenttypes',
    		'django.contrib.sessions',
    		'django.contrib.messages',
    		'django.contrib.staticfiles',
    		'default',
    		'django.middleware.security.SecurityMiddleware',
    		'django.contrib.sessions.middleware.SessionMiddleware',
    		'django.middleware.common.CommonMiddleware',
    		'django.middleware.csrf.CsrfViewMiddleware',
    		'django.contrib.auth.middleware.AuthenticationMiddleware',
   		 'django.contrib.messages.middleware.MessageMiddleware',
    		'django.middleware.clickjacking.XFrameOptionsMiddleware',
    		'django.template.backends.django.DjangoTemplates',
    		  'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
                'django.contrib.auth.password_validation.MinimumLengthValidator',
                'django.contrib.auth.password_validation.CommonPasswordValidator',
                'django.contrib.auth.password_validation.NumericPasswordValidator',

             ],
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
          [],
          exclude_binaries=True,
          name='manage',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='manage')
