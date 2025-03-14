# 🧠 Brainery - Full Stack Learning Platform

Brainery is an **interactive web platform** designed for learners to **store, manage, and explore educational resources**. Built with **Flask, MongoDB, Bootstrap, and JavaScript**, Brainery allows users to **save study topics, access shared learning materials, and track their progress** in an intuitive interface.

---

## 📌 Table of Contents

1. **[Project Overview](#project-overview)**  
    - [Key Features](#key-features)  
    - [Why Choose Brainery?](#why-choose-brainery)  

2. **[Live Site](#live-site)**  

3. **[Repository](#repository)**  

4. **[User Experience (UX)](#user-experience-ux)**  
    - [Project Goals](#project-goals)  
    - [User Stories](#user-stories)  
    - [Design](#design)  
        - [Colour Scheme](#colour-scheme)  
        - [Typography](#typography)  
        - [Imagery & UI Elements](#imagery-ui-elements)  

5. **[Wireframes](#wireframes)**  
    - [Home Page Wireframe](#home-page-wireframe)  
    - [Login Page Wireframe](#login-page-wireframe)  
    - [Register Page Wireframe](#register-page-wireframe)  
    - [Dashboard Page Wireframe](#dashboard-page-wireframe)  

6. **[Features](#features)**  
    - [Existing Features](#existing-features)  
        - [Home Page](#home-page)  
        - [User Authentication](#user-authentication)  
        - [Study Topics Management](#study-topics-management)  
        - [Public Resource Sharing](#public-resource-sharing)  
        - [Search & Filter Functionality](#search-filter-functionality)  
        - [User Dashboard](#user-dashboard)  
        - [Security Features](#security-features)  
        - [Mobile Responsive UI](#mobile-responsive-ui)  
    - [Future Features](#future-features)  
        - [Note-Taking System](#note-taking-system)  
        - [Learning Progress Analytics](#learning-progress-analytics)  
        - [Community Forum](#community-forum)  
        - [Study Schedule Planner](#study-schedule-planner)  
        - [File Upload for Study Materials](#file-upload-for-study-materials)  
        - [Accessibility Enhancements](#accessibility-enhancements)  

7. **[Technologies Used](#technologies-used)**  
    - [Backend Technologies](#backend-technologies)  
    - [Frontend Technologies](#frontend-technologies)  
    - [Security and Authentication](#security-authentication)  
    - [Responsive Design](#responsive-design)  
    - [Version Control & Hosting](#version-control-hosting)  

8. **[Testing](#testing)**  
    - [Manual Testing](#manual-testing)  
        - [Link Navigation](#link-navigation)  
        - [Form Validation](#form-validation)  
        - [Responsiveness Testing](#responsiveness-testing)  
    - [Validation Testing](#validation-testing)  
        - [HTML Validation](#html-validation)  
        - [CSS Validation](#css-validation)  
    - [Google Lighthouse Testing](#google-lighthouse-testing)  
    - [User Testing](#user-testing)  
        - [User Feedback](#user-feedback)  
        - [Mobile Testing Results](#mobile-testing-results)  

9. **[Bugs and Fixes](#bugs-and-fixes)**  
    - [Common Bugs](#common-bugs)  
    - [Solutions Implemented](#solutions-implemented)  

10. **[Deployment](#deployment)**  
    - [Deployment to GitHub Pages](#deployment-to-github-pages)  
    - [Local Setup](#local-setup)  

11. **[Credits](#credits)**  
    - [Icons & Visual Assets](#icons-visual-assets)  
    - [Media & Video Sources](#media-video-sources)  
    - [Libraries & Frameworks](#libraries-frameworks)  
    - [APIs & Integrations](#apis-integrations)  
    - [Documentation References](#documentation-references)  

12. **[Acknowledgements](#acknowledgements)**  

---

## 🌐 Live Site
[**Brainery - Live Site**](#) *(To be updated upon deployment)*

---

## 📂 Repository
[**GitHub Repository**](https://github.com/your-username/MP3-Brainery.git)

---

## 🚀 Project Overview
Brainery is a **community-driven** web platform designed to help learners store, manage, and share educational resources efficiently. It provides an interactive and secure environment where students, educators, and professionals can collaborate and enhance their knowledge base.

### 🌟 Key Features:
- 📚 **User Authentication:** Secure **registration, login, and logout** functionality using Flask-Login.
- 📑 **Study Topic Management:** Users can **create, edit, delete, and organize** their study topics.
- 🌎 **Public Learning Resources:** Users can **browse and contribute to a shared knowledge base** to support collaborative learning.
- 🔍 **Search & Filter Options:** Quickly **locate study topics and resources** with an intuitive search function.
- 📊 **Dashboard & User Analytics:** Personalized **dashboard to track saved topics, learning progress, and activity history**.
- 🎨 **Responsive UI:** A **modern and intuitive design** using Bootstrap for a seamless experience across devices.
- 🔐 **Security Features:**
  - **CSRF Protection** via Flask-WTF to secure forms.
  - **Password Hashing** using bcrypt for **enhanced security**.
  - **Session Management** to **protect user data and prevent unauthorized access**.
- 🌍 **Multi-User Collaboration:** Enables **team-based learning and group study sessions** by allowing users to share topics.
- 📥 **File Upload Support:** Users can **upload PDFs, images, and notes** for reference.
- 📝 **Integrated Note-Taking System:** **Save personal notes** alongside study topics for effective learning.
- 📌 **Bookmarking System:** **Mark favorite resources** for quick access later.
- 📧 **Email Notifications:** Integration with **EmailJS** for sending account updates and notifications.
- 🗂 **Category-Based Organization:** Users can **categorize and tag topics** for a well-structured study plan.

Brainery is designed to **streamline knowledge sharing and academic collaboration**, helping students, researchers, and professionals **manage their learning materials more effectively**.

Brainery is designed to **streamline knowledge sharing and academic collaboration**, helping students and professionals **manage their learning materials** more efficiently.

---

### **📌 Pre-Project Planning**  

To kick off the Brainery project, I evaluated different **educational and knowledge-sharing platforms** to determine **which type of application would provide the most value** while showcasing my technical skills. I analyzed various platform ideas based on **four key criteria**:  

1. **Portfolio-Weight** – How well this project would represent my skills in **full-stack development**.  
2. **Complexity** – The difficulty of implementing **backend functionality, database design, and UI/UX**.  
3. **Time to Research** – The amount of time required to understand and **develop core features**.  
4. **Scalability & Market Demand** – The potential for **expansion and real-world adoption** by learners and educators.  

Based on these factors, I ranked different **web application ideas** to determine the best approach for my **full-stack milestone project**.  

| **Project Type** | **Portfolio-Weight** | **Complexity** | **Time to Research** | **Scalability & Market Demand** | **Total Score** |  
|-----------------|------------------|------------|------------------|-------------------|-------------|  
| **Online Study Hub (Brainery)** | **10** | **9** | **7** | **10** | **36** |  
| **E-Commerce Store** | 8 | 9 | 6 | 8 | 31 |  
| **Event Management System** | 7 | 7 | 5 | 7 | 26 |  
| **Personal Finance Tracker** | 8 | 8 | 7 | 6 | 29 |  

### **💡 Why Brainery?**  
After analyzing the above options, I chose **Brainery** because:  
✅ It **aligns with my skills** in **Flask, MongoDB, Bootstrap, and user authentication**.  
✅ It offers a **high-value, real-world application** that can be expanded over time.  
✅ It allows for **multiple user functionalities** including **CRUD operations, authentication, and search functionality**.  
✅ The concept of a **study hub and collaborative learning** is highly **relevant in today's digital education space**.  

---

### **🔎 Platform Feature Ranking**  
I also ranked specific **core features** of the project to prioritize development and ensure **maximum impact** on user experience.  

| **No.** | **Feature** | **Importance** |  
|-----|-----------------------|--------------|  
| 1️⃣ | **Secure User Authentication** | ⭐⭐⭐⭐⭐ |  
| 2️⃣ | **Save & Manage Study Topics** | ⭐⭐⭐⭐⭐ |  
| 3️⃣ | **Search & Filter Functionality** | ⭐⭐⭐⭐ |  
| 4️⃣ | **Public Resource Sharing** | ⭐⭐⭐⭐ |  
| 5️⃣ | **User Dashboard & Progress Tracking** | ⭐⭐⭐ |  
| 6️⃣ | **Collaborative Study Features** (Future) | ⭐⭐⭐ |  

This ranking helped me **prioritize feature development**, ensuring that **core functionalities** (like authentication and topic management) were **fully implemented before optional enhancements**.  

---

## 📜 User Experience (UX)

### 🎡 Project Goals
Brainery aims to create an interactive, accessible, and **user-friendly platform** that enhances the learning experience through technology. Below are the primary objectives that guide the design and functionality of the platform:

- **User-Centric Design:** Provide an **intuitive online knowledge hub** that is easy to navigate for learners of all skill levels.
- **Efficient Information Management:** Enable users to **store, retrieve, and organize** study topics efficiently.
- **Collaborative Learning:** Foster **community engagement** by allowing users to **share and explore** public learning resources.
- **Secure Environment:** Implement **robust authentication and security protocols** to protect user data and ensure privacy.
- **Seamless User Interaction:** Create an **engaging and responsive UI** that enhances the user experience across devices.

### 👤 User Stories
#### 👨‍💼 New Users
- I want to **create an account** to save my study topics.
- I want to **log in securely** to access my resources.
- I want to **search for learning materials** shared by the community.

#### 👥 Returning Users
- I want to **edit my saved topics** for better organization.
- I want to **delete outdated topics** to keep my list relevant.
- I want to **view my study progress** and track saved resources.

#### 🛠️ Site Admins
- I want to **monitor study topics** and remove inappropriate content.
- I want to **manage user permissions** and prevent unauthorized access.

### 🎨 Design
#### 🟢 Colour Scheme
- **Primary Color:** `#20c997` (Green) – Represents growth and learning.
- **Secondary Color:** `#f8f9fa` (Light Grey) – Clean, modern UI.
- **Accent Colors:** `#333` (Dark Text) and `#ffffff` (White Background).

#### 🎨 Typography
- **Roboto:** Used for general text.
- **Montserrat:** Used for headings.

#### 🖼 Imagery & UI Elements
- **Interactive Cards** for study topics.
- **Progress Tracking Bars** to visualize learning engagement.
- **Icons & Buttons** for **intuitive navigation**.

---

### **🎨 Wireframes**  

The wireframes provide a **visual structure** of Brainery’s **core pages**, ensuring a well-organized **user experience**. These were designed using **Balsamiq** and serve as the **foundation for UI development**.

📂 **Wireframe Directory:**  
```
brainery_data/static/wireframes
```

---

### **🏠 Home Page Wireframe**  
![Home Wireframe](brainery_data/static/wireframes/home.bmpr)

### **🔑 Login Page Wireframe**  
![Login Wireframe](brainery_data/static/wireframes/login.bmpr)

### **📝 Register Page Wireframe**  
![Register Wireframe](brainery_data/static/wireframes/register.bmpr)

### **📊 Dashboard Page Wireframe**  
![Dashboard Wireframe](brainery_data/static/wireframes/dashboard.bmpr)

---

### **💡 Features**  

Brainery is designed to provide a seamless **learning experience** through interactive **study topic management, public resource sharing, and user-friendly navigation**. Below are the **core features**, accompanied by visual representations.  

📂 **Image Directory:**  
```
brainery_data/static/images/
```
---

### **✅ Existing Features**  

---

#### **🏠 Home Page**
- **Engaging Hero Section**
  - Features an **immersive hero video background** sourced from [Tactus Marketing](https://tactusmarketing.com/wp-content/uploads/tactus-waves-hero.mp4).
  - Smooth **fade-in animations** on the title and tagline enhance interactivity.
  - Call-to-action **"Get Started" button** directs users to the registration page.
  - ![Hero Section](brainery_data/static/images/home-hero.png)

---

#### **🔑 User Authentication**
- **Secure Login & Registration**
  - Users can **register** using **email and a secure password**.
  - Flask-Login **manages session authentication**.
  - **CSRF protection** is implemented to prevent cross-site request forgery.
  - ![Login Page](brainery_data/static/images/login-form.png)
  - ![Register Page](brainery_data/static/images/register-form.png)

---

#### **📚 Study Topics Management**
- **CRUD (Create, Read, Update, Delete) Operations**
  - Users can **save, update, and delete study topics** in their personal dashboard.
  - Topics are stored in **MongoDB**, allowing persistent storage and retrieval.
  - **Real-time updates** ensure instant feedback on changes.
  - ![Dashboard - Study Topics](brainery_data/static/images/dashboard-topics.png)

---

#### **📂 Public Resource Sharing**
- **Explore & Save Shared Study Materials**
  - Users can browse **public learning resources** shared by the community.
  - Resources are categorized by **subject type, popularity, and user contributions**.
  - Users can **bookmark resources to their dashboard** for easy access.
  - ![Resource Page](brainery_data/static/images/resource-page.png)

---

#### **🔍 Search & Filter Functionality**
- **Smart Search Bar**
  - Users can **search for topics and resources** by title.
  - Implements **MongoDB text indexing** for **fast and relevant search results**.
  - **Category filters** allow users to narrow down results.
  - ![Search Feature](brainery_data/static/images/search-bar.png)

---

#### **📊 User Dashboard**
- **Personalized Dashboard**
  - Displays **saved study topics, tracked progress, and bookmarked resources**.
  - Features **quick actions** to edit or delete topics.
  - Tracks **study engagement** through **progress indicators**.
  - ![User Dashboard](brainery_data/static/images/user-dashboard.png)

---

#### **🔐 Security Features**
- **CSRF Protection & Secure Sessions**
  - **Flask-WTF prevents CSRF attacks** on all form submissions.
  - **Session cookies** are encrypted and set to expire for added security.
  - ![Security Settings](brainery_data/static/images/security-settings.png)

---

#### **📱 Mobile Responsive UI**
- **Optimized for all devices**
  - Uses **Bootstrap 5 Grid System** for seamless responsiveness.
  - UI elements **automatically adjust** based on screen size.
  - ![Mobile View](brainery_data/static/images/mobile-dashboard.png)

---

### **🚀 Future Features**  

#### **🖊️ Note-Taking System**  
- Allow users to **attach personal notes** to their study topics.  
- Notes will be **stored in MongoDB** and accessible via the dashboard.  
- Users can **edit, delete, and organize their notes** within topics.  

#### **📊 Learning Progress Analytics**  
- Users will be able to **track their study progress visually**.  
- Interactive **progress bars and charts** will display completed topics.  

#### **📢 Community Forum**  
- A **discussion board** where users can ask and answer questions.  
- Threads will be **categorized by subject area**.  

#### **📅 Study Schedule Planner**  
- Users can **set reminders and study schedules** for different topics.  
- **Google Calendar API** will be integrated for **syncing schedules**.  

#### **📎 File Upload for Study Materials**  
- Users will be able to **attach PDF, DOC, and PPT files** to their study topics.  
- Uploaded files will be **securely stored and downloadable**.  

### **🚀 Accessibility Enhancements**  

- **Voice Command Support** – Users will be able to **navigate the dashboard using voice commands**.  
- **High-Contrast Mode** – A toggle option for users with **visual impairments**.  
- **Keyboard Navigation Support** – All features will be accessible **without a mouse**.  

---

### **💪 Technologies Used**
- **Flask** – Lightweight **Python web framework** for backend development.
- **MongoDB** – **NoSQL database** to store user data, study topics, and public resources.
- **Flask-Login** – Ensures **secure authentication and session management**.
- **Flask-WTF** – Provides **CSRF protection and secure form handling**.
- **Bcrypt** – Used for **password hashing** to enhance security.
- **Bootstrap 5** – Delivers a **modern, responsive UI** with built-in CSS components.
- **JavaScript & jQuery** – Enhances **frontend interactivity and AJAX requests**.
- **GitHub** – Used for **version control, collaboration, and deployment**.
- **EmailJS** – Handles **email notifications** and **account recovery emails**.
- **FontAwesome** – Provides **icons for UI elements**.

---

## Testing

### Manual Testing
Brainery was manually tested across multiple browsers (Chrome, Firefox, Safari, and Edge) and on various devices (mobile, tablet, and desktop) to confirm the platform’s responsiveness, functionality, and overall user experience. Detailed results of the tests conducted are outlined below:

#### Testing Links, Forms, and Navigation

| Test                                            | Outcome |
|-------------------------------------------------|---------|
| All navigation bar links direct to their intended pages | Pass    |
| The "Get Started" button on the home page leads to the registration form | Pass    |
| The footer social media icons redirect to the correct social media platforms | Pass    |
| Registration and login forms submit successfully with valid input | Pass    |
| Users are prompted to correct invalid inputs (e.g., missing fields, incorrect email format) | Pass    |
| Users are prevented from submitting forms with empty required fields | Pass    |

#### Testing Responsiveness

| Test                                             | Outcome |
|--------------------------------------------------|---------|
| Layout displays correctly on large screens (desktops and larger tablets) | Pass    |
| Content remains readable and navigation stays functional on small screens (smartphones and small tablets) | Pass    |
| Interactive elements (buttons, dropdowns, and input fields) remain usable across screen sizes | Pass    |

---

### User Testing

**Testing Scenarios:**  
A group of 5 users was asked to complete various tasks without guidance to assess the intuitiveness and usability of the platform. These tasks and results are detailed below:

| Task                                                         | Success Rate |
|--------------------------------------------------------------|--------------|
| Register for an account, log in, and add a study topic       | 100%         |
| Update a saved topic’s details                               | 100%         |
| Navigate to the Explore page and bookmark a public resource  | 100%         |
| Logout and log back in to verify bookmarked items            | 100%         |
| Submit the contact form to reach the support team            | 100%         |

**Responsive Testing Feedback:**  
The same group of users also tested Brainery on mobile and tablet devices, providing insights into layout and navigation.

| Test                                  | Feedback |  
|---------------------------------------|----------|  
| Navigation and forms on mobile        | No issues, clear layout |  
| Topic editing interface on tablet     | No issues, easy to use |  
| Explore resource cards on small screens | No overlap, smooth scrolling |  

---

### Lighthouse Testing

Brainery’s core pages were analyzed using Google Lighthouse to measure performance, accessibility, best practices, and SEO. Below are the scores and corresponding links to the full Lighthouse reports:

| Page                     | Performance | Accessibility | Best Practices | SEO  |  
|--------------------------|-------------|----------------|----------------|------|  
| Home                    | 95          | 100            | 100            | 98   |  
| Dashboard               | 90          | 98             | 100            | 95   |  
| Registration/Sign-In    | 92          | 100            | 100            | 99   |  
| Explore Resources       | 89          | 95             | 100            | 93   |  

**Lighthouse Reports:**  
- [Home Page Report](assets/lighthouse/home.pdf)  
- [Dashboard Report](assets/lighthouse/dashboard.pdf)  
- [Registration/Sign-In Report](assets/lighthouse/auth.pdf)  
- [Explore Resources Report](assets/lighthouse/explore.pdf)

---

### Validation Testing

All critical pages and associated stylesheets were validated using W3C tools to ensure compliance with modern web standards:

- **HTML Validation:**  
  - [Home Page Validation](assets/validation/home-validation.pdf)  
  - [Dashboard Validation](assets/validation/dashboard-validation.pdf)  
  - [Registration/Sign-In Validation](assets/validation/auth-validation.pdf)  
  - [Explore Page Validation](assets/validation/explore-validation.pdf)

- **CSS Validation:**  
  - [Stylesheet Validation](assets/validation/styles-validation.pdf)

---

### **🛠️ Bugs and Fixes**  

| **Bug** | **Issue** | **Fix** |  
|------|-------|-----|  
| **Login Fails** | Incorrect form validation caused login attempts to fail even with correct credentials. | Fixed by adding `email_validator` and ensuring proper email formatting. |  
| **Topic Not Saving** | MongoDB schema issue where ObjectId conversion was incorrect, preventing topic creation. | Fixed by updating `ObjectId` handling to ensure correct data format. |  
| **Styling Issues on Mobile** | UI elements were misaligned on smaller screens, making navigation difficult. | Fixed with Bootstrap media queries to enhance responsiveness. |  
| **Session Not Persisting** | Users were logged out unexpectedly due to incorrect session handling. | Fixed by ensuring session tokens were stored correctly with `SESSION_PERMANENT=False`. |  
| **CSRF Token Missing** | Forms failed to submit due to missing CSRF protection. | Fixed by adding `csrf_token` in all form submissions and implementing Flask-WTF validation. |  
| **Database Connection Timeout** | MongoDB queries took too long or failed intermittently. | Fixed by optimizing queries and ensuring proper database indexing. |  
| **Duplicate Study Topics** | Users could accidentally save duplicate topics without warnings. | Fixed by adding a **duplicate-check system** before saving a new topic. |  
| **Password Reset Not Working** | Users couldn't reset their passwords due to an incorrect email validation flow. | Fixed by ensuring email validation works and sending password reset links correctly via `EmailJS`. |  
| **Bookmarking System Bug** | Bookmarked topics were not displayed correctly after refresh. | Fixed by updating the **database query to fetch saved bookmarks properly**. |  
| **Flash Messages Not Displaying** | Success/error messages didn't appear after user actions. | Fixed by ensuring `flask.flash()` messages were properly included in the HTML templates. |  
| **Search Not Working Properly** | Search results were not filtering topics correctly. | Fixed by refining **search query logic** in MongoDB for better accuracy. |  
| **Dark Mode Not Saving** | Users' dark mode preferences reset after logout. | Fixed by storing dark mode settings in **localStorage** for persistence. |  
| **Broken Logout Button** | Clicking "Logout" didn't always end the session. | Fixed by ensuring `logout_user()` properly clears session cookies. |  
| **404 Errors on Deployment** | Static files like CSS and JS failed to load after deployment. | Fixed by adjusting GitHub Pages **file paths and CORS settings**. |  
| **Wiki API Not Fetching Data** | Study topics that relied on Wikipedia data were not displaying correctly. | Fixed by refining API calls and implementing **error handling for missing topics**. |  
| **Footer Overlapping Content** | The footer covered some content on smaller screens. | Fixed by adding `padding-bottom` to ensure proper spacing. |  
| **Broken Registration Form Validation** | Some required fields were not being validated correctly. | Fixed by ensuring Flask-WTF correctly processes all form fields. |  
| **User Dashboard Slow Load Times** | The dashboard took a long time to fetch study topics. | Fixed by implementing **pagination and lazy loading** for improved performance. |  
| **Session Not Expiring Properly** | Users remained logged in even after logging out in another tab. | Fixed by enforcing `SESSION_COOKIE_SECURE` and `SESSION_COOKIE_HTTPONLY`. |  
| **Rate Limiting Not Implemented** | No restriction on login attempts, allowing brute-force attacks. | Fixed by integrating `Flask-Limiter` to restrict failed login attempts. |  
| **Search Bar Not Displaying Correctly** | The search bar was hidden under some UI elements on mobile. | Fixed by adjusting **CSS positioning** to ensure proper visibility. |  
| **Hero Video Not Autoplaying on iOS** | The background video on the home page did not autoplay in Safari. | Fixed by adding `playsinline` and `muted` attributes to the video tag. |  
| **User Passwords Stored in Plaintext** | Security vulnerability where passwords were not hashed. | Fixed by implementing `bcrypt` for password hashing. |  
| **Study Topics Editable by Other Users** | Users could edit study topics created by others. | Fixed by restricting edit permissions to **only the topic owner**. |  
| **Broken Social Media Links** | Footer links to social media pages were incorrect. | Fixed by updating the `href` attributes with valid URLs. |  
| **Wiki Fetching API Crashing on Invalid Topics** | If a topic was not found on Wikipedia, the app crashed. | Fixed by implementing **fallback messages for missing topics**. |  
| **Static Assets Not Loading on Mobile** | Some CSS and JS files failed to load on certain mobile devices. | Fixed by adjusting static file paths and clearing cache. |  
| **Form Submission Without Input Allowed** | Some fields allowed form submission without input. | Fixed by enforcing required fields and adding JavaScript validation. |  
| **Account Deletion Not Removing All Data** | Deleting an account did not remove saved study topics. | Fixed by adding a **cascade delete function** to remove all user-related data. |  
| **Pagination Not Working for Large Resource List** | Users could not navigate through long lists of public resources. | Fixed by implementing **server-side pagination** for efficient data retrieval. |  
| **Login Button Click Delay** | Clicking "Login" had a noticeable delay before response. | Fixed by optimizing event listeners and reducing unnecessary database queries. |  
| **Forgot Password Emails Not Sending** | Users were not receiving password reset emails. | Fixed by verifying EmailJS API credentials and enabling SMTP debugging. |  
| **Mobile Menu Not Collapsing After Click** | The mobile navbar stayed open after selecting an option. | Fixed by adding an event listener to close the menu after selection. |  
| **User Dashboard Graphs Not Rendering** | Progress tracking graphs were not loading on some browsers. | Fixed by updating the JavaScript chart library to a newer version. |  
| **Bookmarking Resources Resulted in Duplicates** | Clicking "Save" on a resource sometimes saved it multiple times. | Fixed by adding a **duplicate-check system before insertion**. |  
| **Incorrect Timestamp on Study Topics** | Topics were showing incorrect creation dates. | Fixed by ensuring UTC timestamps were used consistently across the database. |  
| **Hover Effects on Buttons Not Consistent** | Some buttons did not show hover animations in Firefox. | Fixed by standardizing CSS transition properties. |  
| **Contact Form Not Sending Messages** | The contact form failed to send messages to the admin. | Fixed by properly setting up EmailJS integration. |  
| **Study Topics Not Deleting Properly** | Deleting a topic sometimes failed without an error message. | Fixed by adding proper database commit handling. |  
| **Wiki Data Caching Issues** | Wikipedia data was fetched on every request, slowing down performance. | Fixed by **caching API responses** for improved speed. |  
| **Site Favicon Not Displaying** | The favicon was missing in some browsers. | Fixed by ensuring the correct favicon path in `base.html`. |  
| **Study Progress Stats Not Updating** | The user’s learning progress stats did not update in real-time. | Fixed by ensuring AJAX calls update the stats after changes. |  
| **File Upload Security Vulnerability** | Users could upload malicious files. | Fixed by restricting file types and scanning for viruses. |  
| **User Dashboard Not Showing Newly Saved Topics** | Topics did not appear immediately after saving. | Fixed by adding a **real-time update function** using JavaScript. |  
| **UI Inconsistencies in Dark Mode** | Some elements did not adjust to dark mode properly. | Fixed by ensuring dark mode styles applied to all components. |  
| **Database Backup Issues** | Regular backups were failing due to a script error. | Fixed by ensuring proper cron job execution for database backups. |  
| **Wiki Data Fetch Delay** | Wikipedia content took too long to load. | Fixed by implementing async fetching and caching. |  

---

### **🚀 Deployment**

This project was deployed using **GitHub Pages**, which provides a **free and reliable hosting platform** for static websites directly from a GitHub repository. Below are the **detailed steps** followed to **deploy Brainery** and make it accessible online.

---

### **Steps for Deployment on GitHub Pages**

#### **1️⃣ Clone the Repository**
To begin, I **cloned the project repository** to my local machine:
```bash
git clone https://github.com/your-username/MP3-Brainery.git
```

#### **2️⃣ Navigate to the Project Directory**
After cloning, I moved into the project folder:
```bash
cd MP3-Brainery
```

#### **3️⃣ Make Necessary Changes**
- I made required updates to the project files using **VS Code**.
- Any changes to **HTML, CSS, JavaScript, or Flask backend** were tested thoroughly before committing.

#### **4️⃣ Commit and Push Changes to GitHub**
Once the changes were verified, I staged and committed them:
```bash
git add .
git commit -m "Updated project for deployment"
git push origin main
```

#### **5️⃣ Deploy to GitHub Pages**
I followed these steps to enable **GitHub Pages**:
1. Navigated to **GitHub Repository** → **Settings**.
2. Scrolled down to the **Pages** section in the sidebar.
3. Under **Branch**, selected `main` as the source.
4. Clicked **Save** to initiate deployment.

#### **6️⃣ Wait for Deployment**
- GitHub Pages automatically **processed the deployment**.
- Within a few minutes, the site was **live and accessible**.

#### **7️⃣ Access the Deployed Site**
Once deployment was complete, the site was available at:
```
https://your-username.github.io/MP3-Brainery/
```

---

### **Running the Project Locally**
To run the project **locally** for development and testing, follow these steps:

#### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/MP3-Brainery.git
```

#### **2️⃣ Navigate to the Project Directory**
```bash
cd MP3-Brainery
```

#### **3️⃣ Set Up a Virtual Environment**
It is recommended to create a virtual environment to install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
```

#### **4️⃣ Install Project Dependencies**
```bash
pip install -r requirements.txt
```

#### **5️⃣ Run the Flask Application**
```bash
python3 app.py
```

#### **6️⃣ Open the Project in Your Browser**
- Once the server is running, open **http://127.0.0.1:5000** in a web browser.

---

### **Benefits of Using GitHub Pages**
#### ✅ **Free Hosting**
- **GitHub Pages provides free hosting** for static sites, making it an ideal choice for personal projects and portfolios.

#### ✅ **Easy Deployment**
- Simply **pushing changes to the `main` branch** automatically **redeploys the site** without manual intervention.

#### ✅ **Reliable Performance**
- GitHub Pages runs on a **stable, globally distributed infrastructure**, ensuring fast and reliable site loading times.

#### ✅ **Version Control Integration**
- **All changes are tracked** using Git, allowing **seamless collaboration, rollbacks, and history tracking**.

#### ✅ **Custom Domain Support**
- Since I'm using **GitHub's paid version**, I can **assign a custom domain** for a **professional brand identity**.

### **✅ Enhanced GitHub Features**  
- This project is hosted on **GitHub’s paid plan**, which provides:  
  - **Increased resource limits** for repositories.  
  - **Better performance and reliability** for managing multiple large projects.  
  - **Advanced security features** for private repositories.  

---

### **🌟 Credits**  

Brainery was built using a combination of **open-source technologies, libraries, and external assets**. Below are the tools, resources, and references used in the development of this project.  

---

### **📌 Icons & Visual Assets**  
- **FontAwesome** – Provided **icons** for UI elements like buttons, navigation, and alerts.  
- **Unsplash** – Used for **high-quality images** where applicable.  

---

### **📌 Media & Video Sources**  
- **Hero Section Video** – The homepage **hero background video** was sourced from:  
  - **Tactus Marketing** – [tactusmarketing.com](https://tactusmarketing.com/wp-content/uploads/tactus-waves-hero.mp4)  
  - Used to create an **immersive visual experience** for users.  

---

### **📌 Libraries & Frameworks**  
- **Flask** – Python-based **web framework** for backend development.  
- **MongoDB** – NoSQL **database solution** for storing user data and study topics.  
- **Bootstrap 5** – **Responsive UI framework** for styling and layout.  
- **Flask-Login** – Managed **user authentication and session handling**.  
- **Flask-WTF** – Used for **form validation and CSRF protection**.  
- **Bcrypt** – Implemented **password hashing** for enhanced security.  
- **JavaScript & jQuery** – Powered **frontend interactivity and AJAX functionality**.  

---

### **📌 APIs & Integrations**  
- **EmailJS** – Integrated for **email notifications** (password resets, confirmations).  
- **Google Fonts** – Applied custom typography for a **modern, clean look**.
- **Wikipedia API / Live Wikipedia Fetch**  
  - Brainery retrieves **live study topics** and summaries from **Wikipedia**.  
  - Wikipedia content is dynamically **loaded and stored** for reference.  

---

### **📌 Deployment & Version Control**  
- **GitHub** – Hosted **repository, version control, and GitHub Pages deployment**.  
- **GitHub Actions** – Used for **CI/CD pipeline and automated testing**.  

---

### **📌 Documentation References**  
- **Flask Documentation** – Used for **backend development and routing logic**.  
- **MongoDB Docs** – Guided **database schema design and queries**.  
- **Bootstrap Docs** – Assisted in **responsive design and UI enhancements**.  

---

## 💙 Acknowledgements
Thanks to **Code Institute**, **Flask Documentation**, and the **open-source community** for guidance! 🚀

Special thanks to Miguel for their guidance throughout the project.
---

## ✨ Star This Project!
If you found Brainery helpful, **please give it a star** ⭐ on GitHub!

