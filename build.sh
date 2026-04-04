#/usr/bin/bash

rm ./package/usr/bin/JLMP.py
cp JLMP.py ./package/usr/bin/JLMP.py

dpkg-deb --build package