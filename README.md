
<div align="center">
   <a href="https://github.com/zebbern/Zefoy-Automator-2025">
      <img src="https://www.edigitalagency.com.au/wp-content/uploads/TikTok-icon-glyph.png" alt="Logo" width="120" height="121">
   </a>

## Automate Zefoy Interactions With No Effort


---

| **Features**                      | **Description**                                                              |
|-----------------------------------|------------------------------------------------------------------------------|
| **Automated Views**               | Automate video views on TikTok seamlessly.                                   |
| **Likes Automation**              | Perform automated likes on specified videos or profiles.                     |
| **Comment Likes**                 | Boost engagement by automating comment likes.                                |
| **Dynamic Service Selection**     | Supports multiple services based on availability.                            |
| **Continuous Execution**          | Automatically loops tasks until stopped by the user.                         |
| **User-Friendly Console Interface**| Interactive CLI for straightforward control and input.                       |
| **Service Reliability**           | Handles errors like interruptions and connectivity issues gracefully.        |

---
</div>

## **Overview**

The **TikTok Automation Bot** leverages Python and Selenium WebDriver to automate TikTok interactions via [Zefoy](https://zefoy.com/). Its simple yet powerful interface makes it ideal for automating tasks like increasing views, likes, and comment interactions.

### **How It Works**

1. **Run the Script:** Execute `Run.py` to start the bot.  
2. **Solve the CAPTCHA:** Manually complete the CAPTCHA on Zefoy.  
3. **Ignore Pop-ups:** Skip consent pop-ups automatically.  
4. **Select an Option:** Choose a desired service in the console.  
5. **Enter Details:** Provide video URL or username if "comment likes" is chosen.  
6. **Relax:** The script runs continuously until manually stopped.  

---

## **Prerequisites**

Before you begin, ensure you have the following installed:

- Python 3.6 or newer
- pip (Python package installer)
- Google Chrome or Chromium browser
- ChromeDriver (compatible with your browser version)

---

## **Installation**

### 1. Clone the Repository

```bash
git clone https://github.com/zebbern/Zefoy-Automation.git
cd Zefoy-Automation
```

### 2. Set Up a Virtual Environment (Optional)

#### On Unix/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

---

## **Usage**

To run the bot, follow these steps:

```bash
python run.py
```

- Complete the CAPTCHA on [Zefoy](https://zefoy.com/).  
- Follow the console prompts to select services and provide necessary details.  
- Sit back and let the automation take over!

---

| **Input Information**             | **Description**                                                              |
|-----------------------------------|------------------------------------------------------------------------------|
| **Video URL/Usernames**           | Specify URLs or usernames for actions like views or comment likes.           |
| **Repeat Mode**                   | Tasks run in a continuous loop until stopped.                                |

---

## **Acknowledgments**

A special thanks to [Zefoy](https://zefoy.com/) for providing the platform for automation.  

---

## **Disclaimer**

> [!WARNING] 
This project is for **educational purposes only** and is not affiliated with TikTok or Zefoy. Users are responsible for ensuring compliance with TikTok's terms of service. Use responsibly and ethically.

---
