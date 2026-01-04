#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import os

from sdk import CafeSDK


async def run():
    try:
        # 1. Get params
        input_json_dict = CafeSDK.Parameter.get_input_json_dict()
        CafeSDK.Log.debug(f"params: {input_json_dict}")

        # 2. proxy configuration
        proxyDomain = "proxy-inner.cafescraper.com:6000"

        try:
            proxyAuth = os.environ.get("PROXY_AUTH")
            CafeSDK.Log.info(f"Proxy authentication information: {proxyAuth}")
        except Exception as e:
            CafeSDK.Log.error(f"Failed to retrieve proxy authentication information: {e}")
            proxyAuth = None

        # 3. Construct the proxy URL
        proxy_url = f"socks5://{proxyAuth}@{proxyDomain}" if proxyAuth else None
        CafeSDK.Log.info(f"Proxy address: {proxy_url}")

        # 4. TODO: Handle business logic
        url = input_json_dict.get('url')
        CafeSDK.Log.info(f"start deal URL: {url}")

        # Simulate business processing results
        result = {
            "url": url,
            "status": "success",
            "data": {
                "title": "Sample title",
                "content": "Sample content",
                # ... Other fields
            }
        }

        # 5. Push result data
        CafeSDK.Log.info(f"Processing result: {result}")
        CafeSDK.Result.push_data(result)

        # 6. Set the table headers (if table output is needed)
        headers = [
            {
                "label": "URL",
                "key": "url",
                "format": "text",
            },
            # ... Other table header configurations
        ]
        res = CafeSDK.Result.set_table_header(headers)

        CafeSDK.Log.info("Script execution completed")

    except Exception as e:
        CafeSDK.Log.error(f"Script execution error: {e}")
        error_result = {
            "error": str(e),
            "error_code": "500",
            "status": "failed"
        }
        CafeSDK.Result.push_data(error_result)
        raise


if __name__ == "__main__":
    asyncio.run(run())