#/usr/bin/bash

rm ./package/usr/lib/python3/dist-packages/JLMP.py
cp JLMP.py ./package/usr/lib/python3/dist-packages/JLMP.py

dpkg-deb --build package