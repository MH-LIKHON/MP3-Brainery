# MP3 - BRAINERY | LEARNING PLATFORM (BACKEND DEVELOPMENT MILESTONE PROJECT)

Brainery is an **interactive web platform** designed for learners to **store, manage, and explore educational resources**. Built with **Flask, MongoDB, Bootstrap, and JavaScript**, Brainery allows users to **save study topics, access shared learning materials, and track their progress** in an intuitive interface.

---

## **Table of Contents (TOC)**  

1. **[Project Overview](#project-overview)**  
   - [Key Features](#key-features)  
   - [Why Choose Brainery?](#why-brainery)  

2. **[Live Site](#live-site)**  

3. **[Repository](#repository)**  

4. **[User Experience (UX)](#user-experience-ux)**  
   - [Project Goals](#project-goals)  
   - [User Stories](#user-stories)  
   - [Design](#design)  
     - [Colour Scheme](#colour-scheme)  
     - [Typography](#typography)  
     - [Imagery & UI Elements](#imagery--ui-elements)  

5. **[Wireframes](#wireframes)**  

6. **[Features](#features)**  
   - [Existing Features](#existing-features)  
     - [Home Page](#home-page)  
     - [User Authentication](#user-authentication)  
     - [User Registration](#user-registration)  
     - [Registration Email](#registration-email)  
     - [Study Topics Management](#study-topics-management)  
     - [Public Resource Sharing](#public-resource-sharing)  
     - [User Dashboard](#user-dashboard)  
     - [Admin Dashboard](#admin-dashboard)
     - [Security Features](#security-features)  
     - [Mobile Responsive UI](#mobile-responsive-ui)  
   - [Future Features](#future-features)  
     - [Note-Taking System](#note-taking-system)  
     - [Learning Progress Analytics](#learning-progress-analytics)  
     - [Community Forum](#community-forum)  
     - [Study Schedule Planner](#study-schedule-planner)  
     - [File Upload for Study Materials](#file-upload-for-study-materials)  
     - [Accessibility Enhancements](#accessibility-enhancements)  

7. **[Security & Payment Disclaimer](#security--payment-disclaimer)**

8. **[Technologies Used](#technologies-used)**  

9. **[Database Schema for Brainery Learning Platform](#database-schema-for-brainery-learning-platform)**  
   - [Users Collection](#users-collection-users)  
   - [Subjects Collection](#subjects-collection-subjects)  
   - [Topics Collection](#topics-collection-topics)  
   - [Schema Relationships](#schema-relationships)  
   - [MongoDB Schema Diagram](#mongodb-schema-diagram)  
   - [How to Query Data](#how-to-query-data)   

10. **[Testing](#testing)**  
   - [Manual Testing](#manual-testing)  
     - [Testing Links, Forms, and Navigation](#testing-links-forms-and-navigation)  
     - [Testing Responsiveness](#testing-responsiveness)  
   - [User Testing](#user-testing)  
     - [Promocode for Testing](#promocode-for-testing)  
   - [Functional Testing (Live Site)](#functional-testing-live-site)  
   - [Security Testing](#security-testing)  
   - [Lighthouse Testing](#lighthouse-testing)  
   - [Validation Testing](#validation-testing)  

11. **[Bugs & Fixes](#bugs--fixes)**  

12. **[Deployment](#deployment)**  
    - [Deployment to Heroku](#steps-for-deployment-on-heroku)  
    - [Accessing Live Application](#accessing-the-live-application)  
    - [Local Setup](#running-the-project-locally)  

13. **[Credits](#credits)**  
    - [Icons & Visual Assets](#icons--visual-assets)  
    - [Media & Video Sources](#media--video-sources)  
    - [Libraries & Frameworks](#libraries--frameworks)  
    - [APIs & Integrations](#apis--integrations)  
    - [Documentation References](#documentation-references)  

14. **[Acknowledgements](#acknowledgements)**  

---

## Live Site
[**Brainery - Live Site**](https://mp3-brainery-7e2da4fb6ce9.herokuapp.com/)

---

## Repository
[**GitHub Repository**](https://github.com/MH-LIKHON/MP3-Brainery.git)

---

## Project Overview
Brainery is a **community-driven** web platform designed to help learners store, manage, and share educational resources efficiently. It provides an interactive and secure environment where students, educators, and professionals can collaborate and enhance their knowledge base.

In addition, Brainery features an **Admin Dashboard**, where **administrators can manage users, oversee study topics, and moderate shared content** to maintain a safe and productive learning space.

### Key Features:
- **User Authentication:** Secure **registration, login, and logout** functionality using Flask-Login.
- **Study Topic Management:** Users can **create, edit, delete, and organize** their study topics.
- **Public Learning Resources:** Users can **browse and contribute to a shared knowledge base** to support collaborative learning.
- **Admin Dashboard:** Admins can **view all users, promote them to admin, and delete accounts when necessary**.
- **User Role Management:** Admins can **assign admin privileges** to regular users.
- **Search & Filter Options:** Quickly **locate study topics and resources** with an intuitive search function.
- **Dashboard & User Analytics:** Personalized **dashboard to track saved topics, learning progress, and activity history**.
- **Responsive UI:** A **modern and intuitive design** using Bootstrap for a seamless experience across devices.
- **Security Features:**
  - **CSRF Protection** via Flask-WTF to secure forms.
  - **Password Hashing** using bcrypt for **enhanced security**.
  - **Session Management** to **protect user data and prevent unauthorized access**.
- **Multi-User Collaboration:** Enables **team-based learning and group study sessions** by allowing users to share topics.
- **File Upload Support:** Users can **upload PDFs, images, and notes** for reference.
- **Integrated Note-Taking System:** **Save personal notes** alongside study topics for effective learning.
- **Bookmarking System:** **Mark favorite resources** for quick access later.
- **Email Notifications:** Integration with **EmailJS** for sending account updates and notifications.
- **Category-Based Organization:** Users can **categorize and tag topics** for a well-structured study plan.

Brainery provides a structured way for students and professionals to organize and access their study materials efficiently.

---

### **Pre-Project Planning**  

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

### **Why Brainery?**  
After analyzing the above options, I chose **Brainery** because:  
✅ It **aligns with my skills** in **Flask, MongoDB, Bootstrap, and user authentication**.  
✅ It offers a **high-value, real-world application** that can be expanded over time.  
✅ It allows for **multiple user functionalities** including **CRUD operations, authentication, and search functionality**.  
✅ The concept of a **study hub and collaborative learning** is highly **relevant in today's digital education space**.  

---

### **Platform Feature Ranking**  
I also ranked specific **core features** of the project to prioritize development and ensure **maximum impact** on user experience.  

| **No.** | **Feature** | **Importance** |  
|-----|-----------------------|--------------|  
| 1️⃣ | **Secure User Authentication** | ⭐⭐⭐⭐⭐ |  
| 2️⃣ | **Save & Manage Study Topics** | ⭐⭐⭐⭐⭐ |  
| 3️⃣ | **Search & Filter Functionality** | ⭐⭐⭐⭐ |  
| 4️⃣ | **Public Resource Sharing** | ⭐⭐⭐⭐ |  
| 5️⃣ | **User Dashboard & Progress Tracking** | ⭐⭐⭐ |  
| 6️⃣ | **Admin Page & User Management** | ⭐⭐⭐⭐ |  
| 7️⃣ | **Collaborative Study Features** (Future) | ⭐⭐⭐ |  

Feature ranking guided development, ensuring authentication and topic management were completed before optional enhancements.

---

## User Experience (UX)

### Project Goals
Brainery aims to create an interactive, accessible, and **user-friendly platform** that enhances the learning experience through technology. Below are the primary objectives that guide the design and functionality of the platform:

- **User-Centric Design:** Provide an **intuitive online knowledge hub** that is easy to navigate for learners of all skill levels.
- **Efficient Information Management:** Enable users to **store, retrieve, and organize** study topics efficiently.
- **Collaborative Learning:** Foster **community engagement** by allowing users to **share and explore** public learning resources.
- **Secure Environment:** Implement **robust authentication and security protocols** to protect user data and ensure privacy.
- **Seamless User Interaction:** Create an **engaging and responsive UI** that enhances the user experience across devices.

### User Stories
#### New Users
- I want to **create an account** to save my study topics.
- I want to **log in securely** to access my resources.
- I want to **search for learning materials** shared by the community.

#### Returning Users
- I want to **edit my saved topics** for better organization.
- I want to **delete outdated topics** to keep my list relevant.
- I want to **view my study progress** and track saved resources.

#### Site Admins
- I want to **view all registered users** in an organized dashboard.
- I want to **promote regular users to admin** when necessary.
- I want to **delete user accounts** in case of inactivity or violation of guidelines.
- I want to **restrict unauthorized access to admin-only pages**.

### Design
#### Colour Scheme
- **Primary Color:** `#20c997` (Green) – Represents growth and learning.
- **Secondary Color:** `#f8f9fa` (Light Grey) – Clean, modern UI.
- **Accent Colors:** `#333` (Dark Text) and `#ffffff` (White Background).

#### Typography
- **Roboto:** Used for general text.
- **Montserrat:** Used for headings.

#### Imagery & UI Elements
- **Interactive Cards** for study topics.
- **Progress Tracking Bars** to visualize learning engagement.
- **Icons & Buttons** for **intuitive navigation**.

---

### **Wireframes**  

The wireframes provide a **visual structure** of Brainery’s **core pages**, ensuring a well-organized **user experience**. These were designed using **Balsamiq** and serve as the **foundation for UI development**.

**Wireframe Directory:**  
```
brainery_data/static/pdfs/
```
---

  - ![All Pages Wireframe](brainery_data/static/pdfs/brainery_allpages_desktop_tablet_mobile.pdf)

---

### **Features**  

Brainery is designed to provide a seamless **learning experience** through interactive **study topic management, public resource sharing, and user-friendly navigation**. Below are the **core features**, accompanied by visual representations.  

**Image Directory:**  
```
brainery_data/static/images/
```
---

### **Existing Features**  

---

#### **Home Page**
- **Engaging Hero Section**
  - Features an **immersive hero video background** sourced from [Tactus Marketing](https://tactusmarketing.com/wp-content/uploads/tactus-waves-hero.mp4).
  - Smooth **fade-in animations** on the title and tagline enhance interactivity.
  - Call-to-action **"Get Started" button** directs users to the registration page.
  - Social icons have hover effect and linked to their pages.
  - Nav menu and logo have animation effect.
  - Features section with multiple cards and popup messages.
  - ![Home Page](brainery_data/static/images/home.png)

    - ![Hero Section](brainery_data/static/images/homehero.png)

    - ![Features Section](brainery_data/static/images/homefeature.png)

    - ![Features PopUp](brainery_data/static/images/homepopup.png)

    - ![Logo](brainery_data/static/images/hoverlogo.png)

    - ![Icons](brainery_data/static/images/hovericon.png)

---

#### **User Authentication**
- **Secure Login**
  - Users can **login** using **email and a secure password**.
  - Users can **reset password** using **email address, if registered**.
  - Flask-Login **manages session authentication**.
  - **CSRF protection** is implemented to prevent cross-site request forgery.
  - ![Login Page](brainery_data/static/images/login.png)

    - ![Empty Field Message](brainery_data/static/images/loginmessage1.png)

    - ![Proceed Message](brainery_data/static/images/loginmessage3.png)

    - ![Invalid Password or Email Message](brainery_data/static/images/loginmessage2.png)

    - ![Password Reset](brainery_data/static/images/passwordreset.png)

  ---

#### **User Registration**
- **Secure Registration**
  - Users can **register** using:
    - **Personal Information** (name, email, phone, address, etc.).
    - **A dummy payment form** *(no real transactions, UI demonstration only)*.
    - **A promo code option** to bypass the payment step.

  #### **Payment Page Details**
  - **Does NOT process real payments** and **does NOT store card details**.
  - **For UI demonstration only** – users can enter any random numbers in the payment fields.
  - If the **promo code `CI25MP3`** is applied, the **card input fields are disabled**.
  - **Do NOT enter real card details** as no transactions occur.

  #### **Clarity on MongoDB Storage**
  - The database **only stores personal user data and authentication credentials**.
  - **Card details are NOT stored** in the database at any point.
  - User passwords are securely **hashed using bcrypt** before storage.

  #### **Additional Features**
  - If the email is already registered, a **notification will be displayed**.
  - After successful registration, a **confirmation message is shown**, and an email is sent.
  - **CSRF protection** is implemented to **prevent cross-site request forgery**.

  - ![Register Page](brainery_data/static/images/register1.png)

    - ![Registered Email Message](brainery_data/static/images/emailregistered.png)

  - ![Register Page](brainery_data/static/images/register2.png)

  - ![Register Page](brainery_data/static/images/register3.png)

  - ![Register Page](brainery_data/static/images/register4.png)

   - ![Register Page](brainery_data/static/images/successfulmessage.png)

---

#### **Registration Email**
- **EmailJS**
  - Users will receive an email after completing their registration.
  - Email contains the necessary information regarding their registration.
  - ![Registration Eamil](brainery_data/static/images/email.png)

---

#### **Study Topics Management**
- **CRUD (Create, Read, Update, Delete) Operations**
  - Users can **save, update, and delete study topics** in their personal dashboard.
  - Topics are stored in **MongoDB**, allowing persistent storage and retrieval.
  - **Real-time updates** ensure instant feedback on changes.
  - ![Dashboard Page](brainery_data/static/images/dashboard2.png)

---

#### **Public Resource Sharing**
- **Explore & Save Shared Study Materials**
  - Users can browse **public learning resources** shared by the community through Wikipedia.
  - Resources are categorized by **subject type, popularity, and user contributions**.
  - Users can **bookmark resources to their dashboard** for easy access.
  - ![Dashboard Saved Topics](brainery_data/static/images/dashboard3.png)

---

#### **User Dashboard**
- **Personalized Dashboard**
  - Displays **saved study topics, edit and bookmarked resources**.
  - Features **quick actions** to edit or delete topics.
  - ![User Dashboard](brainery_data/static/images/dashboard1.png)

---

#### **Admin Dashboard**
The **Admin Dashboard** provides tools for managing users. Admins have **exclusive access** to user role management and content moderation tools.

### **Admin Features**
- **User Management**: View, promote, or delete users.
- **Promote Users to Admin**: Upgrade regular users to **admin**.
- **Delete Users**: Remove inactive or problematic accounts.
- **Role-Based Access**: Only admins can access **admin tools**.

### **How Admins Access the Dashboard**
1. **Log in** with an **admin account**.
2. You will be at the **Admin Dashboard**.
3. Use the available tools to **manage users**.

| Feature | Description |
|---------|------------|
| **View Users** | Admins can **see all registered users** and check their roles. |
| **Promote Users** | Admins can **upgrade regular users to admin status**. Once promoted, demotion is **not possible**. |
| **Delete Users** | Admins can **remove inactive or inappropriate users** permanently. |

### **Updated User Roles**
| Role | Permissions |
|------|------------|
| **User** | Can **create, edit, and delete their own topics**. |
| **Admin** | Can **view all users, promote users to admin, and delete accounts**. |

![Admin Dashboard](brainery_data/static/images/admin1.png)


![Admin Dashboard](brainery_data/static/images/admin2.png)


---

#### **Security Features**
- **CSRF Protection & Secure Sessions**
  - **Flask-WTF prevents CSRF attacks** on all form submissions.
  - **Session cookies** are encrypted and set to expire for added security.

---

#### **Mobile Responsive UI**
- **Optimized for all devices**
  - Uses **Bootstrap 5 Grid System** for seamless responsiveness.
  - UI elements **automatically adjust** based on screen size.
  - ![Mobile View](brainery_data/static/images/mobile1.png)

  - ![Mobile View](brainery_data/static/images/mobile2.png)

  - ![Mobile View](brainery_data/static/images/mobile3.png)

  - ![Mobile View](brainery_data/static/images/mobile4.png)

  - ![Mobile View](brainery_data/static/images/mobile5.png)

  - ![Mobile View](brainery_data/static/images/mobile6.png)

  - ![Mobile View](brainery_data/static/images/mobile7.png)

  - ![Mobile View](brainery_data/static/images/mobile8.png)

  - ![Mobile View](brainery_data/static/images/mobile9.png)

---

### **Future Features**  

#### **Note-Taking System**  
- **Attach personal notes** to study topics.  
- **Store notes in MongoDB** for easy retrieval.  
- **Edit, delete, and organize notes** in the user dashboard.  

#### **Learning Progress Analytics**  
- **Track study progress** visually.  
- **Display progress bars and charts** for completed topics.  

#### **Community Forum**  
- **Create discussion boards** where users can ask and answer questions.  
- **Categorized threads** based on subject areas.  

#### **Study Schedule Planner**  
- Users can **set reminders and study schedules** for different topics.  
- **Google Calendar API** will be integrated for **syncing schedules**.  

#### **File Upload for Study Materials**  
- Users will be able to **upload and attach** PDF, DOC, and PPT files to their study topics.
- Uploaded files will be **securely stored and downloadable**.  

### **Accessibility Enhancements**  

- **Voice Command Support** – Users will be able to **navigate the dashboard using voice commands**.  
- **High-Contrast Mode** – A toggle option for users with **visual impairments**.  
- **Keyboard Navigation Support** – All features will be accessible **without a mouse**.  

---

## Security & Payment Disclaimer
This project **does NOT process real payments** and **does NOT store any credit card information**.

### How Payments Work:
- The payment form is **for UI demonstration only**.
- No real transactions take place.
- No payment details are stored in the database.

⚠️ **Do NOT enter real card information.** This is a **dummy payment page** to simulate a checkout experience without real payment processing.

📌 **Use the promocode `CI25MP3`** during registration to activate test access.

---

### **Technologies Used**
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

## Database Schema for Brainery Learning Platform

### Users Collection (`users`)
Stores user account information, authentication details, and subscription data.

| Field Name      | Data Type  | Description |
|---------------|-----------|-------------|
| `_id`        | ObjectId  | Unique identifier for each user. |
| `username`   | String    | Full name of the user. |
| `email`      | String    | User's email address (unique). |
| `password`   | String    | Hashed password for authentication. |
| `phone`      | String    | User's phone number. |
| `address_line1` | String | First line of the user's address. |
| `address_line2` | String | Second line of the user's address (optional). |
| `city`       | String    | City of residence. |
| `country`    | String    | Country code (ISO format). |
| `postcode`   | String    | Postal/ZIP code. |
| `dob`        | Date      | Date of birth (YYYY-MM-DD). |
| `selected_plan` | String | User's subscription plan. |
| `created_at` | Timestamp | Date when the user registered. |

---

### Subjects Collection (`subjects`)
Defines the categories of learning available in the platform.

| Field Name   | Data Type  | Description |
|-------------|-----------|-------------|
| `_id`       | ObjectId  | Unique identifier for each subject. |
| `name`      | String    | Subject title (e.g., "Information Technology"). |
| `icon`      | String    | Emoji or icon representing the subject. |
| `created_at` | Timestamp | Date when the subject was added. |

---

### Topics Collection (`topics`)
Contains individual learning topics under a subject.

| Field Name   | Data Type  | Description |
|-------------|-----------|-------------|
| `_id`       | ObjectId  | Unique identifier for each topic. |
| `subject_id` | ObjectId  | Links the topic to a subject. |
| `title`     | String    | Title of the study topic. |
| `description` | String  | Brief summary of the topic. |
| `created_at` | Timestamp | Date when the topic was created. |

---

### **Schema Relationships**
1️⃣ **Each `topic` belongs to a `subject`** (linked by `subject_id`).  
2️⃣ **Users are independent and do not directly link to subjects/topics**.  
3️⃣ **MongoDB uses ObjectIds (`_id`) as primary keys for all collections**.

---

### **MongoDB Schema Diagram**
Here’s a **visual representation** of the database structure:

![MongoDB Schema](brainery_data/static/images/mongodb_schema_structured.png)

---

### **How to Query Data**
Here are some common MongoDB queries to interact with your database:

  #### **Find a user by email**
  ```python
  user = mongo.db.users.find_one({"email": "user@example.com"})
  ```

  #### **Get all topics under a specific subject**
  ```python
  topics = mongo.db.topics.find({"subject_id": ObjectId("subject_id_here")})
  ```

  #### **List all subjects**
  ```python
  subjects = mongo.db.subjects.find()
  ```

---

## Testing

### Manual Testing
Brainery was manually tested across multiple browsers (Chrome, Firefox, Safari, and Edge) and on various devices (mobile, tablet, and desktop) to confirm the platform’s responsiveness, functionality, and overall user experience. Detailed results of the tests conducted are outlined below:

---

#### Testing Links, Forms, and Navigation

| Test                                            | Outcome |
|-------------------------------------------------|---------|
| All navigation bar links direct to their intended pages | Pass    |
| The "Get Started" button on the home page leads to the registration form | Pass    |
| The footer social media icons redirect to the correct social media platforms | Pass    |
| Registration and login forms submit successfully with valid input | Pass    |
| Users are prompted to correct invalid inputs (e.g., missing fields, incorrect email format) | Pass    |
| Users are prevented from submitting forms with empty required fields | Pass    |

---

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

#### **Promocode for Testing**
📌 **Use the promocode `CI25MP3`** during registration to activate test access.

---

### **Functional Testing (Live Site)**
The following user features were tested manually on the deployed Heroku site:

| **Feature**            | **Expected Behavior**                  | **Test Result** |
|-----------------------|--------------------------------------|--------------|
| **User Registration** | New users can sign up and receive a verification email | ✅ Working |
| **User Login**        | Registered users can log in with valid credentials | ✅ Working |
| **User Logout**       | Logged-in users can successfully log out | ✅ Working |
| **Create Record**     | Users can add new records to the database | ✅ Working |
| **Edit Record**       | Users can update existing records | ✅ Working |
| **Delete Record**     | Users can delete records from the database | ✅ Working |
| **Database Connection** | Data is properly stored in MongoDB | ✅ Working |
| **Email Functionality** | Verification emails are sent and received | ✅ Working |

📌 **All tests were performed manually by interacting with the live version of the site. The application successfully handled user authentication, CRUD operations, and data storage.**

---

**Responsive Testing Feedback:**  
The same group of users also tested Brainery on mobile and tablet devices, providing insights into layout and navigation.

| Test                                  | Feedback |  
|---------------------------------------|----------|  
| Navigation and forms on mobile        | No issues, clear layout |  
| Topic editing interface on tablet     | No issues, easy to use |  
| Explore resource cards on small screens | No overlap, smooth scrolling |  

---

### Security Testing
- The project was scanned using Bandit for security vulnerabilities.
- No critical security issues were found in the project's source code.
- Some warnings originated from third-party dependencies but do not affect the project's functionality.

---

### Lighthouse Testing

Brainery’s core pages were analyzed using Google Lighthouse to measure performance, accessibility, best practices, and SEO. Below are the scores and corresponding links to the full Lighthouse reports:

| Page                     | Performance | Accessibility | Best Practices | SEO  |  
|--------------------------|-------------|----------------|----------------|------|  
| Home                    | **97**      | **92**         | **96**         | **90**   |  
| Dashboard               | **99**      | **97**         | **96**         | **90**   |  
| Login                   | **98**      | **89**         | **96**         | **90**   |  
| Register                | **97**      | **98**         | **96**         | **90**   |  

**Lighthouse Reports:**  
- [Home Page Report](brainery_data/static/pdfs/home-lh.pdf)  
- [Login Page Report](brainery_data/static/pdfs/login-lh.pdf)
- [Registration Report](brainery_data/static/pdfs/register-lh.pdf)  
- [Dashboard Page Report](brainery_data/static/pdfs/dashboard-lh.png)

---

### Validation Testing

All critical pages and associated stylesheets were validated using W3C tools to ensure compliance with modern web standards:

- **HTML Validation:**  
  - [Home Page Validation](brainery_data/static/images//home-html.png)  
  - [Login Page Validation](brainery_data/static/images//login-html.png)  
  - [Registration Validation](brainery_data/static/images//registration-html.png)  
  - [Dashboard Validation](brainery_data/static/images//dashboard-html.png) 

- **CSS Validation:**  
  - [Stylesheet Validation](brainery_data/static/images//styles-css.png)

---

## Bugs & Fixes

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
| **Admin Page Not Loading** | The admin dashboard failed to load due to missing route permissions. | Fixed by adding `@login_required` and checking `role == 'admin'` before rendering the page. |  
| **Users Not Displaying** | The user management table was empty because of incorrect MongoDB query. | Fixed by updating the query to `mongo.db.users.find()` and ensuring proper data retrieval. |  
| **Cannot Promote Users** | Admins couldn't promote users due to missing role update logic. | Fixed by adding an `update_one()` query to modify the `role` field in the database. |  
| **Delete User Not Working** | Clicking "Delete" did not remove users due to missing `ObjectId` conversion. | Fixed by ensuring `mongo.db.users.delete_one({"_id": ObjectId(user_id)})` correctly converts `_id`. |
| **Unauthorized Users Accessing Admin Panel** | Normal users could access the **admin panel URL** directly without authorization. | Fixed by restricting access using `if current_user.role != "admin": abort(403)` in admin routes. |
| **Session Not Clearing After Admin Logout** | Logging out as an admin didn't properly clear session data. | Fixed by calling `logout_user()` followed by `session.clear()` to fully reset the session. |  

---

### **Deployment**

This project was deployed using **Heroku**, a **cloud platform** that enables deployment and scaling of Python applications easily. Below are the **detailed steps** followed to **deploy Brainery** and make it accessible online.

---

### **Steps for Deployment on Heroku**

#### **1️⃣ Clone the Repository**
To begin, I **cloned the project repository** to my local machine:
```bash
git clone https://github.com/MH-LIKHON/MP3-Brainery.git
```

#### **2️⃣ Navigate to the Project Directory**
```bash
cd MP3-Brainery
```

#### **3️⃣ Set Up a Virtual Environment (Optional for Local Development)**
```bash
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
```

#### **4️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

#### **5️⃣ Deploying to Heroku**
This project uses **GitHub Actions** to **automatically deploy to Heroku** whenever changes are pushed to the repository.

##### **Steps to Set Up Deployment:**
1. **Connected GitHub Repository to Heroku**:
   - Created a new Heroku app using:
     ```bash
     heroku create mp3-brainery
     ```
   - Set up GitHub Actions to automatically deploy changes.

2. **Stored Environment Variables in Heroku**:
   - Added `MONGO_URI` and `SECRET_KEY` to **Heroku Config Vars**:
     ```bash
     heroku config:set MONGO_URI="your-mongodb-connection-string"
     heroku config:set SECRET_KEY="your-secret-key"
     ```

3. **Configured GitHub Actions for Continuous Deployment**:
   - Created a GitHub Actions workflow in `.github/workflows/deploy.yml` to automate deployment.
   - Secrets like `HEROKU_API_KEY` were stored in **GitHub Secrets**.

4. **Pushed Changes to Trigger Deployment**:
   - After making changes, I committed and pushed them:
     ```bash
     git add .
     git commit -m "Deploying updated version to Heroku"
     git push origin main
     ```
   - **GitHub Actions automatically deployed the updated version to Heroku**.

---

### **Accessing the Live Application**
Once deployment was successful, the app was accessible at:  
🔗 [**Brainery - Live Site**](https://mp3-brainery-7e2da4fb6ce9.herokuapp.com/)

---

### **Running the Project Locally**
To run the project **locally**, follow these steps:

#### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/MH-LIKHON/MP3-Brainery.git
```

#### **2️⃣ Navigate to the Project Directory**
```bash
cd MP3-Brainery
```

#### **3️⃣ Set Up a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
```

#### **4️⃣ Install Project Dependencies**
```bash
pip install -r requirements.txt
```

#### **5️⃣ Set Environment Variables Locally**
If testing locally, create a `.env` file and add:
```
MONGO_URI=your-mongodb-connection-string
SECRET_KEY=your-secret-key
```
📌 **Note:** The `.env` file is ignored in `.gitignore` for security.

#### **6️⃣ Run the Flask Application**
```bash
python3 app.py
```

#### **7️⃣ Open the Project in Your Browser**
- Once the server is running, open **http://127.0.0.1:5000** in a web browser.

---

### **Why Use Heroku Instead of GitHub Pages?**
✅ **Supports Full-Stack Apps** - Unlike GitHub Pages (static hosting), Heroku can host **Flask, Django, and databases**.  
✅ **Continuous Deployment** - GitHub Actions ensures **automatic deployment on every push**.  
✅ **Environment Variable Management** - Heroku securely stores **MongoDB credentials and API keys**.  

---

### **Next Steps**
**Commit and push the updated README file**:
```bash
git add README.md
git commit -m "Updated Deployment section for Heroku"
git push origin main
```
---

### **Credits**  

Brainery was built using a combination of **open-source technologies, libraries, and external assets**. Below are the tools, resources, and references used in the development of this project.  

---

### **Icons & Visual Assets**  
- **FontAwesome** – Provided **icons** for UI elements like buttons, navigation, and alerts.  
- **Unsplash** – Used for **high-quality images** where applicable.  

---

### **Media & Video Sources**  
- **Hero Section Video** – The homepage **hero background video** was sourced from:  
  - **Tactus Marketing** – [tactusmarketing.com](https://tactusmarketing.com/wp-content/uploads/tactus-waves-hero.mp4)  
  - Used to create an **immersive visual experience** for users.  

---

### **Libraries & Frameworks**  
- **Flask** – Python-based **web framework** for backend development.  
- **MongoDB** – NoSQL **database solution** for storing user data and study topics.  
- **Bootstrap 5** – **Responsive UI framework** for styling and layout.  
- **Flask-Login** – Managed **user authentication and session handling**.  
- **Flask-WTF** – Used for **form validation and CSRF protection**.  
- **Bcrypt** – Implemented **password hashing** for enhanced security.  
- **JavaScript & jQuery** – Powered **frontend interactivity and AJAX functionality**.  

---

### **APIs & Integrations**  
- **EmailJS** – Integrated for **email notifications** (password resets, confirmations).  
- **Google Fonts** – Applied custom typography for a **modern, clean look**.
- **Wikipedia API / Live Wikipedia Fetch**  
  - Brainery retrieves **live study topics** and summaries from **Wikipedia**.  
  - Wikipedia content is dynamically **loaded and stored** for reference.  

---

### **Deployment & Version Control**  
- **GitHub** – Hosted **repository, version control, and GitHub Pages deployment**.  
- **GitHub Actions** – Used for **CI/CD pipeline and automated testing**.  

---

### **Documentation References**  
- **Flask Documentation** – Used for **backend development and routing logic**.  
- **MongoDB Docs** – Guided **database schema design and queries**.  
- **Bootstrap Docs** – Assisted in **responsive design and UI enhancements**.  

---

## Acknowledgements
Thanks to **Code Institute**, **Flask Documentation**, and the **open-source community** for guidance!

Special thanks to Miguel for their guidance throughout the project.