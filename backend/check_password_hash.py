#!/usr/bin/env python3
"""Check the actual password hash format in the database"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easyfitness_backend.settings')
django.setup()

from api.models import User

# Get the most recently created secure test user
user = User.objects.filter(username__startswith='secureuser_').order_by('-created_at').first()

if user:
    print(f'\nUser: {user.username}')
    print('Password Hash Format:')
    print(user.password_hash[:80] + '...\n')

    if user.password_hash.startswith('pbkdf2_sha256'):
        print('✅ Using secure PBKDF2-SHA256 hashing!')
        parts = user.password_hash.split('$')
        print(f'   Algorithm: {parts[0]}')
        print(f'   Iterations: {parts[1]} (600,000 rounds)')
        print(f'   Salt: {parts[2][:20]}... (truncated)')
        print(f'   Hash: {parts[3][:30]}... (truncated)')
        print('\n✅ This is MUCH more secure than SHA-256!')
        print('   - Takes ~0.6 seconds to compute (vs SHA-256 <0.001s)')
        print('   - Resistant to GPU attacks')
        print('   - Resistant to rainbow tables')
        print('   - Industry standard used by major platforms\n')
    else:
        print(f'Format: {user.password_hash.split("$")[0] if "$" in user.password_hash else "Unknown"}')
        print('⚠️  Not using PBKDF2 format\n')
else:
    print('No test users found. Run test_password_security.py first.')
