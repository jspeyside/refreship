# RefreshIP
Automatically update your home IP in NS1.

Do you have a DHCP home IP address? Do you run any webservices at home and have your IP change on you?

If you use NS1 as your managed DNS service, you can use RefreshIP to automatically update your IP for you.
The updater will run every 5 minutes to detect any IP changes. It is recommended that you set the TTL for the DNS
record you wish updated to a low value such as `600s`.

## Example Usage
Start the updater with:
```
docker run -d -e NS1_API_KEY=abcdefghijklmnopqrst -e ZONE=example.com -e DOMAIN_NAME=example.com -e LOG_LEVEL=debug speyside/refreship
```

NS1_API_KEY is the key acquired from NS1 with permissions to "Manage Zones" and "View Zones"

ZONE is the name of NS1 Zone containing the record you wish to update

DOMAIN_NAME is the name of the NS1 record you wish to update. It is assumed to be an 'A' record

LOG_LEVEL is the verbosity of logging

