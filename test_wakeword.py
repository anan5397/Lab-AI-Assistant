import openwakeword
import os

package_dir = os.path.dirname(openwakeword.__file__)
print(package_dir)

for root, dirs, files in os.walk(package_dir):
    if files:
        print(root)
        print(files[:5])