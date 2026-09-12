import asyncio
from mac_vendor_lookup import AsyncMacLookup

async def main():
    mac_lookup = AsyncMacLookup()
    await mac_lookup.update_vendors()
    print("Vendor database updated.")

asyncio.run(main())
