### Required Files (Located in the Project Root Directory)

``` 
├── main.py
├── requirements.txt
├── input_schema.json
├── README.md
├── sdk.py
├── sdk_pd2.py
├── sdk_pd2_grpc.py

```
| File Name                 | Description                        |
| --------------------- | ------------------------- |
| **`main.py`**           | Script entry file (execution entry point), uniformly named `main` |
| **`requirements.txt`**  | Python dependency management file            |
| **`input_schema.json`** | UI input form configuration file              |
| **`README.md`**         | Project documentation file                  |
| **`sdk.py`**            | SDK core functionality     |
| **`sdk_pd2.py`**        |Enhanced data processing module    |
| **`sdk_pd2_grpc.py`**   | Network communication module|


# ⭐ Core SDK Files for Scripts

### 📁 File Description

The following are three important SDK files that must be placed in the root directory of your script:

| **File Name** | **Core Functionality** |
| --- | --- |
| `sdk.py` | Basic functional modules |
| `sdk_pd2.py` | Enhanced data processing module |
| `sdk_pd2_grpc.py` | Network communication module |

These three files form the "toolkit" for your script, providing all core functionalities required for interacting with the mid-platform system and running web crawlers.

## 🔧 Core Function Usage Guide

### 1. Environment Parameter Retrieval - Get Configuration at Script Startup

When a script starts, you can pass external configuration parameters (e.g., target website URL, search keywords). Use the following method to retrieve these parameters:

```python
# Retrieve all incoming parameters and return them as a dictionary.
parameters = SDK.Parameter.get_input_json_dict()

# Example: Assume a website URL and keywords are provided as input.
# return：{"website": "example.com", "keyword": "news"}
```

**Use Case**：For example, if you need to scrape data from different websites for different tasks, you can achieve this by passing different parameters without modifying the code.

---

### 2. Run log - record the script execution process

During script execution, you can log information at different levels. These logs will be displayed in the mid-platform interface, facilitating status monitoring and troubleshooting:

```python
SDK.Log.debug("Connecting to the target website...")

SDK.Log.info("Successfully retrieved 10 news items.")

SDK.Log.warn("The network connection is slow, which may affect the data collection speed.")

SDK.Log.error("Unable to access the target website. Please check your network connection.")
```
# Log Level Explanation:
- **debug**: Most detailed debugging information, suitable for development
- **info**: Normal process logging, recommended for key steps
- **warn**: Warning messages indicating potential issues that don't stop execution
- **error**: Error messages indicating critical issues requiring attention
---

### 3.Result Return - Send Scraped Data to Mid-Platform

After scraping data, return it to the mid-platform system by following these two steps:

#### Step 1: Set Table Headers (Mandatory First Step)

Before pushing actual data, define the table structure (similar to setting column headers in Excel):

```python
# Define the table column structure.
headers = [
    {
        "label": "News title",      # column name
        "key": "title",          # column key
        "format": "text",        # Data type：text
    },
    {
        "label": "Publish time",
        "key": "publish_time",  
        "format": "text",
    },
    {
        "label": "News category",
        "key": "category",
        "format": "text",
    },
]

# set header
res = CafeSDK.Result.set_table_header(headers)
```

**Field Explanation:**：

- **label**：Column header displayed in the table (user-visible, Chinese recommended)
- **key**：Unique identifier for data (used in code, lowercase English with underscores recommended)
- **format**：Data type supporting the following formats:
    - `"text"`：Text/string
    - `"integer"`：Integer
    - `"boolean"`：Yes/No (Boolean)
    - `"array"`：Array/list
    - `"object"`：Object/dictionary

#### Step 2: Push Data Entry by Entry

After setting headers, start pushing scraped data:

```python
# News date
news_data = [
    {"title": "New breakthroughs in artificial intelligence", "publish_time": "2023-10-01", "category": "Technology"},
    {"title": "Today's stock market trends", "publish_time": "2023-10-01", "category": "Finance"},
    # ... more
]

# push data
for i, news in enumerate(news_data):
    obj = {
        "title": news.get('title'),          
        "publish_time": news.get('publish_time'), 
        "category": news.get('category'),
    }

    res = CafeSDK.Result.push_data(obj)

    # Record the push results
    SDK.Log.info(f"Data item {i+1}：{news.get('title')}")
```

**Important Reminders:**：

1. The order of setting headers and pushing data can be reversed.
2. Keys in the pushed data dictionary must exactly match those defined in headers
3. Data must be pushed entry by entry (bulk push not supported)
4. It is recommended to log after each push to track execution progress

---

### 💡 Complete Code Example

The following is a full script example demonstrating the complete workflow from parameter retrieval to data return:

```python
# 1. Retrieve startup parameters
config = SDK.Parameter.get_input_json_dict()
website = config.get("website", "Default website")
SDK.Log.info(f"Start collecting data from the website：{website}")

# 2. Set the result table header
headers = [
    {"label": "Title", "key": "title", "format": "text"},
    {"label": "Time", "key": "publish_time", "format": "text"},
    {"label": "Category", "key": "category", "format": "text"},
    {"label": "View count", "key": "view_count", "format": "integer"},
]
CafeSDK.Result.set_table_header(headers)

# 3. Simulate data collection (in practice, this could be web scraping code)
collected_data = [
    {"title": "Sample News 1", "publish_time": "2023-10-01 10:00", "category": "Technology", "view_count": 1000},
    {"title": "Sample News 2", "publish_time": "2023-10-01 11:00", "category": "Finance", "view_count": 500},
]

# 4. Push data
for data in collected_data:
    obj = {
        "title": data.get("title"),
        "publish_time": data.get("publish_time"),
        "category": data.get("category"),
        "view_count": data.get("view_count", 0),  # Provide a default value of 0
    }
    res = CafeSDK.Result.push_data(obj)

# 5. Completed
SDK.Log.info("Data collection task completed！")
```

---

### ⚠️ Common Issues & Notes

1. **File Location**： Ensure the three `SDK` files are placed in the script's **root directory** (folder containing the main file)
2. **Import Method**：Directly use `SDK` or `CafeSDK` in code to call related functions
3. **键名一致**：Keys used for pushing data must exactly match (**including case**) those defined in headers
4. **错误处理**： It is recommended to check return results for each SDK call, especially when pushing data

With the above functionalities, your script can seamlessly integrate with the mid-platform system, enabling flexible parameter configuration, transparent execution monitoring, and standardized return of scraped data.

---

# ⭐ Script Entry File (main.py)

### 💡 Code Example

```python
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
```

# Automated Data Scraping Script: Operation & Principle Guide

### 1. Script Overview

This is a template for an automation tool that acts like a "digital employee". It automatically opens specified web pages (e.g., social media pages), extracts the information you need, and organizes it into structured tables.

### 2.  How It Works (4 Core Stages)

### Stage 1: Receive Instructions (Retrieve Input Parameters)

Before starting the script, you provide instructions (e.g., which webpage URL to scrape, how many data entries to collect).

### Stage 2: Anonymity Setup (Proxy Network Configuration)

To access overseas or restricted websites smoothly, the script automatically configures an "encrypted tunnel" (proxy server).

### Stage 3: Automated Work (Business Logic Processing)

This is the core part of the script. Based on the provided URL, it automatically navigates to the target page and extracts information such as titles, content, and image URLs.

### Stage 4: Report Results (Data Push & Table Generation)

After scraping, the script converts unstructured information into a standard format and saves it to the system. It also automatically designs table headers (e.g., Column 1: "URL", Column 2: "Content").

---

# ⭐ Script Input Configuration (input_schema.json) 

The input_schema.json file serves as the "face" of your script. By modifying this file, you control which parameters users need to fill in before starting the script (e.g., URL, keywords, dates) and how these input fields are displayed (dropdowns, checkboxes, text boxes, etc.).

### 1. Overall Structure Analysis

A standard configuration file consists of the following three parts:：

1. **description**：Introduce the script's functionality and usage to users.
2. **b (Concurrency Key Field)**：Determines how the script splits tasks.
3. **properties (Parameter List)**：Specific functional settings.
### 💡  Code Example

```json
{
  "description": "With our Instagram Reel information scraper tool, after a successful scrape, you can extract the Reel author's username, Reel caption, hashtags used in the post, number of comments on the Reel, Reel publish date, likes count, views count, play count, popular comments, unique post identifier, URL of the Reel's display image or video thumbnail, product type, Reel duration, video URL, post audio link, number of posts on the profile, number of followers on the profile, profile URL, whether the account is a paid partner, and other relevant information. Currently, the tool can scrape via Instagram username, URL, and other methods, and the scrape results can be downloaded in various structured formats.",
  "b": "startUrl",
  "properties": [
    {
      "title": "URL",
      "name": "startUrl",
      "type": "array",
      "editor": "requestList",
      "description": "This parameter is used to specify the Instagram access URL to be fetched.",
      "default": [
        {
          "url": "<https://www.instagram.com/reel/C5Rdyj_q7YN/>"
        },
        {
          "url": "<https://www.instagram.com/reel/C85BZjeSHuO>"
        }
      ],
      "required": true
    }
  ]
}

```

### Output Example: Input

![Description](https://oss.cafehook.com/cafehook/20251226/31517262663254017.png)

### 2. Key Root Field Explanation

| Field Name | Required | Description |
| --- | --- | --- |
| **description** | No | **Scraper Overview**。Displayed at the top of the page, supports describing script functionality, notes, etc. |
| **b** | **Yes** | **Task Splitting Key**。 Must contain the `name` of an element in `properties` . The script splits tasks for concurrent processing based on this field (e.g., by number of URLs).
| **properties** | **Yes** | **Parameter Configuration Array**。Stores all input items, with each element representing an input box or selector on the page. |

---

### 3. Detailed Parameter Item Properties (Properties Inside)

Each specific input item can include the following configurations:

- **title**:Label displayed on the page (e.g., "Search Keywords").
- **name(Unique Identifier)**: Internal ID for the program, **must be unique**. Cannot contain Chinese characters.
- **type**:
    - string
    - integer
    - boolean
    - array
    - object
- **editor (Editor Type)**: Determines the form style of the input item on the webpage (see table below).
- **description**: Supplementary hint text below the input box, guiding the user on how to fill it out.
- **default**: Supplementary prompt text below the input box to guide users on filling.
- **required**: Set to true to prevent script startup if the field is empty.

---

### 4.  Editor Type Selection Guide

Optimize user experience by selecting different editors based on your needs:
#### 4.1. Basic Text & Numeric

| Type | Use Case |
| --- | --- |
| **input**  | Short text, keywords, or account name |
| **textarea** | Remarks or detailed text description |
| **number** | Limit the number of items to collect, page number, and wait time in seconds |

#### 4.2. Selectors

| Type | Example |
| --- | --- |
| **select** | Select gender, language, region. |
| **radio** | Single selection from 2-3 options (button layout). |
| **checkbox** | Select multiple tags of interest. |
| **switch** | Enable/disable options. |

#### 4.3. Time & Special Lists

| Type |  Use Case  |
| --- | --- |
| **datepicker** | Filter posts by specific publish date. |
| **requestList** |Batch input webpage links to scrape. |
| **requestListSource** |Customize additional parameters. |
| **stringList** | Batch input multiple keywords.|

---

### 5.  Common Component Code Examples

#### 5.1. Single-line Text Box (input)

```json
{
    "title": "📍 Location (use only one location per run)",
    "name": "location",
    "type": "string",
    "editor": "input",
    "default": "New York, USA"
}
```
![Description](https://oss.cafehook.com/cafehook/20251226/31517269654503424.png)


#### 5.2. Multi-line Text Box (textarea)

```json
{
    "title": "Filter reviews by keywords",
    "name": "keywords",
    "type": "string",
    "editor": "textarea"
}
```

![Description](https://oss.cafehook.com/cafehook/20251226/31517272128487424.png)

#### 5.3.  Numeric Adjustment Box (number)

```json
{
    "title": "Number of places to extract (per each search term or URL)",
    "name": "maxPlacesPerSearch",
    "type": "integer",
    "editor": "number",
    "default": 4
}
```
![Description](https://oss.cafehook.com/cafehook/20251226/31517292686082049.png)

#### 5.4. Dropdown Menu (select)

```json
{
    "title": "🌍 Language",
    "name": "language",
    "type": "string",
    "editor": "select",
    "options": [
        {
            "label": "English",
            "value": "en"
        },
        {
            "label": "Afrikaans",
            "value": "af"
        },
        {
            "label": "azərbaycan",
            "value": "az"
        }
    ],
    "default": "en"
}
```

![Description](https://oss.cafehook.com/cafehook/20251226/31517279399968769.png)

#### 5.5.  Radio Buttons (radio)

```json
{
    "title": "🏢 Category",
    "name": "radio",
    "type": "integer",
    "editor": "radioGroup",
    "options": [
        {
            "label": "hotel",
            "value": 1
        },
        {
            "label": "restaurant",
            "value": 2
        }
    ],
    "default": 1
}
```
![Description](https://oss.cafehook.com/cafehook/20251226/31517296009150465.png)

#### 5.6. Checkboxes (checkbox)

```json
{
    "title": "Data Sections to Scrape",
    "name": "data_sections",
    "type": "array",
    "editor": "checkboxGroup",
    "options": [
        {
            "label": "Reviews",
            "value": "reviews"
        },
        {
            "label": "Address",
            "value": "address"
        },
        {
            "label": "Phone Number",
            "value": "phone_number"
        }
    ],
    "default": ["reviews", "address"]
}
```
![Description](https://oss.cafehook.com/cafehook/20251226/31517297526177792.png)


#### 5.7. Date Picker (datepicker)

```json
{
    "title": "📅 Extract posts that are newer than",
    "name": "date",
    "type": "string",
    "editor": "datepicker",
    "format": "DD/MM/YYYY", 
    "valueFormat": "DD/MM/YYYY" 
}
```
![Description](https://oss.cafehook.com/cafehook/20251226/31517299223560193.png)

```json
// editor:"datepicker"
// dateType: 'absoluteOrRelative'
{
    "title": "📅 Extract posts that are newer than",
    "name": "date",
    "type": "string",
    "editor": "datepicker",
    "dateType": "absoluteOrRelative"
}
```

![Description](https://oss.cafehook.com/cafehook/20251226/31517300750417920.png)

![Description](https://oss.cafehook.com/cafehook/20251226/31517301740404737.png)

#### 5.8. Toggle Switch (switch)

```json
{
    "title": "⏩ Skip closed places",
    "name": "skipClosed",
    "type": "boolean",
    "editor": "checkbox"
}
```

![Description](https://oss.cafehook.com/cafehook/20251226/31517302786752512.png)

#### 5.9. URL List (requestList)

```json
{
    "name": "startURLs",
    "type": "array",
    "title": "Start URLs",
    "editor": "requestList",
    "default": [
        {
            "url": "https://www.google.com/search?sca_esv=593729410&q=Software+Engineer+jobs&uds=AMIYvT8-5jbJIP1-CbwNj1OVjAm_ezkS5e9c6xL1Cc4ifVo4bFIMuuQemtnb3giV7cKava9luZMDXVTS5p4powtoyb0ACtDGDu9unNkXZkFxC0i7ZSwrZd_aHgim6pFgOWgs0dte0pnb&sa=X&ictx=0&biw=1621&bih=648&dpr=2&ibp=htl;jobs&ved=2ahUKEwjt-4-Y6KyDAxUog4kEHSJ8DjQQudcGKAF6BAgRECo"
        },
        {
            "url": "https://www.google.com.hk/search?q=software+engineer+salary&newwindow=1&sca_esv=593729410&biw=1588&bih=1273&ei=vEtOadCxI-3AkPIP952z0Qc&oq=Software+Engineer&gs_lp=Egxnd3Mtd2l6LXNlcnAiEVNvZnR3YXJlIEVuZ2luZWVyKgIIAjIKEAAYgAQYQxiKBTIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABEj2yQFQ0TFYlbEBcAR4AZABBJgBkwOgAbUXqgEHMi0zLjQuMrgBA8gBAPgBAZgCBqACiAWoAgPCAgoQABiwAxjWBBhHwgIgEAAYgAQYtAIY1AMY5QIY5wYYtwMYigUY6gIYigPYAQGYAwTxBcFiu8bFvIEOiAYBkAYKugYECAEYB5IHCTQuMC4xLjAuMaAHvy6yBwcyLTEuMC4xuAf1BMIHAzItNsgHGIAIAA&sclient=gws-wiz-serp"
        }
    ],
    "required": true,
    "description": "The URLs of the website to scrape"
}
```
![Description](https://oss.cafehook.com/cafehook/20251226/31517304617041920.png)

#### 5.10. URL Request List Source (requestListSource)

```json
{
    "title": "startURLs",
    "name": "url",
    "type": "array",
    "editor": "requestListSource",
    "default": [
        {
            "url": "https://www.instagram.com/espn",
            "end_date": "",
            "start_date": "",
            "num_of_posts": "10",
            "posts_to_not_include": ""
        }
    ],
    "param_list": [
        {
            "param": "url",
            "title": "URL",
            "editor": "input",
            "type": "string",
            "required": true,
            "description": "This parameter is used to specify the Instagram access URL to be fetched."
        },
        {
            "param": "num_of_posts",
            "title": "Maximum Number of Reels",
            "type": "integer",
            "editor": "number",
            "description": "This parameter is used to specify the maximum number of Reels to fetch."
        },
        {
            "param": "start_date",
            "title": "Start Date",
            "type": "string",
            "editor": "datepicker",
            "format": "MM-DD-YYYY",
            "valueFormat": "MM-DD-YYYY",
            "description": "This parameter is used to specify the start time of the post, format: mm-dd-yyyy, and should be earlier than the \"end_date\"."
        },
        {
            "param": "end_date",
            "title": "End Date",
            "type": "string",
            "editor": "datepicker",
            "format": "MM-DD-YYYY",
            "valueFormat": "MM-DD-YYYY",
            "description": "This parameter is used to specify the end time of the post, format: mm-dd-yyyy, and should be later than the \"start_date\"."
        }
    ],
    "description": "The URLs of the website to scrape"
}
```
![Description](https://oss.cafehook.com/cafehook/20251226/31517306406043648.png)

#### 5.11. String List

```json
{
    "title": "🔍 Search term(s)",
    "name": "searchTerms",
    "type": "array",
    "editor": "stringList",
    "default": [
        {
            "string": "restaurant"
        },
        {
            "string": "school"
        }
    ]
}
```
![Description](https://oss.cafehook.com/cafehook/20251226/31517307891482624.png)

### 💡 Configuration Tips

1. **Clear Prompts:**：Ensure `description` is clear and accurate to help your script be discovered by more target users.
2. **Set Default Values**：Reasonable`default`values allow users to run the script with one click, significantly lowering the usage barrier.
3. **Mandatory Field Validation**：For parameters required for script execution (e.g., login cookies, main URL), always set `required`: true.

---

# ⭐Python Dependency Management File (requirements.txt)

This file lists all third-party Python packages and their version information required to run the script. The system will automatically read this file and install all specified dependencies to ensure the script runs correctly.

### Dependency List Explanation

Below are the Python packages and their corresponding versions required for this project:

Example：

```
attrs==25.4.0
beautifulsoup4==4.14.2
certifi==2025.10.5
cffi==2.0.0
charset-normalizer==3.4.4
click==8.3.0
colorama==0.4.6
cssselect==1.3.0
DataRecorder==3.6.2
DownloadKit==2.0.7
DrissionPage==4.1.1.2
et_xmlfile
filelock
```

### ❗Important Notes

### 1. Version Number Explanation

- **Packages with version numbers**（e.g. `beautifulsoup4==4.14.2`）：The system installs this exact version to ensure consistency with the development environment.
- **Packages without version numbers**（e.g. `et_xmlfile`）：The system automatically installs the latest available version of the package.

### 2. Installation Notes

- The system automatically handles installation of all dependencies – no manual operation required.
- Installation may take several minutes depending on network speed and package size.
- If installation fails, the system displays error messages – resolve issues as prompted.
### 3. Ensure Script Functionality

To ensure smooth execution of the Python script:

- List all used third-party packages in this file.
- Specify version numbers for critical core packages (e.g., package==version).
- Regularly update dependencies to get new features and security fixes.

## Frequently Asked Questions (FAQs)

**Q：Why specify version numbers?**

A：Specifying version numbers ensures the same package versions are used across different environments (development, testing, production), avoiding inconsistent program behavior or compatibility issues caused by version differences.

**Q：What happens if no version number is specified?**

A：Without a version number, the system installs the latest version of the package. This may cause incompatibility with the script, so it's recommended to fix versions for core dependencies.

**Q：How to add new dependencies?**

A：Simply add a new line in this file in the format "package==version" or "package", then re-upload the zip compressed file in the backend. The system will automatically install it on next run.

**Q：What to do if installation fails?**

A： Check network connectivity or try switching Python package mirrors. If issues persist, contact the system administrator.

---

*Last Updated: Ensure this dependency list is updated promptly after modifying script functionality to reflect all new package dependencies.*