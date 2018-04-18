#!/bin/sh

# YES THIS IS UGLY AS FUCK
# If you want to know more about why we're doing this, contact me directly,
# we'll need a beer.

impacted_files="passwd group shadow"

for file in ${impacted_files}
do
  cp /etc/${file} /etc/${file}.original
  cp /host_etc/${file} /etc/${file}
done

/usr/sbin/useradd $@

for file in ${impacted_files}
do
  cp /etc/${file} /host_etc/${file}
  cp /etc/${file}.original /etc/${file}
done
